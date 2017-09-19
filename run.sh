#!/bin/bash

#zfp parameters
#exp_a=0.000002
#exp_a=0.001
#exp_a=0.01
exp_a=0.00001
a=0.001
f=1

#fpc parameters
fpce=20 

#sz parameters
cfg="sz.config"

#isabela parameters
exp_e=0.0000576
e=0.000118

loop=20

usage() { echo "Usage: $0 [-c <zfp|fpc|sz|isb>] [-i <inputfile>] [-t <outputfile>]" 1>&2; exit 1; }


zfpaction(){
    inputFILESIZE=$(stat -c%s "$i")
    e=`expr $inputFILESIZE / 8`
    zfp/examples/zfp -a $a -d -$f $e -i $i -z $t
    outputFILESIZE=$(stat -c%s "$t")
    zfp/examples/zfp -a $a -d -$f $e -z $t -o $t.out
    #echo $inputFILESIZE
    #echo $outputFILESIZE
    echo 'current a value'
    echo $a
    echo "$inputFILESIZE $outputFILESIZE" | awk '{printf "zfp compression ratio, %.2f \n", $1/$2}'
}

isbaction(){
    inputFILESIZE=$(stat -c%s "$i")
    isbe=`expr $inputFILESIZE / 8`
    ISABELA/apps/example_file/file_compress $i $t 8 $e
    outputFILESIZE=$(stat -c%s "$t")
    ISABELA/apps/example_file/file_decompress $t $t.out 8 $e
    #echo $inputFILESIZE
    #echo $outputFILESIZE
    echo 'current e value'
    echo $e
    echo "$inputFILESIZE $outputFILESIZE" | awk '{printf "isb compression ratio, %.2f \n", $1/$2}'
}

runisb(){
    isbaction 
    out=`./compareData $i $t.out $isbe`
    err=$(echo $out | awk -F"average absolute error value:" '{sub(/ .*/,"",$2);print $2}')
    echo "absolute err: "$err
    err=$(echo $out | awk -F"average relative error rate:" '{sub(/ .*/,"",$2);print $2}')
    echo $err
    c=$(echo $err $exp_e | awk '{ printf "%d", ( $1 > 1.2 * $2 ) ? 1 : (($1 < 0.8 * $2) ? -1 : 0) }')
    x=1
    while [ "$c" != 0 ] && [ $x -le $loop ]
    do
        if [ "$c" -eq  1 ] ; then
            e=$(echo $e | awk '{printf "%10.10f", $1 * 0.7}') 
        elif [ "$c" -eq -1 ] ; then
            e=$(echo $e | awk '{printf "%10.10f", 100 <= ( $1 * 1.3 ) ? 100 : ( $1 * 1.3 ) }') 
        fi
        echo "tried $x times"
        (( x++ ))
        isbaction 
        out=`./compareData $i $t.out $isbe`
        err=$(echo $out | awk -F"average absolute error value:" '{sub(/ .*/,"",$2);print $2}')
        echo "absolute err: "$err
        err=$(echo $out | awk -F"average relative error rate:" '{sub(/ .*/,"",$2);print $2}')
        echo $err
        c=$(echo $err $exp_e | awk '{ printf "%d", ( $1 > 1.2 * $2 ) ? 1 : (($1 < 0.8 * $2) ? -1 : 0) }')
    done
    ./compareData $i $t.out $isbe
}

runzfp(){
    zfpaction 
    out=`./compareData $i $t.out $e`
    echo $out
    err=$(echo $out | awk -F"average absolute error value:" '{sub(/ .*/,"",$2);print $2}')
    echo "absolute err: "$err
    err=$(echo $out | awk -F"average relative error rate:" '{sub(/ .*/,"",$2);print $2}')
    echo $err
    c=$(echo $err $exp_a | awk '{ printf "%d", ( $1 > 1.2 * $2 ) ? 1 : (($1 < 0.8 * $2) ? -1 : 0) }')
    x=1
    while [ "$c" != 0 ] && [ $x -le $loop ]
    do
        if [ "$c" -eq  1 ] ; then
            a=$(echo $a | awk '{printf "%10.10f", $1 * 0.7}') 
        elif [ "$c" -eq -1 ] ; then
            a=$(echo $a | awk '{printf "%10.10f", $1 * 1.3}') 
        fi
        echo "tried $x times"
        (( x++ ))
        zfpaction 
        out=`./compareData $i $t.out $e`
        err=$(echo $out | awk -F"average absolute error value:" '{sub(/ .*/,"",$2);print $2}')
        echo "absolute err: "$err
        err=$(echo $out | awk -F"average relative error rate:" '{sub(/ .*/,"",$2);print $2}')
        echo "relative err: "$err
        c=$(echo $err $exp_a | awk '{ printf "%d", ( $1 > 1.2 * $2 ) ? 1 : (($1 < 0.8 * $2) ? -1 : 0) }')
    done
    ./compareData $i $t.out $e
}

runfpc(){
    fpc/fpc ${fpce} < $i > $t
    inputFILESIZE=$(stat -c%s "$i")
    e=`expr $inputFILESIZE / 8`
    outputFILESIZE=$(stat -c%s "$t")
    echo $inputFILESIZE
    echo $outputFILESIZE
    echo "$inputFILESIZE $outputFILESIZE" | awk '{printf "fpc compression ratio, %.2f \n", $1/$2}'
    fpc/fpc < $t > $t.out
    cat FPC.log
    ./compareData $i $t.out $e
}

rungzip(){
    rm $i.gz
    gzip-1.6/gzip -k $i
    inputFILESIZE=$(stat -c%s "$i")
    e=`expr $inputFILESIZE / 8`
    outputFILESIZE=$(stat -c%s "$i.gz")
    echo $inputFILESIZE
    echo $outputFILESIZE
    echo "$inputFILESIZE $outputFILESIZE" | awk '{printf "gzip compression ratio, %.2f \n", $1/$2}'
    rm $i
    gzip-1.6/gzip -d $i.gz
}


runsz(){
    inputFILESIZE=$(stat -c%s "$i")
    sze=`expr $inputFILESIZE / 8`
    SZ/example/testdouble_compress ${cfg} $i $sze 
    outputFILESIZE=$(stat -c%s "$i.sz")
    echo $inputFILESIZE
    echo $outputFILESIZE
    echo "$inputFILESIZE $outputFILESIZE" | awk '{printf "sz compression ratio, %.2f \n", $1/$2}'
    SZ/example/testdouble_decompress ${cfg} $i.sz $sze
    ./compareData $i $i.sz.out $sze
}

while getopts ":c:i:t:" o; do
    case "${o}" in
        c)
            c=${OPTARG}
            ((c == "zfp" || c == "fpc" || c == "sz")) || usage
            ;;
        i)
            i=${OPTARG}
            ;;
        t)
            t=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${c}" ] || [ -z "${i}" ] ; then
    usage
fi

if [ "$c" == "zfp" ]
then
    runzfp
elif [ "$c" == "isb" ]
then
    runisb
elif [ "$c" == "gzip" ]
then
    rungzip
elif [ "$c" == "fpc" ]
then
    runfpc
elif [ "$c" == "sz" ]
then
    runsz
fi
