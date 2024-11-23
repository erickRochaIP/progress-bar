from inspect import signature
import time

import sys,time

def track_progress(func):
    def wrapper(**k):
        itP(func, k,
        {
        'display': True,
        'label': lambda x: str(x)
        }
        )
    return wrapper

def progress_bar(acc, tot, opt, conc):
    if not opt or 'display' not in opt or not opt['display']:
        return
    
    bar_length = 50
    filled_length = int(bar_length * acc / tot)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    perc = round(100.0 * acc / tot, 2)
    sys.stdout.write('\033[2K\033[1G')
    sys.stdout.write('[%s] %s%% ' %(bar, perc))
    if 'label' in opt:
        sys.stdout.write(opt['label'](conc))
    sys.stdout.flush()

def rec(f, acc, tot, conc, arg_lists, opt):
    if not arg_lists:
        f(**conc)
        progress_bar(acc+1, tot, opt, conc)
        return acc+1
    
    l, *_ = arg_lists.keys()
    for el in arg_lists[l]:
        acc = rec(
            f,
            acc,
            tot,
            {
                **conc,
                **{
                    l: el
                }
            },
            {k:v for k, v in arg_lists.items() if k != l},
            opt
        )
    return acc

def itP(f, a: dict[str, list], opt=None) -> None:
    if not callable(f):
        raise TypeError()
    
    if not isinstance(a, dict):
        raise TypeError()
    
    f_keys = signature(f).parameters.keys()
    a_keys = a.keys()
    if bool(f_keys-a_keys) or bool(a_keys-f_keys):
        raise ValueError()

    tot = 1
    for el in a:
        if not isinstance(a[el], list):
            raise TypeError()
        if len(a[el]) == 0:
            raise ValueError()
        tot*=len(a[el])

    rec(f, 0, tot, {}, a, opt)
    sys.stdout.write('\n')
    sys.stdout.flush()

def printer(a, b, c):
    time.sleep(1)
    
# itP(printer, {
#     'a': [1, 2],
#     'b': ['a', 'b'],
#     'c':['chess', 'pawn']
#     },
#     {
#         'display': True,
#         'label': lambda x: str(x)
#     }
# )

@track_progress
def wait(a, b):
    time.sleep(a+b)

wait(
    a=[1, 2, 3],
    b=[0.5, 1.5]
)
