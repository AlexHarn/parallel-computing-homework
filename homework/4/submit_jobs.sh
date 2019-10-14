#!/bin/bash

template=`cat job_script.template`

#matrix=it-2004
#n_threads=4
#block_size=2048
wall_time="00:10:00"
memory="100G"

#temp="${template//<+N_THREADS+>/$n_threads}"
#temp="${temp//<+MATRIX+>/$matrix}"
#temp="${temp//<+WALL_TIME+>/$wall_time}"
#temp="${temp//<+MEMORY+>/$memory}"
#temp="${temp//<+BLOCK_SIZE+>/$block_size}"
#echo "$temp" > "$matrix"_"$n_threads"_"$block_size".sb
#sbatch "$matrix"_"$n_threads"_"$block_size".sb
for matrix in it-2004 twitter7 sk-2005
do
    for n_threads in 1 2 4 8 14 28
    do
        for block_size in 2048 8192 32768
        do
            if [ $block_size == 2048 ] && [ $matrix == twitter7 ]
            then
                continue
            fi
            temp="${template//<+N_THREADS+>/$n_threads}"
            temp="${temp//<+MATRIX+>/$matrix}"
            temp="${temp//<+BLOCK_SIZE+>/$block_size}"
            temp="${temp//<+WALL_TIME+>/$wall_time}"
            temp="${temp//<+MEMORY+>/$memory}"
            echo "$temp" > "$matrix"_"$n_threads"_"$block_size".sb
            sbatch "$matrix"_"$n_threads"_"$block_size".sb
        done
    done
done

wall_time="00:30:00"
memory="150G"
matrix=twitter7
block_size=2048
for n_threads in 1 2 4 8 14 28
do
    temp="${template//<+N_THREADS+>/$n_threads}"
    temp="${temp//<+MATRIX+>/$matrix}"
    temp="${temp//<+BLOCK_SIZE+>/$block_size}"
    temp="${temp//<+WALL_TIME+>/$wall_time}"
    temp="${temp//<+MEMORY+>/$memory}"
    echo "$temp" > "$matrix"_"$n_threads"_"$block_size".sb
    sbatch "$matrix"_"$n_threads"_"$block_size".sb
done
