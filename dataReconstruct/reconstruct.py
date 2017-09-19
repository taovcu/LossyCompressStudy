import numpy as np

import struct
import sys
import array
import os
import random

p = []
for i in range(101):
    p.append(i)

statinfo = os.stat(sys.argv[1])
fsize = statinfo.st_size

original_elem_count = 1000000
sample_ratio = 0.001
sample_elem_num = original_elem_count * sample_ratio

sample = []
lastpct = 0
lastval = 0
with open(sys.argv[1]) as f:
    content = f.readlines()
    for l in content:
        (pct, val) = tuple(l.split(','))
        if float(pct) == 0:
            sample.append(float(val))
            lastval = float(val)
            continue
        if float(pct) == 100:
            sample.append(float(val))
            lastpct = float(pct)
            lastval = float(val)
            continue

        curRange = int(sample_elem_num * (float(pct) - lastpct) / 100)

        if lastval == float(val):
            sample = sample + curRange * [float(val)]
        else:
            for i in range(curRange):
                sample.append(random.uniform(lastval, float(val)))

        lastpct = float(pct)
        lastval = float(val)

#print sample

def corrcoefInBlock(t):
    i = 0
    res = []
    while i+3 <= len(t):
        a = t[i:i+4]
        b = [1,2,3,4]
        coeff = np.corrcoef([t, range(len(t))])
        res.append(coeff[0][1])
        i += 4
    return np.mean(res)

for i in range(len(p)):
    print p[i],",",np.percentile(sample, p[i])

t = np.asarray(sample, dtype=np.float64)

#fout =  open("FishSample_sorted.dat", 'wb')
fout =  open("dpotSample_sorted.dat", 'wb')
t = np.sort(t)
print corrcoefInBlock(t)
fout.write(t)
fout.close()

np.random.shuffle(t)
print corrcoefInBlock(t)
#fout =  open("FishSample_random.dat", 'wb')
fout =  open("dpotSample_random.dat", 'wb')
fout.write(t)
fout.close()


#a = array.array('d', 101 * [0])
#
#fin =  open("dpotSample_sorted.dat", 'rb')
#fin.readinto(a)
#print a
#print '//////////////////'
#fin =  open("dpotSample_random.dat", 'rb')
#fin.readinto(a)
#print a
