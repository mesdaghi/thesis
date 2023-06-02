#for file in /home/shah/DaliLite.v4/vtt_db/*.pdb;
for file in /media/shah/sdb/db/pdb70/*.pdb;	
do perl -I bin ./bin/import.pl $file ${file:25:4} ./DAT_pdb70/
	
done 


