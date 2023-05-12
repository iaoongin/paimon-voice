import time
from util import log_factory

def timing(fun, args=None, title='', logger=None):
    s = time.time()

    if args:
        r = fun(args)
    else:
        r = fun()
    e = time.time()

    if logger is not None:
        logger.debug('%scost: %s' % (title+' ', (e-s)))
    
    return r