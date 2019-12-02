#!/bin/bash

template=`cat job_script.template`

wall_time="00:05:00"
memory="100G"

for p in {14..140..14}
do
    nodes=$(( ($p + 14)/28 ))
    for n in 100000000 500000000 2000000000
    do
        temp="${template//<+P+>/$p}"
        temp="${temp//<+NODES+>/$nodes}"
        temp="${temp//<+N+>/$n}"
        temp="${temp//<+WALL_TIME+>/$wall_time}"
        temp="${temp//<+MEMORY+>/$memory}"
        echo "$temp" > "$p"_"$n".sb
        sbatch "$p"_"$n".sb
    done
done
