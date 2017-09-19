import h5py, numpy

#f = h5py.File('yf17_hdf5.cgns')
f = h5py.File('bump_hdf5.cgns')


ds = f['/Base/Zone   1/FlowSolution/Density'][' data']

t = ds[:].astype(numpy.float64)

print t[0]
print t.ravel()[:10]

#print t[1]
#print t[2]

fout =  open("bump_dense.dat", 'wb')
fout.write(t.ravel())
fout.close()
