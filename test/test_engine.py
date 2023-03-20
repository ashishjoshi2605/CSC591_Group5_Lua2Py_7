from utils import *
from num import NUM
from sym import SYM
import random

def test_ok(n=None):
    if(n):
        random.seed(n)
    else:
        random.seed(1)

def test_sample():
    for i in range(1,11):
        print("", "".join(samples(["a", "b", "c", "d", "e"])))


def test_num():
    n = NUM()
    for i in range(10):
        n.add(i+1)

    print("", n.n, n.mu, n.sd)

def test_gauss():
    t = []
    for _ in range(1,10**4+1):
        t.append(gaussian(10,2))

    n = NUM()
    for i in t:
        n.add(i)

    print("", n.n, n.mu, n.sd)

def test_bootmu():
    a,b = [],[]
    for _ in range(1,101):
        a.append(gaussian(10,1))
    print("","mu","sd","cliffs","boot","both")
    print("","--","--","------","----","----")

    for mu in range(10,11.1,0.1):
        b = []
        for _ in range(1,101):
            b.append(gaussian(mu,1))

    cl = cliffsDelta(a,b)
    bs = bootstrap(a,b)
    print("",mu,1,cl,bs,cl and bs)

def test_basics():
    print("\t\ttruee", bootstrap( {8, 7, 6, 2, 5, 8, 7, 3}, 
                                {8, 7, 6, 2, 5, 8, 7, 3} , NUM),
              cliffsDelta( {8, 7, 6, 2, 5, 8, 7, 3}, 
                           {8, 7, 6, 2, 5, 8, 7, 3}))
    print("\t\tfalse", bootstrap(  {8, 7, 6, 2, 5, 8, 7, 3},  
                                 {9, 9, 7, 8, 10, 9, 6} , NUM),
             cliffsDelta( {8, 7, 6, 2, 5, 8, 7, 3},  
                          {9, 9, 7, 8, 10, 9, 6})) 
    print("\t\tfalse", 
                    bootstrap({0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6}, 
                               {0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9} , NUM),
                  cliffsDelta({0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6}, 
                              {0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9})
   )
    
def test_pre():
    print("\neg3")
    d = 1
    for _ in range(1,11):
        t1 , t2 = [] , []
        for _ in range(1,33):
            t1.append(gaussian(10,1))
            t2.append(gaussian(d*10,1))

        d_value = True if d<1.1 else False
        print("\t",d,d_value,bootstrap(t1,t2,NUM),bootstrap(t1,t1,NUM))


    

