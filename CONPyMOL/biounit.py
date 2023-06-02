'''
 Class to store data for a biological unit
 Forms part of the CONPyMOL pluggin
'''

# Imports
import sys
import os
import math
from pymol import cmd
from pymol.Qt.utils import loadUi
from pymol import cgo
from contact import Contact
from RGB import rgb
from molecule import Molecule
import itertools


class BioUnit(object):
    # Constructor
    def __init__(self, parent_molID):
        # Store the data
        self.parent_molID = parent_molID
        self.residue_dict = {'resid_list': []}
        cmd.iterate("(%s and name ca)" % self.parent_molID, "resid_list.append((resi,resn))", space=self.residue_dict)
        self.seq_length = len(self.residue_dict['resid_list'])
        self.state_molID_list = None
        self.cmap_fpath = None
        self.predicted_contacts = None
        self.real_contacts = None
        self.cmap_format = None
        self.molecule_list = None

    # Create wrappers arround the simple molecule functions
    def renumber_residues(self):
        for molecule in self.molecule_list:
            molecule.renumber_residues()

    def create_groups(self):
        for molecule in self.molecule_list:
            molecule.create_groups()

    # Create a function to show the biological unit
    def show_biological_unit(self, cif_fpath):
        # Open the cif file and get the biological unit
        cmd.reinitialize()
        cmd.set("assembly", "1")
        cmd.load(cif_fpath)

    # Create a function to state the bio unit into its states
    def split_states(self):
        cmd.split_states(self.parent_molID)
        cmd.delete(self.parent_molID)
        self.state_molID_list = [x for x in list(cmd.get_object_list('(all)'))]
        self.molecule_list = []
        for state in self.state_molID_list:
            self.molecule_list.append(Molecule(molID=state))

    # Create function to load the contacts and return a cmap object
    def load_contacts(self, cmap_fpath, cmap_format="psicov", score_threshold=0.5):
        self.cmap_format = cmap_format
        self.cmap_fpath = cmap_fpath
        # Inform the user
        print("Contact map file path: " + cmap_fpath)
        print("Contact map format: " + cmap_format)
        # Create a contact list that will contain the contacts in the file as tuples
        self.predicted_contacts = []
        # Determine the index of the fields in the file
        if cmap_format == "casp" or cmap_format == "casprr" or cmap_format == "psicov" or cmap_format == "gremlin" or cmap_format == "epcmap" or cmap_format == "nebcon":
            res1 = 0
            res2 = 1
            score = 4
        elif cmap_format == "membrain":
            res1 = 1
            res2 = 4
            score = 6
        elif cmap_format == "comsat":
            res1 = 0
            res2 = 2
            score = 999
        elif cmap_format == "evfold":
            res1 = 0
            res2 = 2
            score = 5
        elif cmap_format == "flib" or cmap_format == "saint2" or cmap_format == "plmdca" or cmap_format == "pconsc":
            res1 = 0
            res2 = 1
            score = 2
        elif cmap_format == "freecontact":
            res1 = 0
            res2 = 2
            score = 4
        else:
            print("FATAL ERROR: Format %s is not supported" % cmap_format)
            sys.exit()
        try:
            # Save the contacts in the file as tuples in the contact list
            with open(cmap_fpath, "r") as cmap_file:
                for line in cmap_file:
                    if cmap_format == "plmdca":
                        line = line.rstrip().split(",")
                    else:
                        line = line.rstrip().split()
                    if len(line) >= 3 and line[res1].isnumeric():
                        if int(line[res1]) > self.seq_length or int(line[res2]) > self.seq_length:
                            print("WARNING: Contact (%s,%s) out of range for protein %s residues long!!" % (
                                line[res1], line[res2], self.seq_length))
                            continue
                        if float(line[score]) > score_threshold:
                            for state in self.molecule_list:
                                self.predicted_contacts.append(
                                    Contact(molID_A=state.molID, residx_A=int(line[res1]), residx_B=int(line[res2]),
                                            score=float(line[score] if score < len(line) else 1.0)))
        # Handle exception if file doesn't exist
        except IOError:
            print("FATAL ERROR: Impossible to open file! " + cmap_fpath)
            sys.exit()

    # Create a function to plot the contacts of this molecule
    def plot_contacts(self, score_threshold=0.5, color_choice="red", label_choice="score", radius_choice=0.2,
                      distance_range=None):
        print("Plotting contacts now:")
        if distance_range is None:
            distance_range = {"neighbours": True, "short": True, "medium": True, "long": True}

        ''' TODO: detect contacts originated from the interactions in the biounit
        for contact in self.predicted_contacts:
            if contact.biounit_contact:
                print("%s %s %s %s" % (
                    contact.molID_A, contact.molID_B, contact.residx_A, contact.residx_B))
                # Check whether the residues of this contact are in close proximity in different chains of the unit
                all_possible_combinations = itertools.combinations(self.molecule_list, 2)
                for combination in all_possible_combinations:
                    biocontact = Contact(molID_A=combination[0].molID, molID_B=combination[1].molID,
                                         residx_A=contact.residx_A, residx_B=contact.residx_B, score=contact.score)
                    print("distance %s" % biocontact.distance)
                    if biocontact.distance < 11:
                        biocontact.create_cylinder(color_A=rgb(color="blue"), color_B=rgb(color="blue"),
                                                radius=radius_choice)
                    else:
                        biocontact.create_cylinder(color_A=rgb(color="red"), color_B=rgb(color="red"),
                                                   radius=radius_choice)
        return
        '''
        # If the user wants to color things according to satisfaction
        if color_choice == "contact satisfaction":
            # Load the real contacts
            self.get_real_cmap()
            pred_cons = [(x.residx_A, x.residx_B) for x in self.predicted_contacts]
            # Plot all real contacts
            for contact_idx, contact in enumerate(self.real_contacts):
                if distance_range[contact.distance_class]:
                    if (contact.residx_A, contact.residx_B) in pred_cons or (
                            contact.residx_B, contact.residx_A) in pred_cons:
                        contact.create_cylinder(color_A=rgb(color="green"), color_B=rgb(color="green"),
                                                radius=radius_choice)
                    else:
                        contact.create_cylinder(color_A=rgb(color="red"), color_B=rgb(color="red"),
                                                radius=radius_choice)
                    contact.show_label(label_choice)

        # Otherwise the user wants another color option
        else:
            # Loop through the predicted contacts
            for contact_idx, contact in enumerate(self.predicted_contacts):
                # Only compute the contact if the raw score is higher than treshold
                if (contact.score < score_threshold or not distance_range[contact.distance_class]):
                    continue
                # Create a cylinder for the contact with the appropiate color
                if (color_choice == "contact score"):
                    contact.create_cylinder(color_A=rgb(value=contact.score), color_B=rgb(value=contact.score),
                                            radius=radius_choice)
                elif (color_choice == "false positives"):
                    if float(contact.distance) > 8.99:
                        contact.create_cylinder(color_A=rgb(color="red"), color_B=rgb(color="red"),
                                                radius=radius_choice)
                    else:
                        contact.create_cylinder(color_A=rgb(color="green"), color_B=rgb(color="green"),
                                                radius=radius_choice)
                elif (color_choice == "contact range"):
                    if contact.short_range:
                        contact.create_cylinder(color_A=rgb(color="orange"), color_B=rgb(color="orange"),
                                                radius=radius_choice)
                    elif contact.medium_range:
                        contact.create_cylinder(color_A=rgb(color="yellow"), color_B=rgb(color="yellow"),
                                                radius=radius_choice)
                    elif contact.long_range:
                        contact.create_cylinder(color_A=rgb(color="green"), color_B=rgb(color="green"),
                                                radius=radius_choice)
                    else:
                        contact.create_cylinder(color_A=rgb(color="red"), color_B=rgb(color="red"),
                                                radius=radius_choice)
                else:
                    contact.create_cylinder(color_A=rgb(color=color_choice), color_B=rgb(color=color_choice),
                                            radius=radius_choice)
                # Tag the contact with the appropiate label
                contact.show_label(label_choice)

        # Re-center the display into the molecule
        cmd.center(self.molecule_list[0].molID)
        cmd.zoom(self.molecule_list[0].molID)

    # Create a function to load the real contacts of the molecule
    def get_real_cmap(self):
        self.real_contacts = []
        self.renumber_residues()
        stored_contacts = []
        # Loop through all the residues in the molecule
        for residue in self.residue_dict['resid_list']:
            # Get the residues within 8.0 A
            contacting_residues = {'resid_list': []}
            cmd.iterate('(/%s///%s/CA around 8.0)' % (self.molID, residue[0]), "resid_list.append((resi,resn))",
                        space=contacting_residues)
            contacting_residues = contacting_residues['resid_list']
            # Create a contact for each contacting residue (exclude PSD and HET)
            for con_res in contacting_residues:
                seq_separation = abs(int(con_res[0]) - int(residue[0]))
                if con_res[1] != "PSD" and con_res != "HET" and con_res[0] != residue[0] and (
                        con_res[0], residue[0]) not in stored_contacts:
                    self.real_contacts.append(
                        Contact(molID=self.molID, residx_A=int(residue[0]), residx_B=int(con_res[0]), score=1.0))
                    stored_contacts.append((residue[0], con_res[0]))
