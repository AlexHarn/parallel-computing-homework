#!/bin/bash
for B in 128 512 1024
do
    N=1024
    for i in {0..4}
    do
        M=1024
        for j in {0..4}
        do
            sbatch job_script.sb $N $M $B
            M=$(( M*2 ))
        done
        N=$(( N*2 ))
    done
done
