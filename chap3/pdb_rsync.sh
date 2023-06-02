MIRRORDIR=/media/shah/sdb/db/pdb/                 		# your top level rsync directory
	LOGFILE=/media/shah/sdb/db/pdb_update.logs          # file for storing logs
	RSYNC=/usr/bin/rsync                            # location of local rsync
	SERVER=rsync.wwpdb.org::ftp                     # RCSB PDB server name
	PORT=33444                                     	# port RCSB PDB server is using
	${RSYNC} -rlpt -v -z --delete --port=$PORT ${SERVER}/data/structures/divided/pdb/ $MIRRORDIR > $LOGFILE

echo -e "${now}\t\pdb backup complete" >> /home/shah/pdb_update_log.txt
