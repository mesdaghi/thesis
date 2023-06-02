'''
 Class to store contact data
 Forms part of the CONPyMOL pluggin
'''

# Imports
import sys
import os
import math
from pymol import cmd
from pymol.Qt.utils import loadUi
from pymol import cgo


class Contact(object):
    # Constructor
    def __init__(self, molID_A, residx_A, residx_B, score, molID_B=None):
        # Store the data
        self.molID_A = molID_A
        if molID_B is not None:
            self.molID_B = molID_B
        else:
            self.molID_B = molID_A
        self.residx_A = residx_A
        self.residx_B = residx_B
        self.score = round(score, 2)
        # Get the coordinates of the residues
        self.coords_A = cmd.get_model('/%s///%s/CA' % (self.molID_A, self.residx_A), 1).get_coord_list()[0]
        self.coords_B = cmd.get_model('/%s///%s/CA' % (self.molID_B, self.residx_B), 1).get_coord_list()[0]
        # Get the real distance between coordinates A and B
        self.distance = cmd.get_distance('/%s///%s/CA' % (self.molID_A, self.residx_A),
                                         '/%s///%s/CA' % (self.molID_B, self.residx_B))
        self.distance = round(self.distance, 2)
        # Get the unique id for this object
        self.contact_ID = "%s_%s_%s_%s" % (self.molID_A, self.residx_A, self.molID_B, self.residx_B)
        self.cylinder_ID = "Contact_%s" % (self.contact_ID)
        self.label_ID = "Label_%s" % (self.contact_ID)
        # Get the sequence seperation between the residues
        self.seq_separation = abs(self.residx_A - self.residx_B)
        self.neighbours = False
        self.short_range = False
        self.medium_range = False
        self.long_range = False
        # Get the contact range
        if 6 <= self.seq_separation <= 11:
            self.short_range = True
            self.distance_class = "short"
        elif 12 <= self.seq_separation <= 23:
            self.medium_range = True
            self.distance_class = "medium"
        elif self.seq_separation >= 24:
            self.long_range = True
            self.distance_class = "long"
        else:
            self.neighbours = True
            self.distance_class = "neighbours"
        # Determine whether this contact might be a result of interactions in the biological unit
        if self.distance > 11 and self.score > 0.4:
            self.biounit_contact = True
        else:
            self.biounit_contact = False

    # Create a method to create a cilinder
    def create_cylinder(self, color_A=(0, 1, 0), color_B=(0, 1, 0), radius=0.1):
        print("(molID_A=%s residx_A=%s molID_B=%s residx_B=%s score=%s distance=%s)" % (
            self.molID_A, self.residx_A, self.molID_B, self.residx_B, self.score, self.distance))
        cmd.load_cgo(
            [cgo.CYLINDER, self.coords_A[0], self.coords_A[1], self.coords_A[2], self.coords_B[0], self.coords_B[1],
             self.coords_B[2], radius, color_A[0], color_A[1], color_A[2], color_B[0], color_B[1], color_B[2]],
            self.cylinder_ID)

    # Create a method to show a label for the contact with the score or the distance
    def show_label(self, label_choice):
        # If the object exists already, delete the pseudoatom
        cmd.delete(self.label_ID)
        label_position = ((self.coords_A[0] + self.coords_B[0]) / 2, (self.coords_A[1] + self.coords_B[1]) / 2,
                          (self.coords_A[2] + self.coords_B[2]) / 2)
        # Create a pseudoatom and put the label
        if label_choice == "score":
            cmd.pseudoatom(object=self.label_ID, pos=label_position, label=str(self.score))
        elif label_choice == "sequence separation":
            cmd.pseudoatom(object=self.label_ID, pos=label_position, label=str(self.seq_separation))
        else:
            # Generate a pseudoatom for the label
            cmd.pseudoatom(object=self.label_ID, pos=label_position, label=str(self.distance))

    # Create a function to determine wether the contact complies with some range
    def complies_range(self, distance_threshold):
        if distance_threshold == "all":
            return True
        elif distance_threshold == "long":
            return self.long_range
        elif distance_threshold == "medium":
            if self.long_range:
                return True
            else:
                return self.medium_range
        elif distance_threshold == "short":
            if self.long_range:
                return True
            elif self.medium_range:
                return True
            else:
                return self.short_range
