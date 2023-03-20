#!/usr/bin/env python3


from utils import *
from test_engine import *

def main():
    y,n,saved = 0,0,deepcopy(the)
    for k,v in cli(settings(help)).items():
        the[k] = v
        saved[k] = v
    if the['help'] == True:
        print(help)
    else:
        for what, fun in egs.items():
            if the['go'] == 'all' or the['go'] == what:
                for k,v in saved.items():
                    the[k] = v
                Seed = the['seed']
                print('▶️ ',what,("-")*(60))
                if egs[what]() == False:
                    n += 1
                    print('❌ fail:', what)
                else:
                    y += 1
                    print('✅ pass:', what)
    if y+n>0:
        print("🔆",{'pass' : y, 'fail' : n, 'success' :100*y/(y+n)//1})
    sys.exit(n)

if __name__ == '__main__':
    eg('ok', 'ok', test_ok)
    eg('sample', 'sample', test_sample)
    eg('nums', 'nums', test_num)
    eg('gauss', 'gauss', test_gauss)
    eg('bootmu', 'bootmu', test_bootmu)
    eg('basic', 'basic', test_basic)
    eg('pre', 'pre', test_pre)
    eg('five', 'five', test_five)
    eg('six', 'six', test_six)
    eg('tiles', 'tiles', test_tiles)
    eg('sk', 'sk', test_sk)
    main()