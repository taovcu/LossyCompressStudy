CFLAGS=-O2 -g

all:
	g++ ${CFLAGS} -c bitstream.c  compressor_zlib_routines.c  error.c  isabela.c utils.c -lz -I../include -I../bspline -I../wavelets `gsl-config --cflags --libs`; 
	mv *o ../lib/

clean:
	rm -f *o
