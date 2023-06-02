'''
 PyMol plugin to superimpose contact map into PDB structure
 Dependencies:
    PyQt5
    Pymol 2.X
'''

# Imports
import sys
import os
from molecule import Molecule
from biounit import BioUnit


# Initiate the pluggin
def __init_plugin__(app=None):
    '''
    Add an entry to the PyMOL "Plugin" menu
    '''
    from pymol.plugins import addmenuitemqt
    addmenuitemqt(label='CONpyMOL', command=run_plugin_gui)


# Run the graphical user interface
def run_plugin_gui():
    '''
    Instantiate our custom main window class using the layout in the ui file (created with qt designer)
    '''

    # Make the imports
    from pymol import cmd
    from pymol.Qt.utils import loadUi
    from PyQt5 import QtWidgets
    import PyQt5
    from PyQt5.QtGui import QStandardItem, QStandardItemModel
    from PyQt5.QtCore import QVariant

    # Initiate qdialog
    window = PyQt5.QtWidgets.QMainWindow()

    # Load form from ui file
    pluggin_homedir = os.path.dirname(os.path.realpath(__file__))
    uifile = os.path.join(pluggin_homedir, "contacts_qtwidget.ui")
    form = loadUi(uifile, window)

    # Populate the list view with the molecule IDs
    molecule_list = [x for x in list(cmd.get_object_list('(all)')) if
                     "Contact_" not in x and "Label_" not in x and "CONpyMOL_colorbar" not in x]
    model = QStandardItemModel(form.MoleculeSelectionListView)
    model.clear()
    for molecule in molecule_list:
        item = QStandardItem(molecule)
        item.setFlags(PyQt5.QtCore.Qt.ItemIsUserCheckable | PyQt5.QtCore.Qt.ItemIsEnabled)
        check = PyQt5.QtCore.Qt.Unchecked
        item.setData(QVariant(check), PyQt5.QtCore.Qt.CheckStateRole)
        model.appendRow(item)
    form.MoleculeSelectionListView.setModel(model)
    form.MoleculeSelectionListView.setEnabled(False)

    # Function connected to OpenFile button
    def get_contact_fpath():
        # Open a file selection window
        form.cmap_fpath = QtWidgets.QFileDialog.getOpenFileName()[0]
        if not os.path.isfile(form.cmap_fpath):
            error_msg = QtWidgets.QMessageBox()
            error_msg.setIcon(QtWidgets.QMessageBox.Critical)
            error_msg.setText("WARNING")
            error_msg.setInformativeText('Please select a valid contact map file')
            error_msg.setWindowTitle("Error")
            error_msg.exec_()
            return
        # Empty the file selection label
        form.NoFileSelectedLabel.setText('')
        # Enable all display options
        form.CmapFormatLabel.setEnabled(True)
        form.CmapFormatComboBox.setEnabled(True)
        form.ScoreThresholdLabel.setEnabled(True)
        form.ScoreThresholdSpinBox.setEnabled(True)
        form.ColorChoiceLabel.setEnabled(True)
        form.ColorChoiceComboBox.setEnabled(True)
        form.LabelChoiceLabel.setEnabled(True)
        form.LabelChoiceComboBox.setEnabled(True)
        form.ThicknessSpinBox.setEnabled(True)
        form.ThicknessLabel.setEnabled(True)
        form.ShowLabelsCheckBox.setEnabled(True)
        form.CleanDisplayCheckBox.setEnabled(True)
        form.Optionslabel.setEnabled(True)
        form.MoleculeSelectionListView.setEnabled(True)
        form.FinalButtonBox.setEnabled(True)

    # Create a function to open a cif file
    def get_cif_fpath():
        form.cif_fpath = QtWidgets.QFileDialog.getOpenFileName()[0]
        if not os.path.isfile(form.cif_fpath):
            error_msg = QtWidgets.QMessageBox()
            error_msg.setIcon(QtWidgets.QMessageBox.Critical)
            error_msg.setText("WARNING")
            error_msg.setInformativeText('Please select a valid cif file')
            error_msg.setWindowTitle("Error")
            error_msg.exec_()
            return
        form.ShowBioUnitCheckBox.setEnabled(True)

    # Function connected to OK button
    def draw_contacts():

        # Load the display options and check user input
        molid_list = []
        model = form.MoleculeSelectionListView.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.isCheckable() and item.checkState() == PyQt5.QtCore.Qt.Checked:
                molid_list.append(str(item.text()))
        # Make sure that the user selected at list a molecule to plot
        if molid_list == []:
            error_msg = QtWidgets.QMessageBox()
            error_msg.setIcon(QtWidgets.QMessageBox.Critical)
            error_msg.setText("WARNING")
            error_msg.setInformativeText('Please select at least one molecule!')
            error_msg.setWindowTitle("Error")
            error_msg.exec_()
            return
        # If the user wants to show the bio unit, there should be only one molecule selected
        elif form.ShowBioUnitCheckBox.isChecked() and len(molid_list) != 1:
            error_msg = QtWidgets.QMessageBox()
            error_msg.setIcon(QtWidgets.QMessageBox.Critical)
            error_msg.setText("WARNING")
            error_msg.setInformativeText('Please select a unique molecule to display the biological unit!')
            error_msg.setWindowTitle("Error")
            error_msg.exec_()
            return

        # Load the rest of user inputs
        cmap_file_format = str(form.CmapFormatComboBox.currentText())
        cmap_file_path = form.cmap_fpath
        display_bio_unit = form.ShowBioUnitCheckBox.isChecked()
        label_choice = str(form.LabelChoiceComboBox.currentText())
        show_labels = bool(form.ShowLabelsCheckBox.isChecked())
        color_choice = str(form.ColorChoiceComboBox.currentText())
        radius_choice = float(form.ThicknessSpinBox.value()) / 10
        score_threshold = float(form.ScoreThresholdSpinBox.value())
        clean_display = bool(form.CleanDisplayCheckBox.isChecked())
        distance_range = {"neighbours": form.actionShow_neighbours.isChecked(),
                          "short": form.actionShow_short.isChecked(),
                          "medium": form.actionShow_medium.isChecked(),
                          "long": form.actionShow_long.isChecked()}

        # Delete any of the already existing contacts if the user wants to
        if clean_display:
            list_measurements = cmd.get_names_of_type("object:cgo")
            for measurement in list_measurements:
                if "Contact_" in measurement:
                    cmd.delete(measurement)
            # Do the same with the labels
            list_molecules = cmd.get_names_of_type("object:molecule")
            for molecule in list_molecules:
                if "Label_" in molecule:
                    cmd.delete(molecule)
            cmd.hide("labels")
            # Delete the color bar legend if any
            if "CONpyMOL_colorbar" in cmd.get_names_of_type("object:ramp"):
                cmd.delete("CONpyMOL_colorbar")
            # Refresh
            cmd.refresh_wizard()

        # If the user wants to display the biological unit, do so
        if display_bio_unit:
            biological_unit = BioUnit(parent_molID=molid_list[0])
            biological_unit.show_biological_unit(cif_fpath=form.cif_fpath)
            biological_unit.split_states()
            biological_unit.renumber_residues()
            biological_unit.load_contacts(cmap_fpath=cmap_file_path, cmap_format=cmap_file_format,
                                          score_threshold=score_threshold)
            biological_unit.plot_contacts(score_threshold=score_threshold, color_choice=color_choice,
                                          label_choice=label_choice, radius_choice=radius_choice,
                                          distance_range=distance_range)
            biological_unit.create_groups()

        # Otherwise load the contacts normally
        else:
            # Plot contacts for each selected molecule
            for molecule_id in molid_list:
                current_molecule = Molecule(molID=molecule_id)
                current_molecule.renumber_residues()
                current_molecule.load_contacts(cmap_fpath=cmap_file_path, cmap_format=cmap_file_format)
                current_molecule.plot_contacts(score_threshold=score_threshold, color_choice=color_choice,
                                               label_choice=label_choice, radius_choice=radius_choice,
                                               distance_range=distance_range)
                current_molecule.create_groups()

        # Set the round ends
        cmd.set("dash_round_ends", 1)

        # Show / hide labels
        if not show_labels:
            cmd.hide("labels")

        # If the user wants to see the colors, add a color bar
        if (color_choice == "contact score"):
            cmd.ramp_new("CONpyMOL_colorbar", "none", [0.0, 0.5, 1.0], ["red", "brown", "green"])

        # Refresh
        cmd.refresh_wizard()

    # Hook up functions with button connections
    form.actionOpen_cmap.triggered.connect(get_contact_fpath)
    form.actionOpen_cif.triggered.connect(get_cif_fpath)
    form.FinalButtonBox.accepted.connect(draw_contacts)
    form.FinalButtonBox.rejected.connect(window.close)

    # Show dialog window
    window.show()
