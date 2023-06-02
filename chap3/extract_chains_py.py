import sys
import os
from pypdb import PDBFile

my_file=str(sys.argv[1])
my_pdbID=os.path.basename(my_file)[:-4]
out_folder=str(sys.argv[2])

with open(my_file,"r") as my_handle:
    mypdb=PDBFile(my_pdbID,my_handle)
my_handle.close()

for chain in mypdb.CHAINS:
    chain_file_out=out_folder+"/"+my_pdbID+"_"+chain+".pdb"
    mypdb.CHAINS[chain].write_file(outfile_path=chain_file_out)