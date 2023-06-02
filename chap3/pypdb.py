'''
Tools to load PDB file into data structures, and more importantly extract fragments. Hierarchy: File > Molecule > Chain
'''

# Import dependencies
import re

'''
Create function to translate amino acid sequences from three letter code to one letter code
Input: list [str]
Output: list [str]
'''

def translate_3to1_AA(sequence):
    d = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
         'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
         'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
         'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
    result=[]
    for residue in sequence:
        try:
            result.append(d[residue])
        except KeyError:
            result.append("X")
    return result

'''
Create function to translate amino acid sequences from one letter code to three letter code
Input: list [str]
Output: list [str]
'''

def translate_1to3_AA(sequence):
    d={'A': 'ALA', 'C': 'CYS', 'D': 'ASP', 'E': 'GLU', 'F': 'PHE',
       'G': 'GLY', 'H': 'HIS', 'I': 'ILE', 'K': 'LYS', 'L': 'LEU',
        'M': 'MET', 'N': 'ASN', 'P': 'PRO', 'Q': 'GLN', 'R': 'ARG',
        'S': 'SER', 'T': 'THR', 'V': 'VAL', 'W': 'TRP', 'Y': 'TYR'}
    result=[]
    for residue in sequence:
        try:
            result.append(d[residue])
        except KeyError:
            result.append("XXX")
    return result


'''
Class to store PDB header record (classification, date, id code)
'''

class PDBHeader:
    #Constructor function
    def __init__(self, file_header):
        #Load each attirbute
        self.classification=file_header[10:50]
        self.date=file_header[50:59]
        self.idcode=file_header[62:66]

'''
Class to store PDB tittle record (experiment title)
'''

class PDBTitle:
    #Constructor function
    def __init__(self, file_title):
        self.experiment_title = file_title[0][10:80].lstrip().rstrip()
        for title_continuation in file_title[1:]:
            self.experiment_title=self.experiment_title+" "+title_continuation[10:80].lstrip().rstrip()
        self.experiment_title=self.experiment_title.lstrip().rstrip()

'''
Class to store PDB caveat record (warning, reason)
'''

class PDBCaveat:
    #Constructor function
    def __init__(self, file_caveat):
        if(file_caveat==[]):
            self.warning=False
        else:
            self.warning=True
            self.reason=""
            for caveat in file_caveat:
                self.reason = self.reason + caveat[19:79]
            self.reason = self.reason.rstrip()

'''
Class to store PDB conect record (atom_serialnumber=[str])
'''

class PDBConect:
    #Constructor function
    def __init__(self, myconnect):
        myconnect=myconnect.split().rstrip()
        self.atom_serialnumbers=myconnect[1:]



'''
Class to store PDB keyword record (list of keywords)
Metohds: keyword_lookup
'''

class PDBKeywords:
    #Constructor function
    def __init__(self, file_keywords):
        self.keywrdlist = file_keywords[0][10:79].lstrip().rstrip().split(", ")
        for list_continuation in file_keywords[1:]:
            self.keywrdlist+=list_continuation[10:79].lstrip().rstrip().split(", ")
    #Check out if a given keyword is on the file
    def keyword_lookup(self,keyword):
        if(keyword in self.keywrdlist):
            return True
        else:
            return False

'''
Class to store PDB experimental data record (list of techniques)
Metohds: expdata_lookup
'''

class PDBExpdata:
    #Constructor function
    def __init__(self, file_expdata):
        self.expdtalist = file_expdata[0][10:79].lstrip().rstrip().split("; ")
        for list_continuation in file_expdata[1:]:
            self.expdtalist+=list_continuation[10:79].lstrip().rstrip().split("; ")
    #Check if a given exp is on the file
    def exp_lookup(self,keyword):
        if(keyword in self.expdtalist):
            return True
        else:
            return False

'''
Class to store PDB missing residues (chain, model, residue, index)
'''

class MissingResidue:
    #Constructor function
    def __init__(self, missing_residue):
        self.chain=missing_residue[19:20]
        self.model=missing_residue[13]
        if(self.model==" "):
            self.model="NA"
        self.residue=missing_residue[15:18]
        self.index=missing_residue[23:27]

'''
Class to store PDB related entry (database, ID)
'''

class RelatedEntry:
    #Constructor function
    def __init__(self, entry):
        self.database=re.search('RELATED DB: (.*)', entry).group(1).rstrip().lstrip()
        self.ID=re.search('RELATED ID: (.*) RELATED DB: ', entry).group(1).rstrip().lstrip()

'''
Class to store PDB remarks (list of missing residues, list of related entries, version, space group,resolution)
Metohds: get_missing_residues
'''

class PDBRemark:
    #Constructor function
    def __init__(self, file_remark):
        self.missing_residues_list = []
        self.related_entries_list = []
        for remark in file_remark:
            remark_category=remark[7:10].lstrip().rstrip()
            remark=remark.rstrip()
            if(remark_category=="2" and remark[10:]!=""):
                self.resolution=remark[23:30].lstrip().rstrip()
            elif(remark_category=="4" and remark[10:]!=""):
                self.version=re.search('COMPLIES WITH FORMAT (.*),', remark).group(1)
            elif(remark_category=="290" and remark[10:]!=""):
                if("SPACE GROUP" in remark):
                    self.spacegroup=re.search('SPACE GROUP: (.*)', remark).group(1).lstrip().rstrip()
            elif(remark_category=="465" and remark[14]==" "  and remark[15:18]!="RES"):
                self.missing_residues_list.append(MissingResidue(remark))
            elif(remark_category=="900" and "RELATED ID:" in remark):
                self.related_entries_list.append(RelatedEntry(remark))

    #Get missing residues in a given chain
    def get_missing_residues(self,chain=False,model=False):
        result=[]
        #If the user specified a chain and a model
        if (chain and model):
            for missing_residue in self.missing_residues_list:
                if missing_residue.chain==chain and missing_residue.model==model:
                    result.append(missing_residue)
        #If the user specified only a chain
        elif (chain):
            for missing_residue in self.missing_residues_list:
                if missing_residue.chain==chain:
                    result.append(missing_residue)
        #If the user specified only a model
        elif (model):
            for missing_residue in self.missing_residues_list:
                if missing_residue.model==model:
                    result.append(missing_residue)
        #Otherwise return everything
        else:
            for missing_residue in self.missing_residues_list:
                result.append(missing_residue)
        return result



#Define HELIX class
class PDBHelix:
    def __init__(self,singlelineHELIX):
        self.serialnumber=singlelineHELIX[7:10].lstrip().rstrip()
        self.helix_id=singlelineHELIX[11:14].lstrip().rstrip()
        self.start_residue_name=singlelineHELIX[15:18].lstrip().rstrip()
        self.start_residue_chain=singlelineHELIX[19].lstrip().rstrip()
        self.start_residue_seqnumber=singlelineHELIX[21:25].lstrip().rstrip()
        self.stop_residue_name=singlelineHELIX[27:30].lstrip().rstrip()
        self.stop_residue_chain=singlelineHELIX[31].lstrip().rstrip()
        self.stop_residue_seqnumber=singlelineHELIX[33:37].lstrip().rstrip()
        self.length=singlelineHELIX[71:76].lstrip().rstrip()


#Define ATOM class
class PDBAtom:
    def __init__(self,myATOM):
        #Check whether it is an aotm or it is ansiou factor
        if("ATOM" in myATOM[:6] or "HETATM" in myATOM[:6]):
            self.isANISOU=False
            if("ATOM" in myATOM[:6]):
                self.isATOM = True
                self.isHETATM = False
            else:
                self.isATOM = False
                self.isHETATM = True
            self.xcoord = myATOM[30:38].lstrip().rstrip()
            self.ycoord = myATOM[38:46].lstrip().rstrip()
            self.zcoord = myATOM[46:54].lstrip().rstrip()
            self.occupancy = myATOM[54:60].lstrip().rstrip()
            self.tempFactor = myATOM[60:66].lstrip().rstrip()
        elif("ANISOU" in myATOM[:6]):
            self.isATOM=False
            self.isANISOU=True
            self.isHETATM=False
            self.factor_1_1=myATOM[28:35]
            self.factor_2_2=myATOM[35:42]
            self.factor_3_3=myATOM[42:49]
            self.factor_1_2=myATOM[49:56]
            self.factor_1_3=myATOM[56:63]
            self.factor_2_3=myATOM[63:70]
        else:
            print("WARNING: Atom format not recognised!\n"+myATOM)

        #Load ATOM/ANISOU shared fields
        self.atom_serialnumber=myATOM[6:11].lstrip().rstrip()
        self.atom_name=myATOM[12:16]
        self.atom_altLoc=myATOM[16]
        self.residue=myATOM[17:20]
        self.chain=myATOM[21].lstrip().rstrip()
        self.residue_seqnumber=myATOM[22:26].lstrip().rstrip()
        self.chem_element=myATOM[76:78].lstrip().rstrip()
        self.charge=myATOM[78:80].lstrip().rstrip()
        if(self.atom_name.lstrip().rstrip()=="CA"):
            self.isCA=True
        else:
            self.isCA=False
        if(self.atom_altLoc!=" " and self.atom_altLoc!="A"):
            self.isAltLoc = True
        else:
            self.isAltLoc = False

    #Create function to return a PDB formated line
    def get_PDBLine(self):
        #If it is an atom
        if(self.isATOM or self.isHETATM):
            if(self.isATOM):
                # Initiate string
                result = "ATOM  "
            else:
                # Initiate string
                result = "HETATM"
            #Append the serial number, atom name, altloc, residue and chain
            result+=(" "*(5-len(str(self.atom_serialnumber)))+str(self.atom_serialnumber)+" "+ self.atom_name + self.atom_altLoc + self.residue + " "+ self.chain)
            # Append the residue sequence number
            result += (" " * (4 - len(str(self.residue_seqnumber))) + str(self.residue_seqnumber) + "    ")
            #Append xcoord ycoord and zcoord
            result += (" " * (8 - len(str(self.xcoord))) + str(self.xcoord))
            result += (" " * (8 - len(str(self.ycoord))) + str(self.ycoord))
            result += (" " * (8 - len(str(self.zcoord))) + str(self.zcoord))
            #Append occupancy and tempfactor
            result += (" " * (6 - len(str(self.occupancy))) + str(self.occupancy))
            result += (" " * (6 - len(str(self.tempFactor))) + str(self.tempFactor)+ " "*10)
            #Append chem elemeent and charge
            result += (" " * (2 - len(str(self.chem_element))) + str(self.chem_element))
            result += (" " * (2 - len(str(self.charge))) + str(self.charge))
            #Return the result
            return result
        #Otherwise it must be ANISOU
        else:
            #Initiate string
            result="ANISOU"
            #Append the serial number, atom name, altloc, residue and chain
            result+=(" "*(5-len(str(self.atom_serialnumber)))+str(self.atom_serialnumber)+" "+ self.atom_name + self.atom_altLoc + self.residue + " "+ self.chain)
            # Append the residue sequence number
            result += (" " * (4 - len(str(self.residue_seqnumber))) + str(self.residue_seqnumber))
            #Append xcoord ycoord and zcoord
            result += ("  " + self.factor_1_1 + self.factor_2_2 + self.factor_3_3 + self.factor_1_2 + self.factor_1_3 + self.factor_2_3 + "      ")
            #Append chem elemeent and charge
            result += (" " * (2 - len(str(self.chem_element))) + str(self.chem_element))
            result += (" " * (2 - len(str(self.charge))) + str(self.charge))
            #Return the result
            return result


#Define a fragment class
class PDBFragment:
    def __init__(self, PDB_ID, FRAGMENT_ID, CHAIN_ID=None, OneSequence=None, ThreeSequence=None, Helices=None, Atoms=None, MissingResidues=None, Cryst1=None, Scale=None,Origx=None):
        #MISCELLANEOUS
        self.PDB_ID=PDB_ID
        self.FRAGMENT_ID=FRAGMENT_ID
        self.CHAIN_ID=CHAIN_ID
        self.OneLetterSequence=OneSequence
        self.ThreeLetterSequence=ThreeSequence
        self.Cryst1=Cryst1
        self.Scale=Scale
        self.Origx=Origx
        #Helix
        self.Helices=Helices
        #Atom
        self.Atoms=Atoms
        #MissingResidues
        self.MissingResidues=MissingResidues

    # Create a function to renumber the atom sequence number or serial number
    def renumber_residues(self,seqnumber=True,serialnumber=True,start=1,inplace=True):
        #If we want to modify the object itself
        if(inplace):
            if(seqnumber and serialnumber):
                residue_count=-1
                prev_residue_seqnumber=0
                helices_start=[]
                helices_stop=[]
                anisou_dict={}  #{oldindex:newindex}
                #Store helix start and stops
                for helix in self.Helices:
                    helices_start.append(helix.start_residue_seqnumber)
                    helices_stop.append(helix.stop_residue_seqnumber)
                #Loop through the atoms
                for index,atom in enumerate(self.Atoms):
                    if(atom.isANISOU):
                        # Load the new serial number corresponding with its ATOM
                        atom.atom_serialnumber = anisou_dict[atom.atom_serialnumber]
                    else:
                        # Store the new serial number for anisou entries
                        anisou_dict[atom.atom_serialnumber] = str(start + index)
                        # New serial number
                        atom.atom_serialnumber = str(start + index)
                    #New sequence number
                    if(atom.residue_seqnumber!=prev_residue_seqnumber):
                        residue_count+=1
                        prev_residue_seqnumber = atom.residue_seqnumber
                        #Change helix indexes if necessary
                        if(atom.residue_seqnumber in helices_start):
                            for helix in self.Helices:
                                if (atom.residue_seqnumber==helix.start_residue_seqnumber):
                                    helix.start_residue_seqnumber=str(start + residue_count)
                                    break
                        if(atom.residue_seqnumber in helices_stop):
                            for helix in self.Helices:
                                if (atom.residue_seqnumber == helix.stop_residue_seqnumber):
                                    helix.stop_residue_seqnumber = str(start + residue_count)
                                    break
                        #Change the atom sequence number
                        atom.residue_seqnumber = str(start + residue_count)
                    #Same residue as before
                    else:
                        atom.residue_seqnumber=str(start+residue_count)
        #Otherwise it is necessary to create a new PDBChain object and return it
        else:
            print("Not supported yet")
    #Create a function to return a PDB file with the contents of the fragment
    def write_file(self,outfile_path):
        try:
            with open(outfile_path,"w") as outfile_handle:
                outfile_handle.write("REMARK   Fragment generated through pdb_tools\nREMARK   Original PDB model "+self.PDB_ID+":"+self.CHAIN_ID+"\nREMARK   Fragment ID: "+self.FRAGMENT_ID+"\n")
                SEQRES_lines=[self.ThreeLetterSequence[x:x + 13] for x in range(0, len(self.ThreeLetterSequence), 13)]
                for index,line in enumerate(SEQRES_lines):
                    seqres_record="SEQRES "+ (" " * (3 - len(str(index))) + str(index) + " " + self.CHAIN_ID + " ") + (" " * (4 - len(str(len(self.ThreeLetterSequence)))) + str(len(self.ThreeLetterSequence)) + "  " ) + " ".join(line)
                    outfile_handle.write(seqres_record+"\n")
                outfile_handle.write("  ".join(self.Cryst1))
                outfile_handle.write("".join(self.Origx))
                outfile_handle.write("".join(self.Scale))
                for atom in self.Atoms:
                    outfile_handle.write(atom.get_PDBLine()+"\n")
            outfile_handle.close()
        except FileNotFoundError:
            print("Impossible to create output file!")

    #Create a method to return a polyALA file
    def get_polyALA(self,inplace=True):
        #The user wants to modify current chain to be a polyALA
        if(inplace):
            atoms_to_keep=[]
            for index,atom in enumerate(self.Atoms):
                #If the atom is not a CA, N or O, delete it
                if(atom.atom_name.rstrip().lstrip()=="CA" or atom.atom_name.rstrip().lstrip()=="N" or atom.atom_name.rstrip().lstrip()=="O" or atom.atom_name.rstrip().lstrip()=="CB" or atom.atom_name.rstrip().lstrip()=="C"):
                    atom.residue="ALA"
                    atoms_to_keep.append(self.Atoms[index])
            self.Atoms=atoms_to_keep
        #Otherwise return a new chain object
        else:
            print("Not supported yet")


#Define chain class
class PDBChain:
    #Constructor
    def __init__(self, CHAIN_ID, PDB_ID=None, REMARKS=None, SEQRES=None, HELIX=None, ATOM=None, CRSYT1=None, SCALE=None,ORIGX=None):

        #Model ID
        self.PDB_ID=PDB_ID
        #Chain ID
        self.ID=CHAIN_ID
        #isPolyALA default to False
        self.isPolyALA=False
        #Chain sequence
        self.ThreeLetterSequence=[]
        self.OneLetterSequence = []
        if(SEQRES):
            for feature in SEQRES:
                if feature[11]==CHAIN_ID:
                    self.ThreeLetterSequence+=feature[19:].rstrip().split()
            self.OneLetterSequence = translate_3to1_AA(self.ThreeLetterSequence)

        #Missing residues
        if(REMARKS):
            self.MissingResidues=REMARKS.get_missing_residues(chain=CHAIN_ID)
        else:
            self.MissingResidues=""
        #Helix
        self.HELICES=[]
        if(HELIX):
            for singleHELIX in HELIX:
                if singleHELIX[19]==self.ID or singleHELIX[31]==self.ID:
                    self.HELICES.append(PDBHelix(singleHELIX))
        #Atom
        self.ATOMS=[]
        if(ATOM):
            for singleATOM in ATOM:
                if singleATOM[21]==self.ID:
                    self.ATOMS.append(PDBAtom(singleATOM))
        #CRSYT1, SCALE, ORIGX
        self.CRYST1=CRSYT1
        self.SCALE=SCALE
        self.ORIGX=ORIGX

    # Method to return only CAs
    def get_CAs(self,target_region=False):
        result = []
        #If the user only wants a region
        if(target_region):
            for atom in self.ATOMS:
                if atom.isCA and atom.residue_seqnumber in target_region:
                    result.append(atom)
        #Otherwise the user wants the entire chain
        else:
            for atom in self.ATOMS:
                if atom.isCA:
                    result.append(atom)
        #Return CAs
        return result

    #Method to return helices in a particular region
    def get_helices(self,target_region):
        #Loop through the helices and only return those that are totally or partially in the target region
        result=[]
        for helix in self.HELICES:
            #Do not allow helices that start rigth when the fragment stops (one residue helix LOL)
            if(int(helix.start_residue_seqnumber) in target_region or int(helix.stop_residue_seqnumber) in target_region):
                result.append(helix)
        return result

    #Method to return atoms in a particular region
    def get_atoms(self,target_region):
        #Loop through the helices and only return those that are totally or partially in the target region
        result=[]
        for atom in self.ATOMS:
            if(int(atom.residue_seqnumber) in target_region):
                result.append(atom)
        return result

    #Method to return missing residues in a particular region
    def get_missingresidues(self,target_region):
        #Loop through the helices and only return those that are totally or partially in the target region
        result=[]
        for residue in self.MissingResidues:
            if(int(residue.index) in target_region):
                result.append(residue)
        return result

    #Create function to extarct three letter and one letter sequence of a region
    def get_sequence(self,target_region,one_letter=False):
        #Loop through the residues and only return those that are totally or partially in the target region
        result=[]
        #If it is one letter
        if(one_letter):
            for index,residue in enumerate(self.OneLetterSequence):
                if(index in target_region):
                    result.append(residue)
        #Otherwise it is three letter
        else:
            for index,residue in enumerate(self.ThreeLetterSequence):
                if(index in target_region):
                    result.append(residue)
        return result

    #Create a function to return a specific fragment target_region=[int,int] in form of a PDBFragment object
    def get_fragment(self,target_region,FRAGMENT_ID,PDB_ID):
        #Extract fragment data
        fragment_three_letter_sequence=self.get_sequence(target_region)
        fragment_one_letter_sequence=self.get_sequence(target_region,one_letter=True)
        fragment_helices=self.get_helices(target_region=target_region)
        fragment_atoms=self.get_atoms(target_region=target_region)
        fragment_missingresidues=self.get_missingresidues(target_region=target_region)
        #Return the fragment as a PDBChain object
        return PDBFragment(PDB_ID=PDB_ID, FRAGMENT_ID=FRAGMENT_ID, CHAIN_ID=self.ID, OneSequence=fragment_one_letter_sequence, ThreeSequence=fragment_three_letter_sequence, Helices=fragment_helices, Atoms=fragment_atoms, MissingResidues=fragment_missingresidues, Cryst1=self.CRYST1, Scale=self.SCALE,Origx=self.ORIGX)

    # Create a function to renumber the atom sequence number or serial number
    def renumber_residues(self,seqnumber=True,serialnumber=True,start=1,inplace=True):
        #If we want to modify the object itself
        if(inplace):
            if(seqnumber and serialnumber):
                residue_count=-1
                prev_residue_seqnumber=0
                helices_start=[]
                helices_stop=[]
                anisou_dict={}  #{oldindex:newindex}
                #Store helix start and stops
                for helix in self.HELICES:
                    helices_start.append(helix.start_residue_seqnumber)
                    helices_stop.append(helix.stop_residue_seqnumber)
                #Loop through the atoms
                for index,atom in enumerate(self.ATOMS):
                    if(atom.isANISOU):
                        # Load the new serial number corresponding with its ATOM
                        atom.atom_serialnumber = anisou_dict[atom.atom_serialnumber]
                    else:
                        # Store the new serial number for anisou entries
                        anisou_dict[atom.atom_serialnumber] = str(start + index)
                        # New serial number
                        atom.atom_serialnumber = str(start + index)
                    #New sequence number
                    if(atom.residue_seqnumber!=prev_residue_seqnumber):
                        residue_count+=1
                        prev_residue_seqnumber = atom.residue_seqnumber
                        #Change helix indexes if necessary
                        if(atom.residue_seqnumber in helices_start):
                            for helix in self.HELICES:
                                if (atom.residue_seqnumber==helix.start_residue_seqnumber):
                                    helix.start_residue_seqnumber=str(start + residue_count)
                                    break
                        if(atom.residue_seqnumber in helices_stop):
                            for helix in self.HELICES:
                                if (atom.residue_seqnumber == helix.stop_residue_seqnumber):
                                    helix.stop_residue_seqnumber = str(start + residue_count)
                                    break
                        #Change the atom sequence number
                        atom.residue_seqnumber = str(start + residue_count)
                    #Same residue as before
                    else:
                        atom.residue_seqnumber=str(start+residue_count)
        #Otherwise it is necessary to create a new PDBChain object and return it
        else:
            print("Not supported yet")

    #Create a function to return a PDB file with the contents of the fragment
    def write_file(self,outfile_path):
        try:
            with open(outfile_path,"w") as outfile_handle:
                outfile_handle.write("REMARK   Fragment generated through pdb_tools\nREMARK   Original PDB model "+self.PDB_ID+":"+self.ID+"\n")
                SEQRES_lines=[self.ThreeLetterSequence[x:x + 13] for x in range(0, len(self.ThreeLetterSequence), 13)]
                for index,line in enumerate(SEQRES_lines):
                    seqres_record="SEQRES "+ (" " * (3 - len(str(index))) + str(index) + " " + self.ID + " ") + (" " * (4 - len(str(len(self.ThreeLetterSequence)))) + str(len(self.ThreeLetterSequence)) + "  " ) + " ".join(line)
                    outfile_handle.write(seqres_record+"\n")
                outfile_handle.write("  ".join(self.CRYST1))
                outfile_handle.write("".join(self.ORIGX))
                outfile_handle.write("".join(self.SCALE))
                for atom in self.ATOMS:
                    outfile_handle.write(atom.get_PDBLine()+"\n")
            outfile_handle.close()
        except FileNotFoundError:
            print("Impossible to create output file!")

    #Create a method to return a polyALA file
    def get_polyALA(self,inplace=True):
        #Store the atoms to be kept
        atoms_to_keep=[]
        for index,atom in enumerate(self.ATOMS):
            #If the atom is not a CA, N or O, delete it
            if(atom.atom_name.rstrip().lstrip()=="CA" or atom.atom_name.rstrip().lstrip()=="N" or atom.atom_name.rstrip().lstrip()=="O" or atom.atom_name.rstrip().lstrip()=="CB" or atom.atom_name.rstrip().lstrip()=="C"):
                atoms_to_keep.append(self.ATOMS[index])
        #Also replace the SEQRES
        new_ThreeLetterSequence=["ALA" for x in self.ThreeLetterSequence]
        new_OneLetterSequence=["A" for x in self.OneLetterSequence]

        # The user wants to modify current chain to be a polyALA
        if (inplace):
            self.ATOMS=atoms_to_keep
            #Change residue name
            for atom in self.ATOMS:
                atom.residue="ALA"
            self.OneLetterSequence=new_OneLetterSequence
            self.ThreeLetterSequence=new_ThreeLetterSequence
        #Otherwise return a new chain object
        else:
            polyALA=PDBChain(CHAIN_ID=self.ID,PDB_ID=self.PDB_ID,CRSYT1=self.CRYST1,SCALE=self.SCALE,ORIGX=self.ORIGX)
            polyALA.isPolyALA=True
            polyALA.ATOMS=atoms_to_keep
            #Change residue name
            for atom in polyALA.ATOMS:
                atom.residue="ALA"
            polyALA.HELICES=self.HELICES
            polyALA.ThreeLetterSequence=new_ThreeLetterSequence
            polyALA.OneLetterSequence=new_OneLetterSequence
            polyALA.MissingResidues=self.MissingResidues
            return polyALA


#Create a PDB file parser that returns a pdb object
class PDBFile:
    #Constructor function
    def __init__(self, PDB_ID, f_handle=None, PDBID_urlretrieve=False):

        #The user wants to donwload the file from the PDB database
        if(PDBID_urlretrieve):
            #Make imports
            import sys
            import os
            #Create a temporary file
            tmp_file=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/tmp/"+PDBID_urlretrieve.upper()+".pdb"
            #Import the appropiate module and download PDB file
            if (float(sys.version[:3]) < 3.0):
                import urllib
                urllib.urlretrieve("http://www.rcsb.org/pdb/files/"+PDBID_urlretrieve.upper()+".pdb", tmp_file)
            else:
                import urllib.request
                urllib.request.urlretrieve("http://www.rcsb.org/pdb/files/"+PDBID_urlretrieve.upper()+".pdb", tmp_file)
            #Open the file handle
            f_handle=open(tmp_file,"r")


        self.OriginalInputFile=f_handle.name
        self.PDB_ID=PDB_ID

        #Load the file lines
        infile=f_handle.readlines()

        ###
        ###     SOME MISCELLANEOUS
        ###

        #HEADER
        try:
            self.HEADER=PDBHeader([record for record in infile if "HEADER" in record][0])
        except IndexError:
            self.HEADER=None
        #TITLE
        try:
            self.TITLE=PDBTitle([record for record in infile if "TITLE" in record[:6]])
        except IndexError:
            self.TITLE=None
        #CAVEAT
        try:
            self.CAVEAT=PDBCaveat([record for record in infile if "CAVEAT" in record[:6]])
        except IndexError:
            self.CAVEAT=None
        #KEYWORDS
        try:
            self.KEYWORDS=PDBKeywords([record for record in infile if "KEYWDS" in record[:6]])
        except IndexError:
            self.KEYWORDS=None
        #EXPDTA
        try:
            self.EXPDATA=PDBExpdata([record for record in infile if "EXPDTA" in record[:6]])
        except IndexError:
            self.EXPDATA=None
        #REMARKS
        try:
            self.REMARKS=PDBRemark([record for record in infile if "REMARK" in record[:6]])
        except IndexError:
            self.REMARKS=None
        #CRYST1
        try:
            self.CRYST1=[record for record in infile if "CRYST1" in record[:6]]
        except IndexError:
            self.CRYST1=None
        #ORIGX
        try:
            self.ORIGX=[record for record in infile if "ORIGX" in record[:6]]
        except IndexError:
            self.ORIGX=None
        #SCALE
        try:
            self.SCALE=[record for record in infile if "SCALE" in record[:6]]
        except IndexError:
            self.SCALE=None
        #SEQRES
        try:
            self.SEQRES=[record for record in infile if "SEQRES" in record[:6]]
        except IndexError:
            self.SEQRES=None
        #DBREF
        try:
            self.DBREF=[record for record in infile if "DBREF" in record[:6]]
        except IndexError:
            self.DBREF=None
        #HELIX
        try:
            self.HELIX=[record for record in infile if "HELIX" in record[:6]]
        except IndexError:
            self.HELIX=None
        #ATOM
        try:
            self.ATOM=[record for record in infile if ("ATOM" in record[:6] or "ANISOU" in record[:6] or "HETATM" in record[:6])]
        except IndexError:
            self.ATOM=None
            print("WARNING: File does not contain ATOMS!")
        #COMPND
        try:
            self.COMPND=[record for record in infile if "COMPND" in record[:6]]
        except IndexError:
            self.COMPND=None
        #Model ID
        try:
            self.model_id = re.search('MOL_ID: (.*)', [feature for feature in self.COMPND if "MOL_ID:" in feature][0]).group(1)
        except IndexError:
            self.model_id = None
        #Molecule name
        try:
            self.molecule_name = re.search('MOLECULE: (.*)',[feature for feature in self.COMPND if " MOLECULE:" in feature][0]).group(1)
        except IndexError:
            self.molecule_name = None
        #Chain IDs
        all_chains=[]
        try:
            for atom in self.ATOM:
                all_chains.append(atom[21])
            self.chain_ids=set(all_chains)
        except IndexError:
            self.chain_ids = None
        #Fragment
        try:
            self.fragment = re.search('FRAGMENT: (.*)',
                                      [feature for feature in self.COMPND if "FRAGMENT:" in feature][0]).group(1)
        except IndexError:
            self.fragment = "NA"
        #Synonims
        try:
            self.synonim = re.search('SYNONYM: (.*)',
                                     [feature for feature in self.COMPND if "SYNONYM:" in feature][0]).group(1).split(", ")
        except IndexError:
            self.synonim = "NA"
        #EC
        try:
            self.ec = re.search('EC: (.*)', [feature for feature in self.COMPND if "EC: " in feature][0]).group(1)
        except IndexError:
            self.ec = "NA"
        #Engineered
        try:
            if (re.search('ENGINEERED: (.*)', [feature for feature in self.COMPND if "ENGINEERED: " in feature][0]).group(1) == "YES" or re.search('ENGINEERED: (.*)',[feature for feature in self.COMPND if "ENGINEERED: " in feature][0]).group(1) == "YES;"):
                self.engineered = True
            else:
                self.engineered = False
        except IndexError:
            self.engineered = False
        #Mutation
        try:
            if (re.search('MUTATION: (.*)', [feature for feature in self.COMPND if "MUTATION: " in feature][0]).group(1) == "YES" or re.search('MUTATION: (.*)',[feature for feature in self.COMPND if "MUTATION: " in feature][0]).group(1) == "YES;"):
                self.mutation = True
            else:
                self.mutation = False
        except IndexError:
            self.mutation = False


        ###
        ###     HIERARCHY  PDBFile > PDBModel > PDBChain
        ###

        # Create the chain objects
        self.CHAINS = {}  # {chainID:chain_object}
        for chain in self.chain_ids:
            chain=chain.lstrip().rstrip().replace(';', '').replace(',', '')
            self.CHAINS[chain] = PDBChain(PDB_ID=self.PDB_ID, CHAIN_ID=chain, REMARKS=self.REMARKS, SEQRES=self.SEQRES, HELIX=self.HELIX, ATOM=self.ATOM, CRSYT1=self.CRYST1, SCALE=self.SCALE, ORIGX=self.ORIGX)

        #The user wanted to donwload the file from the PDB database, delete the tmp file
        if(PDBID_urlretrieve):
            #Close the file handle
            f_handle.close()
            os.remove(tmp_file)

    #Create a method to return a fragment
    def get_fragment(self,FRAGMENT_ID,target_chain,target_region):
        # Extract fragment data
        fragment_three_letter_sequence=self.CHAINS[target_chain].get_sequence(target_region)
        fragment_one_letter_sequence=self.CHAINS[target_chain].get_sequence(target_region,one_letter=True)
        fragment_helices = self.CHAINS[target_chain].get_helices(target_region=target_region)
        fragment_atoms = self.CHAINS[target_chain].get_atoms(target_region=target_region)
        fragment_missingresidues = self.CHAINS[target_chain].get_missingresidues(target_region=target_region)
        # Return the fragment as a PDBChain object
        return PDBFragment(PDB_ID=self.PDB_ID, FRAGMENT_ID=FRAGMENT_ID, CHAIN_ID=target_chain, OneSequence=fragment_one_letter_sequence,ThreeSequence=fragment_three_letter_sequence, Helices=fragment_helices, Atoms=fragment_atoms,MissingResidues=fragment_missingresidues, Cryst1=self.CRYST1, Scale=self.SCALE,Origx=self.ORIGX)

    #Create a method to create a polyALA chain
    def get_polyALA(self,chain_id,inplace=True):
        if(inplace):
            self.CHAINS[chain_id].get_polyALA(inplace)
        else:
            result_polyALA=self.CHAINS[chain_id].get_polyALA(inplace)
            return result_polyALA

#Program starts
if __name__ == "__main__":
    #Test
    test_file="/home/filo/Documents/PhD_Stuff/Data/MyDataset/PDB/4qnd.pdb"
    test_handle=open(test_file, "r")
    test_object=PDBFile("3WO6",test_handle)
    test_handle.close()

    #Parse the file
    #test_object=PDBFile("3WO6",PDBID_urlretrieve="3WO6")
    #Write entire chain
    #test_object.CHAINS["A"].write_file("/home/filo/test_chainA.pdb")
    #Get frag and write into file
    test_frag=test_object.get_fragment(FRAGMENT_ID="test",target_chain="A",target_region=range(25,101))
    #test_frag.renumber_residues()
    test_frag.write_file("/home/filo/test_chainA_25_100.pdb")
    #Get polyALA
    test_polyALA=test_object.CHAINS["A"].get_polyALA(inplace=False)
    test_polyALA.write_file("/home/filo/test_chainA_polyALA.pdb")
#test_object.CHAINS["A"].write_file("/home/filo/test_chainA.pdb")