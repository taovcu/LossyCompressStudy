#A study of lossy compression schemes

##By Tao Lu

Scientific simulations generate large sums of floating-point data, which are hardly compressible using traditional data reduction methods such as deduplication and lossless compression. The emerging lossy floating-point data compression is promising to satisfy the data reduction demand of HPC systems. However, lossy compression has not been widely adopted in HPC production systems. We believe one main reason is that there lacks comprehensive evaluation of the benefits and pitfalls of conducting lossy compression on scientific data.

To expedite the landing of lossy compression on HPC production platforms, we conduct extensive evaluation on state-of-the-art lossy compression schemes, including ZFP, ISABELA, and SZ, using real and representative HPC datasets. Our eval- uation reveals the crushing influences of compressor design on compression performance. We also uncover the impact of high compression ratio on data analytics. Our evaluation provides domain scientists a good understanding of what to expect from lossy compression. Moreover, we propose compressor-aware sampling methods and build compression ratio estimation model to accurately estimate compression ratio. Considering compression consumes computation resources and not all datasets are highly compressible, the proposed compression ratio estimation mechanisms can help domain scientists or data management middleware make “compress or not” decisions.


1. Run the code  

./run.sh -c gzip -i testdouble\_8\_8\_128.zfp

./run.sh -c fpc -i fpc/testdouble\_8\_8\_128.dat -t file.fpc

./run.sh -c zfp -i fpc/testdouble\_8\_8\_128.dat -t testdouble\_8\_8\_128.zfp

./run.sh -c sz -i testdouble\_8\_8\_128.dat

./run.sh -c isb -i fpc/testdouble\_8\_8\_128.dat -t testdouble\_8\_8\_128.isb


##Note, please cite our IPDPS'18 paper if you use any material in this repository. 

Tao Lu, Qing Liu, Xubin He, Huizhang Luo, Eric Suchyta, Norbert Podhorszki, Scott Klasky, Matthew Wolf and Tong Liu, Understanding and Modeling Lossy Compression Schemes on HPC Scientific Data, IEEE International Parallel & Distributed Processing Symposium (IPDPS), 2018.
