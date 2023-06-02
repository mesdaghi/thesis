#!/bin/bash

isConnected() {
        if [ -f "$1"/connected ];
        then
                return 1;
        else
                now=$(/bin/date "+%F\t%T");
                /bin/echo -e "${now}\t'$1' not connected";
                return 0;
        fi
}

backupDiskFromTo() {
        now=$(/bin/date "+%F\t%T")
        /bin/echo -e "${now}\t\tbacking up from '$1' to '$2'"
        /usr/bin/rsync -aAX --exclude "lost+found" --exclude "chaindata" --exclude ".cache" --delete "$1" "$2"

        # Double-check our backup was successful
        if [ $? -ne 0 ]; then
                now=$(/bin/date "+%F\t%T")
                /bin/echo -e "${now}\t\tbackup failed"
                exit
        fi

        now=$(/bin/date "+%F\t%T")
        /bin/echo -e "${now}\t\tbackup successful"
}


# Check if we have a connected /media/seagate drive
isConnected /media/shah/backup

seagateIsConnected=$?

# Backup /home to /media/shah/Elements
if [ $seagateIsConnected -eq 1 ]; then
        backupDiskFromTo /mnt/ad48ca2d-e154-485e-aa6b-5e7277f70d4e/data /media/shah/backup/data
fi
