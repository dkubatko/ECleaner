class Monitor():
    '''
    Remote storage class to monitor and maintain variables
    '''
    def __init__(self):
        self.vars = {}
    
    def add(self, var, val=0, monitor=True):
        self.vars[var] = {'val': val, 'monitor': monitor}
        if monitor:
            self.alert()
    
    def inc(self, var):
        self.vars[var]['val'] += 1
        if self.vars[var]['monitor']:
            self.alert()
        return self.vars[var]['val']
    
    def upd(self, var, val):
        self.vars[var]['val'] = val
        if self.vars[var]['monitor']:
            self.alert()
        return val

    def get(self, var):
        return self.vars[var]['val']

    def monitor(self, var):
        self.vars[var]['monitor'] = True

    def alert(self):
        # Get monitored variables and their values
        vrs = [var for var in self.vars.keys() if self.vars[var]['monitor']]
        vals = [str(self.vars[v]['val']) for v in vrs]
        # Convert to display format
        s_vrs = ', '.join(vrs)
        s_vals = ', '.join(vals)
        print(f'\r[{s_vrs}] progress: |{s_vals}|', end = '\r')

class monitored(object):
    def __init__(self, args):
        """
        Set up monitored variables
        """
        print(f"Setting monitor for {args}")
        # Add each variable to the monitor
        self.monitor = Monitor()
        list(map(self.monitor.add, args))
        print(self.monitor.vars)

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        print("Inside __call__()")
        def wrapped_f(*args, **kwargs):
            monitor = self.monitor
            result = f(*args, monitor=monitor, **kwargs)
            print("\nTask finished")
            return result
        return wrapped_f
