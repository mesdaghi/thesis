#!/bin/sh
#$ -j y
#$ -o /volatile/mesdaghi/map_align.log
#$ -wd /volatile/mesdaghi
#$ -V
#$ -N map_align
#$ -pe smp 10
#$ -S /bin/bash
#email me at the end of the job
#$ -m e
#$ -M shahram.mesdaghi@liverpool.ac.uk

num_threads=10

date_start=`date +%s`

hostname

/home/mesdaghi/progs/map_align-master/map_align -s /home/mesdaghi/tmem41b_human.a3m -c /home/mesdaghi/tmem41b_human.casp -L /home/mesdaghi/ma_list_2.txt -N 25 -T 0 -t $num_threads -O tmem41b_pdbtm. > /volatile/mesdaghi/log.txt


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
