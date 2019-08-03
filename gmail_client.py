from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client import file, client, tools
from monitor import Monitor, monitored
import multiprocessing as mp

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'

class GmailClient:
    def __init__(self):
        store = file.Storage('token.json')
        self.creds = store.get()
        if not self.creds or self.creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            self.creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=self.creds.authorize(Http()))
    
    def build_query(self, q_from, q_to, q_unread):
        '''
        Builds a Gmail searchbox query from the specified params
        :param q_from: list of email addresses
        :param q_to: list of email addresses
        :param q_unread: True/False only unread messages
        '''
        s_from = list(map(lambda e: f'from:{e}', q_from))
        s_from = '{' + ' '.join(s_from) + '}'

        s_to = list(map(lambda e: f'to:{e}', q_to))
        s_to = '{' + ' '.join(s_to) + '}'
        
        s_unread = 'is:' + 'unread' if q_unread else 'read'

        return f'{s_from} {s_to} {s_unread}'
    
    def get_labels(self):
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return labels

    def _batch_get_messages(self, q, token):
        results = self.service.users().messages().list(userId='me', q=q, pageToken=token).execute()
        return results

    @monitored('Fetch mail', ['count'])
    def get_messages(self, frm=[], to=[], unrd=False, monitor=None):
        messages = []
        # Build query string
        q = self.build_query(frm, to, unrd)
        # Make initial request
        results = self.service.users().messages().list(userId='me', q=q).execute()
        messages.extend(results.get('messages', []))

        # Make requests until all messages retrieved
        
        count = monitor.upd('count', len(results.get('messages', [])))
        while results.get('nextPageToken') is not None:
            results = self._batch_get_messages(q, results['nextPageToken'])
            messages.extend(results.get('messages', []))
            count = monitor.upd('count', count + len(results.get('messages', [])))

        return {'messages': messages, 'count': count}

    def _mark_one_read(self, id):
        body = {
            'addLabelIds': [],
            'removeLabelIds': ['UNREAD']
        }

        try:
            result = self.service.users().messages().modify(userId='me', 
                id=id, body=body).execute(http=self.creds.authorize(Http()))
        except HttpError as e:
            return (id, False)


        return (id, True) if result else (id, False)

    def _chunks(self, l, n):
        """Helper function to yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @monitored('Mark as unread', ['success', 'failure'])
    def mark_read(self, ids, num_threads = 1, monitor=None):
        '''
        Marks every message in the list of ids as read
        :param ids: list of message ids
        '''
        total = len(ids)
        # Split ids into chunks of size |threads|
        groups = list(self._chunks(ids, num_threads))

        for group in groups:
            with mp.Pool(num_threads) as pool:
                for (id, result) in pool.map(self._mark_one_read, group):
                    if result:
                        monitor.inc('success')
                    else:
                        monitor.inc('failure')

        return {'success': monitor.get('success'), 'total': total}

    def get_message(self, id):
        results = self.service.users().messages().get(userId='me', id=id).execute()
        return {'labels': results['labelIds'], 'snippet': results['snippet']}

from pprint import pprint as pp

if __name__ == '__main__':
    gmc = GmailClient()
    print("Starting unread messages retrieval:")
    msgs = gmc.get_messages(unrd=True)
    print("Marking as read:")
    ids = [m['id'] for m in msgs['messages']]
    gmc.mark_read(ids, num_threads=30)
