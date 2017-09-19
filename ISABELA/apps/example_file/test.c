#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string>

#include <zlib.h>
#include <zconf.h>

using namespace std;

#define CHUNK 16384

int def(FILE *source, FILE *dest, int level)
{
	z_stream strm;
	strm.zalloc = Z_NULL;
	strm.zfree = Z_NULL;
	strm.opaque = Z_NULL;
	deflateInit(&strm, level);

	int flush;
	int have;
	unsigned char in[CHUNK];
	unsigned char out[CHUNK];
	do 
	{
		strm.avail_in = fread(in, 1, CHUNK, source);
		strm.next_in = in;
		flush = feof(source) ? Z_FINISH : Z_NO_FLUSH;

		do 
		{
			strm.avail_out = CHUNK;
			strm.next_out = out;

			deflate(&strm, flush);

			have = CHUNK - strm.avail_out;
			fwrite(out, 1, have, dest);

		} while (0 == strm.avail_out);

	} while (Z_FINISH != flush);

	deflateEnd(&strm);

	return Z_OK;
}

int inf(FILE *source, FILE *dest)
{
	z_stream strm;
	strm.zalloc = Z_NULL;
	strm.zfree = Z_NULL;
	strm.opaque = Z_NULL;
	inflateInit(&strm);

	int ret = Z_OK;
	int have;
	unsigned char in[CHUNK];
	unsigned char out[CHUNK];
	do 
	{
		strm.avail_in = fread(in, 1, CHUNK, source);
		strm.next_in = in;
		if(0 == strm.avail_in)
			break;

		do 
		{
			strm.avail_out = CHUNK;
			strm.next_out = out;

			ret = inflate(&strm, Z_NO_FLUSH);

			have = CHUNK - strm.avail_out;
			fwrite(out, 1, have, dest);

		} while (0 == strm.avail_out);
	} while (Z_STREAM_END != ret);

	inflateEnd(&strm);

	return Z_OK;
}

int main(int argc, char *argv[])
{

	cout<<"zlibVersion:"<<zlibVersion()<<endl;

	FILE *fp1 = fopen("1.txt","rb+");
	FILE *fp2 = fopen("2.txt", "rb+");
	FILE *fp3 = fopen("3.txt", "rb+");
	if((NULL == fp3) || (NULL == fp3) || (NULL == fp3))
	{
		cout<<"fail to open file."<<endl;
		return 0;
	}

	//压缩
	def(fp1, fp2, Z_DEFAULT_COMPRESSION);

	//解压缩，这个2个函数要分别调用。
	inf(fp2, fp3);

        return 1;
}
