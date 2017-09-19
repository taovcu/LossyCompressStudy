#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double average(double s[], int sz){
    double t = 0;
    for(int i=0; i< sz; i++){
        t+= s[i];
    }
    return t/sz;
}

int main(int argc, char *argv[]){
    char* origfile = argv[1]; 
    char* reducedfile = argv[2]; 
    int sz = atoi(argv[3]); 
    printf("%s, %s, %d\n", origfile, reducedfile, sz);
    printf("size of double: %ld\n", sizeof(double));
    double * ptr1 = (double *)malloc(sz * sizeof(double)) ;
    double * ptr2 = (double *)malloc(sz * sizeof(double)) ;
    double * diff = (double *)malloc(sz * sizeof(double)) ;

    FILE* stream1 = fopen(origfile, "rb");
    FILE* stream2 = fopen(reducedfile, "rb");
    //fread(ptr, sizeof(float), 6, stream);
    fread(ptr1, sizeof(double), sz, stream1);
    fread(ptr2, sizeof(double), sz, stream2);
    for(int i=0;i<500;i++){
        printf("%lf, %lf, %lf\n", ptr1[i], ptr2[i], ptr2[i] - ptr1[i]);
    }
    double rd = 0;
    double ad = 0;
    for(int i=0;i<sz;i++){
        if(ptr1[i]!=0)
            rd += fabs((ptr2[i] - ptr1[i])/ptr1[i]);
        else if(ptr2[i]!=0)
            rd += 1;  
        ad += fabs((ptr2[i] - ptr1[i]));
    }
    printf("totaldiff=%.10lf, sz=%d, average absolute error value:%.10lf\n", ad, sz, ad/sz);
    printf("totaldiff=%.10lf, sz=%d, average relative error rate:%.10lf\n", rd, sz, rd/sz);
    fclose(stream1);
    fclose(stream2);
}
