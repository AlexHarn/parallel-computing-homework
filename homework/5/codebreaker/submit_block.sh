#!/bin/bash

template=`cat block.template`

for key in 3988183917 4294967273 306783377
do
    for p in 8 12 14 16 22 28
    do
        temp="${template//<+key+>/$key}"
        temp="${temp//<+p+>/$p}"
        echo "$temp" > block_"$key"_"$p".sb
        sbatch block_"$key"_"$p".sb
    done
done
