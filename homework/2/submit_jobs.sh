#!/bin/bash
#for B in 128 512 1024
#do
    #N=8192
    #for i in {0..5}
    #do
        #M=8192
        #for j in {0..5}
        #do
            #sbatch job_script.sb $N $M $B
            #M=$(( M*2 ))
        #done
        #N=$(( N*2 ))
    #done
#done


#M=10000
#N=10000
#M=100000
#N=200
#M=200
#N=100000
#B=2
#for i in {250..512}
#do
    #sbatch job_script.sb $N $M $i
    ##B=$(( B*2 ))
#done

#B=200
#for N in {1000..10000..100}
#do
    #sbatch job_script.sb $N $N $B
#done

#B=200
#N=10000
#for M in {100..10000..100}
#do
    #sbatch job_script.sb $N $M $B
#done
