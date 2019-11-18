#!/bin/bash

template=`cat job_script.template`

for n in 1000 100000 10000000
do
    for p in 2 3 6 11 21 101 251
    do
        temp="${template//<+n+>/$n}"
        temp="${temp//<+p+>/$p}"
        echo "$temp" > "$n"_"$p".sb
        sbatch "$n"_"$p".sb
    done
done
