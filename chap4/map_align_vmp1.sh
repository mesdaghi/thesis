#!/bin/sh
#$ -j y
#$ -o /volatile/mesdaghi/map_align_vmp1.log
#$ -wd /volatile/mesdaghi
#$ -V
#$ -N map_align_vmp1
#$ -pe smp 10
#$ -S /bin/bash
#$ -l  h_rt=72:00:00
#email me at the end of the job
#$ -m e
#$ -M shahram.mesdaghi@liverpool.ac.uk

num_threads=10

date_start=`date +%s`

hostname

/home/mesdaghi/progs/map_align-master/map_align -s /home/mesdaghi/vmp1_tmem49_human.a3m -c /home/mesdaghi/396159.casp -L /home/mesdaghi/ma_list_2.txt -N 25 -T 0 -t $num_threads -O vmp1_pdbtm. > /volatile/mesdaghi/vmp1_log.txt


date_end=`date +%s`
seconds=$((date_end-date_start))
minutes=$((seconds/60))
seconds=$((seconds-60*minutes))
hours=$((minutes/60))
minutes=$((minutes-60*hours))
echo =========================================================   
echo SGE job: finished   date = `date`
echo Total run time : $hours Hours $minutes Minutes $seconds Seconds
echo =========================================================   
