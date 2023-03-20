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