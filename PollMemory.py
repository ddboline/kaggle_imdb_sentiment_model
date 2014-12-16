############################
# Written by Daniel Boline #
#       2013-03-05         #
############################

#########################################################################
# Module contains:
#     Three utility functions which grab memory usage information from the linux proc directory for the current process.
#     A class designed to track memory consumption by individual analysis processors
#########################################################################

import os
import datetime
_proc_status = '/proc/%d/status' % os.getpid()

_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}

def _VmB(VmKey):
    '''
        stolen from the interwebs, just reads info from proc and slightly formats it
    '''
    global _proc_status, _scale
    # get pseudo file  /proc/<pid>/status
    try:
        with open(_proc_status) as t:
            v = t.read()
    except:
        return 0.0  # non-Linux?
    # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
    # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]

def _userFriendlyBytes(nbytes):
    ''' pretty formating '''
    ostr = ''
    for tb in nbytes:
        megbytes = tb/(1024.0*1024.0)
        ostr = '%s%8s' % (ostr, '%i MB ' % megbytes)
    return ostr

def memory(since=0.0):
    ''' Return memory usage in bytes. '''
    return _VmB('VmSize:') - since


def resident(since=0.0):
    ''' Return resident memory usage in bytes. '''
    return _VmB('VmRSS:') - since


def stacksize(since=0.0):
    ''' Return stack size in bytes. '''
    return _VmB('VmStk:') - since

def timeinseconds(orig_time=None):
    ''' find time in seconds since orig_time '''
    if not orig_time:
        print 'no time given'
        exit(0)
    td = (datetime.datetime.now() - orig_time)
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / float(10**6)

def cumtime(orig_time=None, since=0.0):
    return timeinseconds(orig_time) - since

class MemoryConsumption(object):
    ''' class object to keep track of memory / time consumption '''
    def __init__(self, keys=None, label='memory'):
        self.ordered_list_of_keys = ['TOTAL']
        self.begin_time = datetime.datetime.now()
        self.processors = {'TOTAL': [memory(), resident(), stacksize(), cumtime(self.begin_time)]}
        self.poll_idx = {'TOTAL': 0}
        if not keys:
            keys = []
        for key in keys:
            self.processors[key] = [0., 0., 0., 0.]
            self.ordered_list_of_keys.append(key)
        self.current_mem = [memory(), resident(), stacksize(), cumtime(self.begin_time)]
        self.current_time = 0.0
        self.label = label

    def add_key(self, key):
        ''' add label/key '''
        self.processors[key] = [0., 0., 0., 0.]
        self.ordered_list_of_keys.append(key)
        self.poll_idx[key] = 0
        self.poll(key)

    def poll(self, key=''):
        ''' poll memory/time consumption for current key '''
        m, r, s, t = self.current_mem
        added_mem = [memory(m), resident(r), stacksize(s), cumtime(self.begin_time, t)]
        self.current_mem = [memory(), resident(), stacksize(), cumtime(self.begin_time)]
        self.current_time = cumtime(self.begin_time)
        for i in range(0, 4):
            if key in self.processors and key != 'TOTAL':
                if added_mem[i] < 0:
                    print 'memory is reduced', added_mem, key, cumtime(self.begin_time, t), cumtime(self.begin_time), m, r, s, t
                    #exit(0)
                self.processors[key][i] += added_mem[i]
            self.processors['TOTAL'][i] += added_mem[i]
        if key in self.processors and key != 'TOTAL':
            self.poll_idx[key] += 1
        self.poll_idx['TOTAL'] += 1

    def print_memory_consumption(self, pref=''):
        ''' print current memory consumption for all keys '''
        self.poll(self)
        for key in self.ordered_list_of_keys:
            item = self.processors[key]
            print 'memory consumption %s: %25s \t %s \t %i s' % (pref, key, _userFriendlyBytes(item[:3]), item[3])
        print ''

    def write_graphs(self):
        ''' not implemented (was it ever?) '''
        pass

if __name__ == '__main__':
    print 'PollMemory doesn\'t do anything when called directly'
    exit(0)
