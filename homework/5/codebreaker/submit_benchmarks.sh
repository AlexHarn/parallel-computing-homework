#!/bin/bash

template=`cat benchmark.sb.template`

for version in sequential block cyclic
do
    temp="${template//<+VERSION+>/$version}"
    echo "$temp" > "$version"_benchmark.sb
    sbatch "$version"_benchmark.sb
done
