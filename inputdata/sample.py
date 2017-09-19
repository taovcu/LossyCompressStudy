import numpy as np

import struct
import sys
import array
import os
import random
import argparse
import re

sample_ratio = 0.01
chunksize = 40
blksize = 4
def prefixSample(inputfile, outputfile, ratio):
    statinfo = os.stat(inputfile)
    fsize = statinfo.st_size
    original_elem_count = fsize / 8
    sample_elem_num = int(original_elem_count * ratio)
    a = array.array('d', (fsize / 8) * [0])
    with open(inputfile, 'rb') as fin:
        fin.readinto(a)
        fout =  open(outputfile, 'wb')
        a[:sample_elem_num].tofile(fout)
        fout.close()

def intervalSample(inputfile, outputfile, opt, ratio):
    statinfo = os.stat(inputfile)
    fsize = statinfo.st_size
    original_elem_count = fsize / 8
    sample_elem_num = int(original_elem_count * ratio)
    a = array.array('d', (fsize / 8) * [0])
    with open(inputfile, 'rb') as fin:
        fin.readinto(a)
        samplepoints = array.array('d')
        if opt == 'point':
            stride = int(1 / ratio)
            offset = random.randrange(0, stride)
            for i in sample_elem_num:
                samplepoints.append(a[i+offset])
        if opt == 'block':
            stride = int(1 / ratio * blksize) 
            offset = random.randrange(0, stride / blksize)
            for i in (sample_elem_num / blksize):
                samplepoints += a[(i+offset)*4:(i+offset+1)*4]
        if opt == 'chunk':
            stride = int(1 / ratio * chunksize) 
            offset = random.randrange(0, stride / chunksize)
            for i in (sample_elem_num / chunksize):
                samplepoints += a[(i+offset)*chunksize:(i+offset+1)*chunksize]

        print samplepoints[:10]
        fout =  open(outputfile, 'wb')
        samplepoints.tofile(fout)
        fout.close()

def randomSample(inputfile, outputfile, opt, ratio):
    statinfo = os.stat(inputfile)
    fsize = statinfo.st_size
    original_elem_count = fsize / 8
    sample_elem_num = int(original_elem_count * ratio)
    a = array.array('d', (fsize / 8) * [0])
    with open(inputfile, 'rb') as fin:
        fin.readinto(a)
        samplepoints = array.array('d')
        if opt == 'point':
            sampleidx = random.sample(range(len(a)), sample_elem_num)
            for i in sorted(sampleidx):
                samplepoints.append(a[i])
        if opt == 'block':
            sampleidx = random.sample(range(len(a)/4), sample_elem_num/4)
            for i in sorted(sampleidx):
                samplepoints += a[i*4:(i+1)*4]
        if opt == 'chunk':
            sampleidx = random.sample(range(len(a)/chunksize), sample_elem_num/chunksize)
            for i in sorted(sampleidx):
                samplepoints += a[i*chunksize:(i+1)*chunksize]

        print samplepoints[:10]
        fout =  open(outputfile, 'wb')
        samplepoints.tofile(fout)
        fout.close()

def signalReconstruct(distfile, outputfile, opt, samplesize):
    sample = array.array('d')
    lastpct = 0
    lastval = 0
    with open(distfile) as f:
        content = f.readlines()
        if opt == 'uniform':
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
    
                curRange = int(samplesize * (float(pct) - lastpct) / 100)
    
                if lastval == float(val):
                    sample = sample + array.array('d', curRange * [float(val)])
                else:
                    for i in range(curRange):
                        sample.append(random.uniform(lastval, float(val)))
                lastpct = float(pct)
                lastval = float(val)
        if opt == 'skew':
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
    
                curRange = int(samplesize * (float(pct) - lastpct) / 100)
    
                if lastval == float(val):
                    sample = sample + array.array('d', curRange * [float(val)])
                else:
                    for i in range(curRange):
                        sample.append(random.uniform(lastval, lastval + (float(val)-lastval)/100))
                lastpct = float(pct)
                lastval = float(val)
            
        fout =  open(outputfile, 'wb')
        print sample[:10]
        sample.tofile(fout)
        fout.close()
    
    

def main():
    parser = argparse.ArgumentParser(description='Select sampling method')
    parser.add_argument('-s','--sample', help='choose sampling method, either prefix, interval, random, or reconstruct', required=True)
    parser.add_argument('-i','--input', help='original file', required=True)
    #parser.add_argument('-o','--output', help='output sample file', required=True)
    parser.add_argument('-r','--randopt', help='interval or random sampling option, either point, block or chunk', required=False)
    parser.add_argument('-c','--constructopt', help='reconstruct option, either uniform, or skew', required=False)
    parser.add_argument('-n','--num', help='reconstruction sample size', required=False)
    args = vars(parser.parse_args())
    print args

    if args['sample'] == 'prefix':
        prefixSample(args['input'], 'prefixSample/' + args['input'], sample_ratio)
    if args['sample'] == 'interval':
        randomSample(args['input'], args['randopt'] + 'intervalSample/' + args['input'], args['randopt'], sample_ratio)
    if args['sample'] == 'random':
        randomSample(args['input'], args['randopt'] + 'randomSample/' + args['input'], args['randopt'], sample_ratio)
    if args['sample'] == 'reconstruct':
        signalReconstruct(args['input'], 'reconstruct' + args['constructopt'] + '/' + re.split('/|\.', args['input'])[-2], args['constructopt'], int(args['num']))
    

if __name__ == "__main__":
    main()
