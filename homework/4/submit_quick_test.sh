#!/bin/bash

template=`cat job_script.template`

wall_time="00:03:00"
memory="50G"
n_threads=14
block_size=8192

for matrix in it-2004 sk-2005
do
    temp="${template//<+N_THREADS+>/$n_threads}"
    temp="${temp//<+MATRIX+>/$matrix}"
    temp="${temp//<+BLOCK_SIZE+>/$block_size}"
    temp="${temp//<+WALL_TIME+>/$wall_time}"
    temp="${temp//<+MEMORY+>/$memory}"
    echo "$temp" > "$matrix"_"$n_threads"_"$block_size".sb
    sbatch "$matrix"_"$n_threads"_"$block_size".sb
done
