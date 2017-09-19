CFLAGS=-O2 -g

all:
	g++ ${CFLAGS} -o file_compress -DCOMPRESS=1 file_compress.c -I../../include -L../../lib -lisabela -lgsl -lgslcblas -lz
	g++ ${CFLAGS} -o file_decompress file_compress.c -I../../include -L../../lib -lisabela -lz -lgsl -lgslcblas

clean:
	rm -f *o;
	rm -f file_compress file_decompress;
