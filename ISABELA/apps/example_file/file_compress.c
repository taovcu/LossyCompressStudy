/*
 * Author: Eric R. Schendel <erschend AT ncsu.edu>
 */

#include "isabela.h"

#include <string.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <zlib.h>
#include <zconf.h>


void print_usage_error_exit (const char *_err_msg)
{
    printf ("ERROR: %s!\n", _err_msg);
    printf ("\n");

    printf ("Program Usage Arguments: ");
    printf ("<input file> <output file> <element size> <relative error rate>\n");

    printf ("  <input file>  : name of input file\n");
    printf ("  <output file> : name of output file\n");
    printf ("  <element size>: element segment size in bytes (ie, 8 for double, 4 for float)\n");
    printf ("  <relative error rate>: err rate value (ie, 1 for 0.01)\n");

    exit (-1);
}

void read_file (char *file_name, void *input_buffer, size_t input_buffer_size)
{
    FILE* in_file = fopen (file_name, "rb");

    if (in_file == NULL)
        print_usage_error_exit ("unable to open input file");

    if (fread (input_buffer, 1, input_buffer_size, in_file) != input_buffer_size)
        print_usage_error_exit ("unable to read input file completely");

    fclose (in_file);
}

void write_file (char *file_name, void *output_buffer, size_t output_buffer_size)
{
    FILE* out_file = fopen (file_name, "wb");

    if (out_file == NULL)
        print_usage_error_exit ("unable to open output file");

    if (fwrite (output_buffer, 1, output_buffer_size, out_file) != output_buffer_size)
        print_usage_error_exit ("unable to write output file completely");

    fclose (out_file);
}

int main (int argc, char** argv)
{
    struct stat stat_info;
    size_t file_size;
    int element_bytes;
    float err_bound;
    char *in_buffer;
    char *in_buffer_copy;
    char *out_buffer;
    char *in_ptr;
    char *out_ptr;

    enum ISABELA_status status;
    struct isabela_stream i_strm;
    struct isabela_config config;

    /*time statistics */
    struct timeval start, end;
    float delta;


    if (argc != 5)
        print_usage_error_exit ("missing program arguments");

    if (sscanf (argv[3], "%d", &element_bytes) != 1)
        print_usage_error_exit ("invalid input for element byte size");
    if (sscanf (argv[4], "%f", &err_bound) != 1)
        print_usage_error_exit ("invalid input for element byte size");

    //printf ("Input File  : %s\n", argv[1]);
    //printf ("Output File : %s\n", argv[2]);
    //printf ("Element Size: %d\n", element_bytes);
    //printf ("relative err rate: %f\n", err_bound);

    // Compress 1024 elements at a time
    config.window_size = 1024;
//    config.window_size = 10240;

    // Approximate each window with 30 coefficients
    config.ncoefficients = 30;
//    config.ncoefficients = 10;

    // Relative error between approximate and original values should be
    // no more than 5%
    config.error_rate = err_bound;

    // Size of each element
    config.element_byte_size = element_bytes;

    // Use either BSplines or Wavelets.
    config.transform = ISABELA_BSPLINES;
    // config.transform = ISABELA_WAVELETS;

#if COMPRESS
    if (stat (argv[1], &stat_info)) {
        printf ("[%s: %d] Unable to read input file %s", __FUNCTION__, __LINE__, argv [1]);
        print_usage_error_exit ("unable to read ISABELA file");
    }

    file_size = (size_t) stat_info.st_size;

    // Input buffer
    in_buffer = (char*) malloc (file_size);

    // Setting output buffer with file_size
    out_buffer = (char*) malloc (file_size);
    assert (in_buffer != NULL && out_buffer != NULL);

    // Read file
    //printf ("Elements    : %ld\n", file_size/element_bytes);
    read_file (argv[1], in_buffer, file_size);

    // Setup compression (deflate) with isabela_config
    status = isabelaDeflateInit (&i_strm, element_bytes, &config);
    assert (status == ISABELA_SUCCESS);

    i_strm.next_in = (void*) in_buffer;
    i_strm.avail_in = file_size;

    i_strm.next_out = (void*) out_buffer;

    gettimeofday(&start, 0);
    // Perform compression
    status = isabelaDeflate (&i_strm, ISABELA_FINISH);
    gettimeofday(&end, 0);

    delta = (end.tv_sec - start.tv_sec) * 1000 + (end.tv_usec - start.tv_usec) / 1000.0;
    printf("Compression time: %f ms\n", delta);

    assert (status == ISABELA_SUCCESS);

    printf ("\n");

    //printf ("%d bytes written out\n", i_strm.avail_out);
    write_file(argv[2], out_buffer, i_strm.avail_out);

    // Cleanup
    status = isabelaDeflateEnd (&i_strm);
    assert (status == ISABELA_SUCCESS);
#else
    if (stat (argv[1], &stat_info)) {
        printf ("[%s: %d] Unable to read input file %s", __FUNCTION__, __LINE__, argv [1]);
        print_usage_error_exit ("unable to read ISABELA file");
    }

    file_size = (size_t) stat_info.st_size;

    // Input buffer
    in_buffer = (char*) malloc (file_size);

    // Being cautious and setting output buffer to 8 x compressed_file_size 
    out_buffer = (char*) malloc (8 * file_size);
    assert (in_buffer != NULL && out_buffer != NULL);

    // Read file
    read_file (argv[1], in_buffer, file_size);

    // Setup deflation
    status = isabelaInflateInit (&i_strm, element_bytes, &config);
    assert (status == ISABELA_SUCCESS);

    // Setting up input / output buffers
    i_strm.next_in = (void*) in_buffer;
    i_strm.avail_in = file_size;

    i_strm.next_out = (void*) out_buffer;
 
    //decompress 
    gettimeofday(&start, 0);
    // Perform compression
    status = isabelaInflate (&i_strm, ISABELA_FINISH);
    gettimeofday(&end, 0);

    delta = (end.tv_sec - start.tv_sec) * 1000 + (end.tv_usec - start.tv_usec) / 1000.0;
    printf("Decompression time: %f ms\n", delta);
    assert (status == ISABELA_SUCCESS);

    printf ("\n");
    //printf ("%d bytes written out\n", i_strm.avail_out);
    write_file (argv[2], out_buffer, i_strm.avail_out);

    status = isabelaInflateEnd (&i_strm);
    assert (status == ISABELA_SUCCESS);
#endif

    free (out_buffer);
    free (in_buffer);

    return 0;
}
