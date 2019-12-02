#!/bin/bash

template=`cat job_script.template`

wall_time="00:05:00"
memory="100G"

p=$1
n=$2

nodes=$(( ($p + 14)/28 ))
temp="${template//<+P+>/$p}"
temp="${temp//<+NODES+>/$nodes}"
temp="${temp//<+N+>/$n}"
temp="${temp//<+WALL_TIME+>/$wall_time}"
temp="${temp//<+MEMORY+>/$memory}"
echo "$temp" > "$p"_"$n".sb
sbatch "$p"_"$n".sb
