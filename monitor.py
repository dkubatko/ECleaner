class Monitor():
    '''
    Remote storage class to monitor and maintain variables
    '''
    def __init__(self):
        self.vars = {}
    
    def add(self, var, val, monitor=False):
        self.vars[var] = {'val': val, 'monitor': monitor}
        if monitor:
            self.alert(var)
    
    def inc(self, var):
        self.vars[var]['val'] += 1
        if self.vars[var]['monitor']:
            self.alert(var)
        return self.vars[var]['val']

    def get(self, var):
        return self.vars[var]['val']

    def monitor(self, var):
        self.vars[var]['monitor'] = True

    def alert(self, var):
        val = self.vars[var]['val']
        print('\r%s progress: |%s|' % (var, val), end = '\r')
        # print(f'{var} has changed to {val}')
        self.vars[var]['changed'] = False