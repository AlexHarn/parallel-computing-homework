#!/bin/bash

template=`cat job_script.template`

for nodes in 1 2 3 4 5
do
    p=$(( $nodes * 28))
    temp="${template//<+NODES+>/$nodes}"
    temp="${temp//<+p+>/$p}"
    echo "$temp" > "$nodes".sb
    #sbatch "$n"_"$p".sb
done
