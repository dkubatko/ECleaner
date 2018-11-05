from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from monitor import Monitor
import multiprocessing as mp

# TODO: Add request pool

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

        self.monitor = Monitor()
    
    def build_query(self, q_from, q_to, q_unread):
        '''
        Builds a Gmail searchbox query from the specified params
        :param q_from: list of email addresses
        :param q_to: list of email addresses
        :param q_unread: True/False only unread messages
        '''
        # TODO: move to constants
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

    # Monitored TODO: add decorator
    def get_messages(self, frm=[], to=[], unrd=False):
        messages = []
        # Build query string
        q = self.build_query(frm, to, unrd)
        # Make initial request
        results = self.service.users().messages().list(userId='me', q=q).execute()
        messages.extend(results.get('messages', []))

        # Make requests until all messages retrieved
        count = len(results.get('messages', []))
        self.monitor.add('count', count, True)

        while results.get('nextPageToken') is not None:
            results = self._batch_get_messages(q, results['nextPageToken'])
            messages.extend(results.get('messages', []))
            count = self.monitor.set('count', count + len(results.get('messages', [])))

        return {'messages': messages, 'count': count}

    # Threaded TODO: add decorator
    def _mark_one_read(self, id):
        #TODO: move to constants
        body = {
            'addLabelIds': [],
            'removeLabelIds': ['UNREAD']
        }
        result = self.service.users().messages().modify(userId='me', 
            id=id, body=body).execute(http=self.creds.authorize(Http()))
        return True if result else False

    def _chunks(self, l, n):
        """Helper function to yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    # Monitored TODO: add decorator
    # Threaded TODO: add decorator
    def mark_read(self, ids, num_threads = 1):
        '''
        Marks every message in the list of ids as read
        :param ids: list of message ids
        '''
        self.monitor.add('success', 0, monitor=True)
        total = len(ids)
        # Split ids into chunks of size |threads|
        groups = list(self._chunks(ids, num_threads))
        
        # Thread callback func
        def read_callback(result):
            success = 0
            if result:
                self.monitor.inc('success')

        for group in groups:
            pool = mp.Pool(num_threads)
            for _id in group:
                pool.apply_async(self._mark_one_read, 
                        args=(_id, ), callback=read_callback)
            pool.close()
            # Join all read threads
            pool.join()

        return {'success': self.monitor.get('success'), 'total': total}
    
    def get_message(self, id):
        results = self.service.users().messages().get(userId='me', id=id).execute()
        return {'labels': results['labelIds'], 'snippet': results['snippet']}

from pprint import pprint as pp

if __name__ == '__main__':
    gmc = GmailClient()
    # pp(gmc.get_messages(['boris, vladimir'], ['me'], False))
    print("Starting unread messages retrieval:")
    msgs = gmc.get_messages(unrd=True)
    print("\nDone")
    print("Marking as read:")
    ids = [m['id'] for m in msgs['messages']]
    gmc.mark_read(ids, num_threads=5)
    print("\nDone")
    
