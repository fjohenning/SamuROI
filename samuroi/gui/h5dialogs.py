from PyQt4 import QtGui


class H5Dialog(QtGui.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(H5Dialog, self).__init__(*args, **kwargs)

        self.setNameFilter("hdf5 Files (*.h5 *.hdf *.hdf5)")
        if "directory" not in kwargs.keys():
            self.setDirectory('.')

        # get the grid layout of the dialog
        # TODO: make nice sub layout
        layout = self.layout()

        self.chk_branches = QtGui.QCheckBox("Branch Masks")
        self.chk_freehand = QtGui.QCheckBox("Freehand Masks")
        self.chk_pixel = QtGui.QCheckBox("Pixel Masks")
        self.chk_circles = QtGui.QCheckBox("Circle Masks")

        self.chk_traces = QtGui.QCheckBox("Traces")
        self.chk_data = QtGui.QCheckBox("Data")
        self.chk_mask = QtGui.QCheckBox("Threshold Mask")

        layout.addWidget(self.chk_branches)
        layout.addWidget(self.chk_freehand)
        layout.addWidget(self.chk_circles)
        layout.addWidget(self.chk_pixel)
        layout.addWidget(self.chk_traces)
        layout.addWidget(self.chk_mask)
        layout.addWidget(self.chk_data)


class H5SaveDialog(H5Dialog):
    def __init__(self, *args, **kwargs):
        super(H5SaveDialog, self).__init__(*args, **kwargs)

        self.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        self.setFileMode(QtGui.QFileDialog.AnyFile)

        self.chk_branches.setChecked(True)
        self.chk_freehand.setChecked(True)
        self.chk_pixel.setChecked(True)
        self.chk_circles.setChecked(True)
        self.chk_traces.setChecked(True)
        self.chk_data.setChecked(False)
        self.chk_mask.setChecked(True)

        self.chk_branches.setToolTip("Store the branch rois in the hdf5 file.")
        self.chk_freehand.setToolTip("Store the freehand rois in the hdf5 file.")
        self.chk_pixel.setToolTip("Store the pixel rois in the hdf5 file.")
        self.chk_circles.setToolTip("Store the circle rois in the hdf5 file.")
        self.chk_traces.setToolTip("Also store the traces of all selected rois as shown in the current preview.")
        self.chk_data.setToolTip("Store the 3D video data the hdf5 file.\n " + \
                                 "This will significantly increase the filesize.")
        self.chk_mask.setToolTip("Store the threshold value and binary mask in the hdf5 file.")


class H5LoadDialog(H5Dialog):
    def __init__(self, *args, **kwargs):
        super(H5LoadDialog, self).__init__(*args, **kwargs)

        self.setFileMode(QtGui.QFileDialog.ExistingFile)
        self.setAcceptMode(QtGui.QFileDialog.AcceptOpen)

        self.chk_branches.setEnabled(False)
        self.chk_freehand.setEnabled(False)
        self.chk_pixel.setEnabled(False)
        self.chk_circles.setEnabled(False)
        self.chk_traces.setEnabled(False)
        self.chk_data.setEnabled(False)
        self.chk_mask.setEnabled(False)

        self.chk_branches.setToolTip("Load the branch rois from the hdf5 file.")
        self.chk_freehand.setToolTip("Load the freehand rois from the hdf5 file.")
        self.chk_pixel.setToolTip("Load the pixel rois from the hdf5 file.")
        self.chk_circles.setToolTip("Load the circle rois from the hdf5 file.")
        self.chk_traces.setToolTip("The traces can never be loaded from hdf files,\n" + \
                                   " since they are defined by the masks and the data.")
        self.chk_data.setToolTip("Load the 3D video data from the hdf5 file.\n " + \
                                 "This will discard the currently selected dataset.")
        self.chk_mask.setToolTip("Load the threshold value and binary mask from the hdf5 file.")


        self.currentChanged.connect(self.update_checkboxes)

    def update_checkboxes(self, filename):
        # make QString to str
        filename = str(filename)
        import h5py
        f = h5py.File(filename, mode='r')

        self.chk_branches.setEnabled("branches" in f)
        self.chk_freehand.setEnabled("polygons" in f)
        self.chk_pixel.setEnabled("pixels" in f)
        self.chk_circles.setEnabled("circles" in f)
        self.chk_data.setEnabled("data" in f)
        self.chk_mask.setEnabled("mask" in f)

        self.chk_branches.setChecked("branches" in f)
        self.chk_freehand.setChecked("polygons" in f)
        self.chk_pixel.setChecked("pixels" in f)
        self.chk_circles.setChecked("circles" in f)
        self.chk_data.setChecked("data" in f)
        self.chk_mask.setChecked("mask" in f)

        # write stuff to disc
        f.close()
