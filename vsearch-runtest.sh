#! /bin/bash

#$ -S /bin/bash
#$ -l site=hh
#$ -V
#$ -o log/qsubt.txt
#$ -e log/qsubt.txt
#$ -cwd
#$ -l h_rt=0:10:00 -l h_vmem=2000M -l h_fsize=2000M
#$ -R y
vlistlist=$1
filedir=$(sed -n ${SGE_TASK_ID}'p' < $vlistlist)
echo 'filedir: ' ${filedir}
ffname=$(basename ${filedir})
echo 'change variable list to ' $ffname
date --rfc-3339=seconds >vsearch-log/${ffname}.log
./bin/mva-train-test 7 ${ffname} ${filedir} >>vsearch-log/${ffname}.log


