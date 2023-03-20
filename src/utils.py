import sys, re, math, copy, json, random
from the import *
from pathlib import Path
from sym import SYM
from operator import itemgetter


def settings(s):
    return dict(re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s))


def coerce(s):
    if s == 'true':
        return True
    elif s == 'false':
        return False
    elif s.isdigit():
        return int(s)
    elif '.' in s and s.replace('.', '').isdigit():
        return float(s)
    else:
        return s


def cli(options):
    args = sys.argv[1:]
    for k, v in options.items():
        for n, x in enumerate(args):
            if x == '-' + k[0] or x == '--' + k:
                if v == 'false':
                    v = 'true'
                elif v == 'true':
                    v = 'false'
                else:
                    v = args[n + 1]
        options[k] = coerce(v)
    return options


def eg(key, str, fun):
    egs[key] = fun
    global help
    help = help + '  -g ' + key + '\t' + str + '\n'


def deepcopy(t):
    return copy.deepcopy(t)


def rint(lo, hi, mSeed=None):
    return math.floor(0.5 + rand(lo, hi, mSeed))


def rand(lo, hi, mSeed=None):
    lo, hi = lo or 0, hi or 1
    global Seed
    Seed = 1 if mSeed else (16807 * Seed) % 2147483647
    return lo + (hi - lo) * Seed / 2147483647


def rnd(n, nPlaces=3):
    mult = 10 ** nPlaces
    return math.floor(n * mult + 0.5) / mult


def firstN(sortedRanges, scoreFun):
    print("")

    def function(r):
        print(r['range']['txt'], r['range']['lo'], r['range']['hi'], rnd(r['val']), r['range']['y'].has)

    _ = list(map(function, sortedRanges))
    print()
    first = sortedRanges[0]['val']

    def useful(range):
        if range['val'] > .05 and range['val'] > first / 10:
            return range

    sortedRanges = [x for x in sortedRanges if useful(x)]
    most, out = -1, -1
    for n in range(1, len(sortedRanges) + 1):
        slice = sortedRanges[0:n]
        slice_range = [x['range'] for x in slice]
        tmp, rule = scoreFun(slice_range)
        if tmp and tmp > most:
            out, most = rule, tmp
    return out, most


def prune(rule, maxSize):
    n = 0
    for txt, ranges in rule.items():
        n = n + 1
        if len(ranges) == maxSize[txt]:
            n = n + 1
            rule[txt] = None
    if n > 0:
        return rule


def samples(t, n=None):
    u = {}
    for i in range(1, (n or len(t)) + 1):
        u[i] = t[random.randint(0, len(t) - 1)]
    return u


def gaussian(mu, sd):
    mu, sd = mu or 0, sd or 1
    sq, pi, log, cos, r = math.sqrt, math.pi, math.log, math.cos, random.random
    return mu + sd * sq(-2 * log(r())) * cos(2 * pi * r())


def cliffsDelta(ns1, ns2):
    if len(ns1) > 128:
        ns1 = samples(ns1, 128)
    if len(ns2) > 128:
        ns2 = samples(ns2, 128)
    n, gt, lt = 0, 0, 0
    for x in ns1:
        for y in ns2:
            n = n + 1
            if x > y:
                gt = gt + 1
            if x < y:
                lt = lt + 1
    return abs(lt - gt) / n <= the['cliff']


def delta(i, other):
    e, y, z = 1E-32, i, other
    return abs(y.mu - z.mu) / ((e + y.sd ** 2 / y.n + z.sd ** 2 / z.n) ** .5)


def bootstrap(y0, z0, NUM):
    x, y, z, yhat, zhat = NUM(), NUM(), NUM(), [], []
    for y1 in y0:
        x.add(y1)
        y.add(y1)
    for z1 in z0:
        x.add(z1)
        z.add(z1)
    xmu, ymu, zmu = x.mu, y.mu, z.mu
    for y1 in y0:
        yhat.append(y1 - ymu + xmu)
    for z1 in z0:
        zhat.append(z1 - zmu + xmu)
    tobs = delta(y, z)
    n = 0
    for _ in range(1, the['bootstrap'] + 1):
        i = NUM()
        other = NUM()
        for y in samples(yhat).values():
            i.add(y)
        for z in samples(zhat).values():
            other.add(z)
        if delta(i, other) > tobs:
            n = n + 1
    return n / the['bootstrap'] >= the['conf']


def RX(t, s):
    t = sorted(t)
    return {'name': s or "", 'rank': 0, 'n': len(t), 'show': "", 'has': t}


def div(t):
    t = t['has'] if t['has'] else t
    return (t[len(t) * 9 // 10] - t[len(t) * 1 // 10]) / 2.56


def mid(t):
    t = t['has'] if t['has'] else t
    n = (len(t) - 1) // 2
    return (t[n] + t[n + 1]) / 2 if len(t) % 2 == 0 else t[n + 1]


def merge(rx1, rx2):
    rx3 = RX([], rx1['name'])
    rx3['has'] = rx1['has'] + rx2['has']
    rx3['has'] = sorted(rx3['has'])
    rx3['n'] = len(rx3['has'])
    return rx3


def rxs_sort(rxs):
    for i, x in enumerate(rxs):
        for j, y in enumerate(rxs):
            if mid(x) < mid(y):
                rxs[j], rxs[i] = rxs[i], rxs[j]
    return rxs


def scottKnot(rxs, NUM):
    def merges(i, j):
        out = RX([], rxs[i]['name'])
        for k in range(i, j + 1):
            out = merge(out, rxs[j])
        return out

    def same(lo, cut, hi):
        l = merges(lo, cut)
        r = merges(cut + 1, hi)
        return cliffsDelta(l['has'], r['has']) and bootstrap(l['has'], r['has'], NUM)

    def recurse(lo, hi, rank):
        b4 = merges(lo, hi)
        best = 0
        cut = None
        for j in range(lo, hi + 1):
            if j < hi:
                l = merges(lo, j)
                r = merges(j + 1, hi)
                now = (l['n'] * (mid(l) - mid(b4)) ** 2 + r['n'] * (mid(r) - mid(b4)) ** 2) / (l['n'] + r['n'])
                if now > best:
                    if abs(mid(l) - mid(r)) >= cohen:
                        cut, best = j, now
        if cut != None and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank = recurse(cut + 1, hi, rank)
        else:
            for i in range(lo, hi + 1):
                rxs[i]['rank'] = rank
        return rank

    rxs = rxs_sort(rxs)
    cohen = div(merges(0, len(rxs) - 1)) * the['cohen']
    recurse(0, len(rxs) - 1, 1)
    return rxs


def tiles(rxs):
    huge = float('inf')
    lo, hi = huge, float('-inf')
    for rx in rxs:
        lo, hi = min(lo, rx['has'][0]), max(hi, rx['has'][len(rx['has']) - 1])
    for rx in rxs:
        t, u = rx['has'], []

        def of(x, most):
            return int(max(0, min(most, x)))

        def at(x):
            return t[of(len(t) * x // 1, len(t))]

        def pos(x):
            return math.floor(of(the['width'] * (x - lo) / (hi - lo + 1E-32) // 1, the['width']))

        for i in range(0, the['width'] + 1):
            u.append(" ")
        a, b, c, d, e = at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E = pos(a), pos(b), pos(c), pos(d), pos(e)
        for i in range(A, B + 1):
            u[i] = "-"
        for i in range(D, E + 1):
            u[i] = "-"
        u[the['width'] // 2] = "|"
        u[C] = "*"
        x = []
        for i in [a, b, c, d, e]:
            x.append(the['Fmt'].format(i))
        rx['show'] = ''.join(u) + str(x)
    return rxs