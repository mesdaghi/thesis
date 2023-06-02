#!/bin/bash

cd $HOME

        #Store current date and time
        date=$(/bin/date "+%F")
        date=${date//-/_}
        now=$(/bin/date "+%F\t%T")

        #Create a log file
        log_dir=$HOME/log
        log_file=$log_dir/$date\_NAS_backup.log
        rsync_stdout=$log_dir/$date\_rsync.stdout
        if ! [ -d $log_dir ]; then
                mkdir $log_dir
        fi

        #Inform the user
        echo -e "${now}\t\tbacking up from /media/shah/sdc/data to shah@NAS:" >> $log_file
        echo 'rsync -a --delete /media/shah/sdc/data shah@138.253.196.171:' >> $log_file

        #Rsync stdout is too big, let's not store it
        #rsync -a --progress --delete /home/shah/seq shah@NAS: > $rsync_stdout
        rsync -a --delete /media/shah/sdc/data shah@138.253.196.171:

        # Double-check our backup was successful
        now=$(/bin/date "+%F\t%T")
        if [ $? -ne 0 ]; then
                echo -e "${now}\t\tbackup failed" >> $log_file
        else
                echo -e "${now}\t\tbackup successful" >> $log_file
        fi

