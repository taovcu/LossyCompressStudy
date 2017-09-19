import numpy as np
import random

import struct
import sys
import array
import os

zfpBlocks = 2500 # 4 points each
SZpiece = 100 # 100 points each

statinfo = os.stat(sys.argv[1])
fsize = statinfo.st_size

a = array.array('d', (fsize / 8) * [0])

fin =  open(sys.argv[1], 'rb')
fin.readinto(a)

zfppoints = array.array('d')
szpoints = array.array('d')

zfpSample = random.sample(range(len(a)/4), zfpBlocks)
szSample = random.sample(range(len(a)/100), SZpiece)


for i in sorted(zfpSample):
    zfppoints += a[i*4:i*4+4]

for i in sorted(szSample):
    szpoints += a[i*100:i*100+100]

print zfppoints[:10]
print szpoints[:10]

fout =  open(sys.argv[2], 'wb')
zfppoints.tofile(fout)

fout =  open(sys.argv[3], 'wb')
szpoints.tofile(fout)

fout.close()
