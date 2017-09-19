List="dpot astro fish sedov-pres blast2-pres eddy_velx_f4 yf17_pres yf17_temp bump_dense"
set -- $List

for i
do
    echo $i
    python sample.py -s prefix -i $i.dat
    python sample.py -s interval -r point -i $i.dat 
    python sample.py -s interval -r block -i $i.dat
    python sample.py -s interval -r chunk -i $i.dat
    python sample.py -s random -r point -i $i.dat 
    python sample.py -s random -r block -i $i.dat
    python sample.py -s random -r chunk -i $i.dat
    #python sample.py -s reconstruct -c uniform -n 200 -i reconstruct/$i.dist
done

