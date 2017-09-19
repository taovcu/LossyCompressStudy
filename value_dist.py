import numpy as np
import operator

import struct
import sys
import array
import os

p = []
for i in range(101):
    p.append(i)
#p = [0.01, 0.1, 1, 5, 10, 20, 30, 40, 50, 60,70,80,90,95,99,99.9]

statinfo = os.stat(sys.argv[1])
fsize = statinfo.st_size

a = array.array('d', (fsize / 8) * [0])
c = array.array('c', fsize * ['0'])

fin =  open(sys.argv[1], 'rb')
fin.readinto(a)

fin =  open(sys.argv[1], 'rb')
fin.readinto(c)

print "minimum", np.percentile(a, 0)
print "median", np.percentile(a, 50)
print "average", np.mean(a)
print "maximum", np.percentile(a, 100)

d = dict()
for i in c:
    if i in d:
        d[i] += 1
    else:
        d[i] = 1

sorted_d = sorted(d.items(), key=operator.itemgetter(1))
tenth = 0
for i in range(len(sorted_d)):
    tenth += sorted_d[i][1]
    if tenth * 1.0 / fsize >= 0.1:
        print len(sorted_d) - i
        break

#print np.corrcoef([a, range(len(a))])


#for i in range(len(p)):
#    print p[i],",",np.percentile(a, p[i])


#np.random.shuffle(a)
#print np.corrcoef([a, range(len(a))])

#a = np.sort(a)
#print np.corrcoef([a, range(len(a))])

#print a[20693]

#print(struct.unpack('d', fin.read(8)))


#self.assertEqual(v.read(), npval)
