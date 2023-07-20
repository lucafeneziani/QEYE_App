import numpy as np
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit
import pyqtgraph as pg
import os
import datetime

import functions
import configuration_params
from constants import TO_WE, TO_EYETISSUE, TO_PERSPEX, CLINICAL_RANGE_PERC, PEAK_WIDTH_PERC

DIRECTORY = '/Users/lucafeneziani/Desktop/QEYE/QEYE_App/'

########################################################################################################################################

class QApp(QMainWindow):
    def __init__(self):
        super(QApp, self).__init__()
        self.GUIstruct()
    
    def GUIstruct(self):
        width = QDesktopWidget().screenGeometry().width()
        height = QDesktopWidget().screenGeometry().height()
        self.setGeometry(0,0,round(width),round(height))
        self.setWindowTitle("QApp")
        self.setStyleSheet('background: whitesmoke')

        #########################################################################
        # GUI STYLE
        
        self.button_style = 'QPushButton:enabled{color: black; \
                                                background-color: white; \
                                                border: 1px solid gray; \
                                                border-radius: 5px; \
                                                border-style: outset} \
                             QPushButton:disabled{color: lightgray; \
                                                background-color: whitesmoke; \
                                                border: 1px lightgray; \
                                                border-radius: 5px; \
                                                border-style: outset} \
                             QPushButton:pressed{background-color: whitesmoke; \
                                                border-style: inset} \
                             QPushButton:checked{color: green; \
                                                background-color: palegreen}'
    
        self.analyze_style = 'QPushButton:enabled{color: black; \
                                                background-color: lightgreen; \
                                                border: 1px solid gray; \
                                                border-radius: 5px; \
                                                border-style: outset} \
                             QPushButton:disabled{color: lightgreen; \
                                                background-color: #BDFCC9; \
                                                border: 1px solid lightgray; \
                                                border-radius: 5px; \
                                                border-style: outset} \
                             QPushButton:pressed{background-color: #BDFCC9; \
                                                border-style: inset}'
        
        self.reset_style = 'QPushButton{color: red; \
                                        background-color: lightgray; \
                                        border: 1px solid gray; \
                                        border-radius: 5px; \
                                        border-style: outset} \
                             QPushButton:pressed{background-color: whitesmoke; \
                                                border-style: inset}'
        
        self.line_style = 'background-color: None; \
                           border: 3px solid lightseagreen; \
                           border-radius: 10px'
        
        
        textstyle = QFont()
        textstyle.setBold(True)
        textstyle2 = QFont(None,15)
        textstyle2.setBold(True)
        self.pen_data = pg.mkPen(color='red', width=3)
        self.pen_fit = pg.mkPen(color='lightseagreen', width=3, style=Qt.DashLine)
        self.pen_fit2 = pg.mkPen(color='navy', width=3, style=Qt.DashLine)
        self.pen_roi = pg.mkPen(color=(50,50,50), width=1)

        #########################################################################
        # VARIABLES

        self.analysis_window = False
        self.to_equivalence = TO_WE

        #########################################################################
        # CONFIGURATION PARAMS
        
        self.detector_params  = configuration_params.configs

        #########################################################################
        # TOP

        # Bar
        self.barlabel = QLabel(self)
        self.pixmap = QPixmap(DIRECTORY + 'images/bar.png')
        self.pixmap = self.pixmap.scaledToWidth(round(width),Qt.SmoothTransformation)
        self.barlabel.setPixmap(self.pixmap)
        self.barlabel.resize(round(width), round(0.085*height))
        self.barlabel.move(round(0.0*width), round(0.0*height))

        # De.Tec.Tor Logo
        self.logolabel = QLabel(self)
        self.pixmap = QPixmap(DIRECTORY + 'images/DeTecTor.png')
        self.pixmap = self.pixmap.scaledToHeight(round(0.05*height),Qt.SmoothTransformation)
        self.logolabel.setPixmap(self.pixmap)
        self.logolabel.resize(round(0.27*width), round(0.085*height))
        self.logolabel.move(round(0.72*width), round(0.0*height))
        self.logolabel.setStyleSheet('background-color: None')

        # Device logo
        self.logolabel = QLabel(self)
        self.pixmap = QPixmap(DIRECTORY + 'images/detectors/logo_QEYE.png')
        self.pixmap = self.pixmap.scaledToHeight(round(0.045*height),Qt.SmoothTransformation)
        self.logolabel.setPixmap(self.pixmap)
        self.logolabel.resize(round(0.27*width), round(0.085*height))
        self.logolabel.move(round(0.05*width), round(0.0*height))
        self.logolabel.setStyleSheet('background-color: None')

        #########################################################################
        # LEFT SIDE

        # Z Plot
        self.ZPlot = pg.PlotWidget(self)
        self.ZPlot.setLabel('left','counts')
        self.ZPlot.setLabel('bottom','channels')
        self.ZPlot.setTitle('Profile Z total counts')
        self.ZPlot.resize(round(0.65*width), round(0.45*height))
        self.ZPlot.move(round(0.02*width), round(0.12*height))
        self.ZPlot.setBackground('white')
        self.ZPlot.showGrid(x=True, y=True, alpha=0.4)

        # Shaw Z Raw Data button
        self.shawZraw = QPushButton(self)
        self.shawZraw.setText("Hide Data")
        self.shawZraw.resize(round(0.07*width), round(0.04*height))
        self.shawZraw.move(round(0.675*width), round(0.15*height))
        self.shawZraw.clicked.connect(self.Shaw_Z_Data)
        self.shawZraw.setStyleSheet(self.button_style)
        self.shawZraw.setEnabled(False)

        # Shaw Z Analyzed Data button
        self.shawZfit = QPushButton(self)
        self.shawZfit.setText("Hide auto-Fit")
        self.shawZfit.resize(round(0.07*width), round(0.04*height))
        self.shawZfit.move(round(0.675*width), round(0.195*height))
        self.shawZfit.clicked.connect(self.Shaw_Z_Fit)
        self.shawZfit.setStyleSheet(self.button_style)
        self.shawZfit.setEnabled(False)
        #
        self.shawZfit2 = QPushButton(self)
        self.shawZfit2.setText("Hide sel-Fit")
        self.shawZfit2.resize(round(0.07*width), round(0.04*height))
        self.shawZfit2.move(round(0.675*width), round(0.24*height))
        self.shawZfit2.clicked.connect(self.Shaw_Z_Fit2)
        self.shawZfit2.setStyleSheet(self.button_style)
        self.shawZfit2.setEnabled(False)

        # Reset Z Plot button
        self.resetZplot = QPushButton(self)
        self.resetZplot.setText("Reset axes")
        self.resetZplot.resize(round(0.07*width), round(0.04*height))
        self.resetZplot.move(round(0.675*width), round(0.51*height))
        self.resetZplot.clicked.connect(lambda: self.ZPlot.getPlotItem().enableAutoRange())
        self.resetZplot.setStyleSheet(self.button_style)
        self.resetZplot.setEnabled(False)

        
        #########################################################################
        # RESULTS LABEL

        # Rectangle line
        self.lines = QLabel(self)
        self.lines.move(round(0.02*width), round(0.63*height))
        self.lines.resize(round(0.725*width), round(0.3*height))
        self.lines.setStyleSheet(self.line_style)

        # Equivalence buttons
        self.to_we = QPushButton(self)
        self.to_we.setCheckable(True)
        self.to_we.setChecked(True)
        self.to_we.setText("Water")
        self.to_we.resize(round(0.075*width), round(0.04*height))
        self.to_we.move(round(0.04*width), round(0.7*height))
        self.to_we.clicked.connect(self.Change_Equivalence_we)
        self.to_we.setStyleSheet(self.button_style)
        self.to_we.setEnabled(True)
        #
        self.to_eyetissue = QPushButton(self)
        self.to_eyetissue.setCheckable(True)
        self.to_eyetissue.setText("Eye tissue")
        self.to_eyetissue.resize(round(0.075*width), round(0.04*height))
        self.to_eyetissue.move(round(0.04*width), round(0.75*height))
        self.to_eyetissue.clicked.connect(self.Change_Equivalence_eyetissue)
        self.to_eyetissue.setStyleSheet(self.button_style)
        self.to_eyetissue.setEnabled(True)
        #
        self.to_perspex = QPushButton(self)
        self.to_perspex.setCheckable(True)
        self.to_perspex.setText("Perspex")
        self.to_perspex.resize(round(0.075*width), round(0.04*height))
        self.to_perspex.move(round(0.04*width), round(0.8*height))
        self.to_perspex.clicked.connect(self.Change_Equivalence_perspex)
        self.to_perspex.setStyleSheet(self.button_style)
        self.to_perspex.setEnabled(True)

        # line
        self.lines = QLabel(self)
        self.lines.move(round(0.14*width), round(0.67*height))
        self.lines.resize(round(0.002*width), round(0.24*height))
        self.lines.setStyleSheet(self.line_style)
        
        # Profile Z
        self.labelResultsZt = QLabel(self)
        self.labelResultsZt.move(round(0.3*width), round(0.6*height))
        self.labelResultsZt.resize(round(0.4*width), round(0.08*height))
        self.labelResultsZt.setText('Analysis results\n\n\tautomatic:\t\t  selected:')
        self.labelResultsZt.setFont(textstyle2)
        self.labelResultsZt.setStyleSheet('background-color: None')
        #
        self.labelResultsZt = QLabel(self)
        self.labelResultsZt.move(round(0.16*width), round(0.65*height))
        self.labelResultsZt.resize(round(0.16*width), round(0.3*height))
        self.labelResultsZt.setText('Window\'s range [ch]:\n\nWindow\'s range [equivalent mm]:\n\nPeak position:\n\nPeak-plateau ratio:\n\nClinical range (R{:d}):\n\nPeak width (@{:d}%):\n\nEntrance dose:'.format(int(CLINICAL_RANGE_PERC*100), int(PEAK_WIDTH_PERC*100)))
        self.labelResultsZt.setFont(textstyle)
        self.labelResultsZt.setStyleSheet('background-color: None')
        #
        self.labelResultsZ = QLabel(self)
        self.labelResultsZ.move(round(0.37*width), round(0.65*height))
        self.labelResultsZ.resize(round(0.12*width), round(0.3*height))
        self.labelResultsZ.setText('--\n\n--\n\n--\n\n--\n\n--\n\n--\n\n--')
        self.labelResultsZ.setFont(textstyle)
        self.labelResultsZ.setStyleSheet('background-color: None')
        #
        self.labelResultsZm = QLabel(self)
        self.labelResultsZm.move(round(0.51*width), round(0.65*height))
        self.labelResultsZm.resize(round(0.12*width), round(0.3*height))
        self.labelResultsZm.setText('--\n\n--\n\n--\n\n--\n\n--\n\n--\n\n--')
        self.labelResultsZm.setFont(textstyle)
        self.labelResultsZm.setStyleSheet('background-color: None')

        # line
        self.lines = QLabel(self)
        self.lines.move(round(0.6*width), round(0.67*height))
        self.lines.resize(round(0.002*width), round(0.24*height))
        self.lines.setStyleSheet(self.line_style)

        # label
        self.label = QLabel(self) 
        self.label.setText("Insert file name:")
        self.label.move(round(0.635*width), round(0.72*height))
        self.label.resize(round(0.1*width), round(0.04*height))
        self.label.setStyleSheet('border: 1px solid gray; border: None')

        # textbox nome file
        self.textbox = QLineEdit(self)
        self.textbox.move(round(0.61*width), round(0.75*height))
        self.textbox.resize(round(0.125*width), round(0.04*height))
        self.textbox.setStyleSheet('background-color: white')
        self.textbox.setEnabled(False)

        # Save button
        self.savebutton = QPushButton(self)
        self.savebutton.setText("Save")
        self.savebutton.move(round(0.63*width), round(0.83*height))
        self.savebutton.resize(round(0.075*width), round(0.04*height))
        self.savebutton.clicked.connect(self.Savefile)
        self.savebutton.setStyleSheet(self.button_style)
        self.savebutton.setEnabled(False)
        

        #########################################################################
        # RIGHT SIDE

        # Z File load button
        self.loadZdata = QPushButton(self)
        self.loadZdata.setText("Load Z Data")
        self.loadZdata.resize(round(0.2*width), round(0.05*height))
        self.loadZdata.move(round(0.78*width), round(0.12*height))
        self.loadZdata.clicked.connect(self.Load_Z_Data)
        self.loadZdata.setStyleSheet(self.button_style)
        
        # Z File label
        self.labelZfile = QLabel(self) 
        self.labelZfile.setText("File IN Z:")
        self.labelZfile.resize(round(0.045*width), round(0.03*height))
        self.labelZfile.move(round(0.79*width), round(0.18*height))
        self.labelZfile.setStyleSheet('border: 1px solid gray; border: None')
        #
        self.labelZfile = QLabel(self) 
        self.labelZfile.setText('')
        self.labelZfile.resize(round(0.135*width), round(0.03*height))
        self.labelZfile.move(round(0.835*width), round(0.18*height))
        self.labelZfile.setStyleSheet('background-color: lightgray; border: None')

        # line
        self.lines = QLabel(self)
        self.lines.resize(round(0.21*width), round(0.003*height))
        self.lines.move(round(0.775*width), round(0.23*height))
        self.lines.setStyleSheet(self.line_style)

        # Background load button
        self.loadbkg = QPushButton(self)
        self.loadbkg.setText("Load Background")
        self.loadbkg.resize(round(0.2*width), round(0.05*height))
        self.loadbkg.move(round(0.78*width), round(0.25*height))
        self.loadbkg.clicked.connect(self.Load_Background)
        self.loadbkg.setStyleSheet(self.button_style)
        self.loadbkg.setEnabled(False)

        # Background label
        self.labelbkg = QLabel(self) 
        self.labelbkg.setText("BKG file:")  
        self.labelbkg.resize(round(0.045*width), round(0.03*height))
        self.labelbkg.move(round(0.79*width), round(0.31*height))
        self.labelbkg.setStyleSheet('border: 1px solid gray; border: None')
        #
        self.labelbkg = QLabel(self) 
        self.labelbkg.setText('')
        self.labelbkg.resize(round(0.135*width), round(0.03*height))
        self.labelbkg.move(round(0.835*width), round(0.31*height))
        self.labelbkg.setStyleSheet('background-color: lightgray; None')

        # Remove Background button
        self.removebkg = QPushButton(self)
        self.removebkg.setCheckable(True)
        self.removebkg.setText("Remove BKG from data")
        self.removebkg.resize(round(0.16*width), round(0.03*height))
        self.removebkg.move(round(0.8*width), round(0.35*height))
        self.removebkg.clicked.connect(self.Remove_Background)
        self.removebkg.setStyleSheet(self.button_style)
        self.removebkg.setEnabled(False)

        # line
        self.lines = QLabel(self)
        self.lines.resize(round(0.21*width), round(0.003*height))
        self.lines.move(round(0.775*width), round(0.4*height))
        self.lines.setStyleSheet(self.line_style)

        # Z Calibration load button
        self.loadZcalib = QPushButton(self)
        self.loadZcalib.setText("Load Z Calibration file")
        self.loadZcalib.resize(round(0.2*width), round(0.05*height))
        self.loadZcalib.move(round(0.78*width), round(0.42*height))
        self.loadZcalib.clicked.connect(self.Load_Z_Calibration)
        self.loadZcalib.setStyleSheet(self.button_style)
        self.loadZcalib.setEnabled(False)

        # Z Calib label 
        self.labelZcalib = QLabel(self) 
        self.labelZcalib.setText("Calib Z:")  
        self.labelZcalib.resize(round(0.045*width), round(0.03*height))
        self.labelZcalib.move(round(0.79*width), round(0.48*height))
        self.labelZcalib.setStyleSheet('border: 1px solid gray; border: None')
        #
        self.labelZcalib = QLabel(self) 
        self.labelZcalib.setText('')
        self.labelZcalib.resize(round(0.135*width), round(0.03*height))
        self.labelZcalib.move(round(0.835*width), round(0.48*height))
        self.labelZcalib.setStyleSheet('background-color: lightgray; None')

        # Enable Z Calib switch button
        self.enableZcalib = QPushButton(self)
        self.enableZcalib.setCheckable(True)
        self.enableZcalib.setText("Apply calib Z")
        self.enableZcalib.resize(round(0.16*width), round(0.03*height))
        self.enableZcalib.move(round(0.8*width), round(0.52*height))
        self.enableZcalib.clicked.connect(self.Apply_Z_Calib)
        self.enableZcalib.setStyleSheet(self.button_style)
        self.enableZcalib.setEnabled(False)

        # line
        self.lines = QLabel(self)
        self.lines.resize(round(0.21*width), round(0.003*height))
        self.lines.move(round(0.775*width), round(0.57*height))
        self.lines.setStyleSheet(self.line_style)

        # Manual choose button
        self.manualbutton = QPushButton(self)
        self.manualbutton.setText("Select window manually")
        self.manualbutton.resize(round(0.2*width), round(0.05*height))
        self.manualbutton.move(round(0.78*width), round(0.59*height))
        self.manualbutton.clicked.connect(self.ManualWindow)
        self.manualbutton.setStyleSheet(self.button_style)
        self.manualbutton.setEnabled(False)

        # Windows edges label
        self.leftlabel = QLabel(self) 
        self.leftlabel.setText('left edge:\t0 ch\t0 eq. mm\nright edge:\t0 ch\t0 eq. mm')
        self.leftlabel.resize(round(0.2*width), round(0.05*height))
        self.leftlabel.move(round(0.79*width), round(0.65*height))
        self.leftlabel.setStyleSheet('border: None')

        # Manual window button
        self.manual_window = QPushButton(self)
        self.manual_window.setCheckable(True)
        self.manual_window.setText("Set window's edges")
        self.manual_window.resize(round(0.16*width), round(0.03*height))
        self.manual_window.move(round(0.8*width), round(0.71*height))
        self.manual_window.clicked.connect(self.Set_Windows_edge)
        self.manual_window.setStyleSheet(self.button_style)
        self.manual_window.setEnabled(False)

        # line
        self.lines = QLabel(self)
        self.lines.resize(round(0.21*width), round(0.003*height))
        self.lines.move(round(0.775*width), round(0.76*height))
        self.lines.setStyleSheet(self.line_style)

        # Reset All button
        self.resetall = QPushButton(self)
        self.resetall.setText("Reset all")
        self.resetall.resize(round(0.16*width), round(0.03*height))
        self.resetall.move(round(0.8*width), round(0.78*height))
        self.resetall.clicked.connect(self.Reset_all)
        self.resetall.setStyleSheet(self.reset_style)

        # Analyze button
        self.analyze = QPushButton(self)
        self.analyze.setText("ANALYZE")
        self.analyze.setFont(textstyle)
        self.analyze.resize(round(0.2*width), round(0.1*height))
        self.analyze.move(round(0.78*width), round(0.82*height))
        self.analyze.clicked.connect(self.Analyze)
        self.analyze.setStyleSheet(self.analyze_style)
        self.analyze.setEnabled(False)

        #########################################################################

        
    
    ########################################################################################################################################
    def Load_Z_Data(self):

        self.Reset_all()
        
        try:
            '''
            data =np.loadtxt('/Users/lucafeneziani/Desktop/QEYE_App/data/mlfc/Clatter - modificati e funzionanti/20220929_135127_profileZ.dat', dtype=str, delimiter = '\t')
            '''
            file = QFileDialog.getOpenFileName(self, os.getcwd())[0]
            data = np.loadtxt(file, dtype=str, delimiter='\t')
            self.labelZfile.setText(file.split('/')[-1])
            
            self.Z_Time = data[-1][0].astype(float)
            self.Z_Data = data[-1][1::].astype(float)*-1

            self.Z_data_x = range(len(self.Z_Data))
            self.Z_data_y = self.Z_Data
            self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            self.ZPlot.getPlotItem().enableAutoRange()

            self.shawZraw.setEnabled(True)
            self.loadZcalib.setEnabled(True)
            self.analyze.setEnabled(True)
            self.resetZplot.setEnabled(True)
            self.manualbutton.setEnabled(True)
            self.loadbkg.setEnabled(True)
        
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('Unrecognized data format - Check the upload')
            msg.exec_()

        return


    def Load_Background(self):

        if self.removebkg.isChecked():
            self.Z_data_y = self.Z_data_y + self.BKG_Data
            self.ZPlot.removeItem(self.Zraw)
            self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            self.removebkg.setChecked(False)

        self.labelbkg.setText('')
        self.removebkg.setEnabled(False)

        try:
            file = QFileDialog.getOpenFileName(self, os.getcwd())[0]
            data = np.loadtxt(file, dtype=str, delimiter='\t')
            self.labelbkg.setText(file.split('/')[-1])
            
            self.BKG_Time = data[-1][0].astype(float)
            self.BKG_Data = data[-1][1::].astype(float) * -1 / self.BKG_Time * self.Z_Time

            self.removebkg.setEnabled(True)

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('Unrecognized data format - Check the upload')
            msg.exec_()

        return
    

    def Remove_Background(self):

        try:
            if self.removebkg.isChecked():
                self.Z_data_y = self.Z_data_y - self.BKG_Data
                self.ZPlot.removeItem(self.Zraw)
                self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
                self.removebkg.setText("BKG removed from data")
            else:
                self.Z_data_y = self.Z_data_y + self.BKG_Data
                self.ZPlot.removeItem(self.Zraw)
                self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
                self.removebkg.setText("Remove BKG from data")

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('Error during background removal')
            msg.exec_()

        return


    def Load_Z_Calibration(self):

        if self.enableZcalib.isChecked():
            self.Z_data_y = self.Z_data_y / self.calibZ_vector
            self.ZPlot.removeItem(self.Zraw)
            self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            self.enableZcalib.setChecked(False)

        self.labelZcalib.setText('')
        self.enableZcalib.setEnabled(False)

        try:
            file = QFileDialog.getOpenFileName(self, os.getcwd())[0]
            data = np.loadtxt(file, dtype=str, delimiter = '\t')
            self.labelZcalib.setText(file.split('/')[-1])

            self.calibZ_vector = np.transpose(data)[1][1::].astype(float)

            self.enableZcalib.setEnabled(True)

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('Unrecognized data format - Check the upload')
            msg.exec_()
        
        return


    def Apply_Z_Calib(self):

        try:
            if self.enableZcalib.isChecked():
                self.Z_data_y = self.Z_data_y * self.calibZ_vector
                self.ZPlot.removeItem(self.Zraw)
                self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            else:
                self.Z_data_y = self.Z_data_y / self.calibZ_vector
                self.ZPlot.removeItem(self.Zraw)
                self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('Error during calibration applying')
            msg.exec_()

        return
    

    def ManualWindow(self):
        self.ZPlot.clear()

        self.Z_data_x = range(len(self.Z_Data))

        self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
        self.ZPlot.setTitle('Profile Z total counts')
        self.ZPlot.setLabel('bottom','channels')
        self.ZPlot.setLabel('left','counts')
        self.ZPlot.getPlotItem().enableAutoRange()

        self.leftline = pg.InfiniteLine(pos=self.Z_data_x[0], pen=self.pen_roi, angle=90, movable=True)
        self.leftlinelabel = pg.InfLineLabel(self.leftline, text=str(self.leftline.value()), position=0.95)
        self.rightline = pg.InfiniteLine(pos=self.Z_data_x[-1], pen=self.pen_roi, angle=90, movable=True)
        self.rightlinelabel = pg.InfLineLabel(self.rightline, text=str(self.rightline.value()), position=0.9)
        self.leftline.sigPositionChanged.connect(self.Update_label)
        self.rightline.sigPositionChanged.connect(self.Update_label)
        
        self.ZPlot.addItem(self.leftline)
        self.ZPlot.addItem(self.rightline)

        self.manual_window.setEnabled(True)
        self.leftlabel.setText('left edge:\t0 ch\t0 eq. mm\nright edge:\t0 ch\t0 eq. mm')
        self.shawZfit.setEnabled(False)
        self.shawZfit2.setEnabled(False)
        self.manual_window.setChecked(False)
        
        return

    def Update_label(self):
        self.leftlinelabel.setText(str(int(self.leftline.value())))
        self.rightlinelabel.setText(str(int(self.rightline.value())))
        self.manual_window.setChecked(False)
        self.leftlabel.setText('left edge:\t0 ch\t0 eq. mm\nright edge:\t0 ch\t0 eq. mm')
        return

    def Set_Windows_edge(self):
        
        if self.manual_window.isChecked():
            
            line1 = int(self.leftline.value())
            line2 = int(self.rightline.value())
            left = min(line1,line2)
            right = max(line1,line2)
            self.leftlabel.setText('left edge:\t{} ch\t{:.2f} eq. mm\nright edge:\t{} ch\t{:.2f} eq. mm'.format(left,left*self.to_equivalence,right,right*self.to_equivalence))
        
            self.analysis_window = [left, right]
        
        else:
            self.analysis_window = False
            self.leftlabel.setText('left edge:\t0 ch\t0 eq. mm\nright edge:\t0 ch\t0 eq. mm')

        return
    

    def Shaw_Z_Data(self):
        if self.Zraw.isVisible():
            self.Zraw.hide()
            self.shawZraw.setText("Show Data")
        else:
            self.Zraw.show()
            self.shawZraw.setText("Hide Data")
        return
    
    
    def Shaw_Z_Fit(self):
        if self.Zfit.isVisible():
            self.Zfit.hide()
            self.shawZfit.setText("Show auto-Fit")
        else:
            self.Zfit.show()
            self.shawZfit.setText("Hide auto-Fit")
        return
    
    def Shaw_Z_Fit2(self):
        if self.Zfit2.isVisible():
            self.Zfit2.hide()
            self.shawZfit2.setText("Show sel-Fit")
        else:
            self.Zfit2.show()
            self.shawZfit2.setText("Hide sel-Fit")
        return
    
    
    def Change_Equivalence_we(self):
        self.to_we.setChecked(True)
        self.to_eyetissue.setChecked(False)
        self.to_perspex.setChecked(False)
        self.to_equivalence = TO_WE
        self.Analyze()
        return
    

    def Change_Equivalence_eyetissue(self):
        self.to_we.setChecked(False)
        self.to_eyetissue.setChecked(True)
        self.to_perspex.setChecked(False)
        self.to_equivalence = TO_EYETISSUE
        self.Analyze()
        return
    

    def Change_Equivalence_perspex(self):
        self.to_we.setChecked(False)
        self.to_eyetissue.setChecked(False)
        self.to_perspex.setChecked(True)
        self.to_equivalence = TO_PERSPEX
        self.Analyze()
        return
    
    def Savefile(self):
        self.savebutton.setEnabled(False)
        self.textbox.setEnabled(False)

        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        hour = now.strftime('%H%M%S')
        name = self.textbox.text()
        path = QFileDialog.getExistingDirectory(self, os.getcwd())
        filename = path+'/'+date+'_'+hour+'_'+name+'.txt'
        
        if self.to_we.isChecked():
            eq = 'Water'
        elif self.to_eyetissue.isChecked():
            eq = 'Eye tissue'
        elif self.to_perspex.isChecked():
            eq = 'Perspex'

        f = open(filename, 'w')
        if self.analysis_window != False:
            f.write('Depth dose profile, {} equivalent length\tAutomatic Fit\tSelected range Fit'.format(eq))
            f.write('\nWindow\'s range [ch]:\t[{}, {}]\t[{}, {}]\nWindow\'s range [mm]:\t[{:.2f}, {:.2f}]\t[{}, {}]\nPeak position:\t{:.2f} {}\t{:.2f} {}\nPeak-plateau ratio:\t{:.2f} {}\t{:.2f} {}\nClinical range (R{:d}):\t{:.2f} {}\t{:.2f} {}\nPeak width (@{:d}%):\t{:.2f} {}\t{:.2f} {}\nEntrance dose:\t{:.2f} {}\t{:.2f} {}'.format(
                            self.Zres_auto['windows_range'][0],self.Zres_auto['windows_range'][1], self.Zres_man['windows_range'][0],self.Zres_man['windows_range'][1],
                            self.Zres_auto['windows_range'][0]*self.to_equivalence,self.Zres_auto['windows_range'][1]*self.to_equivalence, self.Zres_man['windows_range'][0]*self.to_equivalence,self.Zres_man['windows_range'][1]*self.to_equivalence,
                            self.Zres_auto['peak_pos']['value'],self.Zres_auto['peak_pos']['unit'], self.Zres_man['peak_pos']['value'],self.Zres_man['peak_pos']['unit'],
                            self.Zres_auto['pp_ratio']['value'],self.Zres_auto['pp_ratio']['unit'], self.Zres_man['pp_ratio']['value'],self.Zres_man['pp_ratio']['unit'],
                            int(CLINICAL_RANGE_PERC*100),self.Zres_auto['cl_range']['value'],self.Zres_auto['cl_range']['unit'], self.Zres_man['cl_range']['value'],self.Zres_man['cl_range']['unit'],
                            int(PEAK_WIDTH_PERC*100),self.Zres_auto['peak_width']['value'],self.Zres_auto['peak_width']['unit'], self.Zres_man['peak_width']['value'],self.Zres_man['peak_width']['unit'],
                            self.Zres_auto['entrance_dose']['value'],self.Zres_auto['entrance_dose']['unit'], self.Zres_man['entrance_dose']['value'],self.Zres_man['entrance_dose']['unit'],
                            ))
            f.write('\n\n{} equivalent length\tAutomatic Fit\tSelected range Fit'.format(eq))
            for i in range(len(self.Zres_auto['coordinates_raw'])):
                f.write('\n{:.2f}\t{:.2f}\t{:.2f}'.format(self.Zres_auto['coordinates_raw'][i], self.Zres_auto['fit_data'][i], self.Zres_man['fit_data'][i]))
        else:
            f.write('Depth dose profile, {} equivalent length\tAutomatic Fit'.format(eq))
            f.write('\nWindow\'s range [ch]:\t[{}, {}]\nWindow\'s range [mm]:\t[{:.2f}, {:.2f}]\nPeak position:\t{:.2f} {}\nPeak-plateau ratio:\t{:.2f} {}\nClinical range (R{:d}):\t{:.2f} {}\nPeak width (@{:d}%):\t{:.2f} {}\nEntrance dose:\t{:.2f} {}'.format(
                            self.Zres_auto['windows_range'][0], self.Zres_auto['windows_range'][1],
                            self.Zres_auto['windows_range'][0]*self.to_equivalence,self.Zres_auto['windows_range'][1]*self.to_equivalence,
                            self.Zres_auto['peak_pos']['value'],self.Zres_auto['peak_pos']['unit'],
                            self.Zres_auto['pp_ratio']['value'],self.Zres_auto['pp_ratio']['unit'],
                            int(CLINICAL_RANGE_PERC*100),self.Zres_auto['cl_range']['value'],self.Zres_auto['cl_range']['unit'],
                            int(PEAK_WIDTH_PERC*100),self.Zres_auto['peak_width']['value'],self.Zres_auto['peak_width']['unit'],
                            self.Zres_auto['entrance_dose']['value'],self.Zres_auto['entrance_dose']['unit'],
                            ))
            f.write('\n\n{} equivalent length\tAutomatic Fit'.format(eq))
            for i in range(len(self.Zres_auto['coordinates_raw'])):
                f.write('\n{:.2f}\t{:.2f}'.format(self.Zres_auto['coordinates_raw'][i], self.Zres_auto['fit_data'][i]))
        f.close()

        return


    def Reset_all(self):

        # Plot
        self.ZPlot.clear()
        self.ZPlot.setTitle('Profile Z total counts')
        self.ZPlot.setLabel('bottom','channels')
        self.ZPlot.setLabel('left','counts')

        # Data
        self.Z_Data = []

        # Variables
        self.to_we.setChecked(True)
        self.to_eyetissue.setChecked(False)
        self.to_perspex.setChecked(False)
        self.removebkg.setChecked(False)
        self.manual_window.setChecked(False)
        self.enableZcalib.setChecked(False)
        self.analysis_window = False

        # button
        self.shawZraw.setEnabled(False)
        self.shawZfit.setEnabled(False)
        self.shawZfit2.setEnabled(False)
        self.loadbkg.setEnabled(False)
        self.removebkg.setEnabled(False)
        self.loadZcalib.setEnabled(False)
        self.enableZcalib.setEnabled(False)
        self.analyze.setEnabled(False)
        self.resetZplot.setEnabled(False)
        self.manualbutton.setEnabled(False)
        self.manual_window.setEnabled(False)
        self.savebutton.setEnabled(False)

        # Label
        self.shawZraw.setText("Hide Data")
        self.shawZfit.setText("Hide auto-Fit")
        self.shawZfit2.setText("Hide sel-Fit")
        self.labelZfile.setText('')
        self.labelbkg.setText('')
        self.labelZcalib.setText('')
        self.labelResultsZ.setText('--\n\n--\n\n--\n\n--\n\n--\n\n--\n\n--')
        self.labelResultsZm.setText('--\n\n--\n\n--\n\n--\n\n--\n\n--\n\n--')
        self.leftlabel.setText('left edge:\t0 ch\t0 eq. mm\nright edge:\t0 ch\t0 eq. mm')
        self.removebkg.setText("Remove BKG from data")
        self.textbox.setText("")
        self.textbox.setEnabled(False)
        
        return
    
    def Analyze(self):

        # MLFC Analysis
        try:
            self.Zres_auto = functions.mlfc_analysis(self.Z_data_y, False, self.to_equivalence)
            
            self.ZPlot.clear()
            self.ZPlot.setTitle('Profile Z dose')
            self.ZPlot.setLabel('bottom','depth','equivalent mm')
            self.ZPlot.setLabel('left','%')
            self.labelResultsZm.setText('--\n\n--\n\n--\n\n--\n\n--\n\n--\n\n--')

            self.Zraw = self.ZPlot.plot(self.Zres_auto['coordinates_raw'], self.Zres_auto['raw_data']/np.max(self.Zres_auto['raw_data'])*100, pen = self.pen_data)
            self.Zfit = self.ZPlot.plot(self.Zres_auto['coordinates_fit'], self.Zres_auto['fit_data'], pen = self.pen_fit)
            self.shawZfit.setEnabled(True)
            self.labelResultsZ.setText('[{}, {}]\n\n[{:.2f}, {:.2f}]\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}'.format(self.Zres_auto['windows_range'][0],self.Zres_auto['windows_range'][1],
                                                                                                                                    self.Zres_auto['windows_range'][0]*self.to_equivalence,self.Zres_auto['windows_range'][1]*self.to_equivalence,
                                                                                                                                    self.Zres_auto['peak_pos']['value'],self.Zres_auto['peak_pos']['unit'],
                                                                                                                                    self.Zres_auto['pp_ratio']['value'],self.Zres_auto['pp_ratio']['unit'],
                                                                                                                                    self.Zres_auto['cl_range']['value'],self.Zres_auto['cl_range']['unit'],
                                                                                                                                    self.Zres_auto['peak_width']['value'],self.Zres_auto['peak_width']['unit'],
                                                                                                                                    self.Zres_auto['entrance_dose']['value'],self.Zres_auto['entrance_dose']['unit']))
        
            if self.analysis_window != False:
                self.Zres_man = functions.mlfc_analysis(self.Z_data_y, self.analysis_window, self.to_equivalence)
                self.Zfit2 = self.ZPlot.plot(self.Zres_man['coordinates_fit'], self.Zres_man['fit_data'], pen = self.pen_fit2)
                self.shawZfit2.setEnabled(True)
                self.labelResultsZm.setText('[{}, {}]\n\n[{:.2f}, {:.2f}]\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}'.format(self.Zres_man['windows_range'][0],self.Zres_man['windows_range'][1],
                                                                                                                                            self.Zres_man['windows_range'][0]*self.to_equivalence,self.Zres_man['windows_range'][1]*self.to_equivalence,
                                                                                                                                            self.Zres_man['peak_pos']['value'],self.Zres_man['peak_pos']['unit'],
                                                                                                                                            self.Zres_man['pp_ratio']['value'],self.Zres_man['pp_ratio']['unit'],
                                                                                                                                            self.Zres_man['cl_range']['value'],self.Zres_man['cl_range']['unit'],
                                                                                                                                            self.Zres_man['peak_width']['value'],self.Zres_man['peak_width']['unit'],
                                                                                                                                            self.Zres_man['entrance_dose']['value'],self.Zres_man['entrance_dose']['unit']))
        
            self.ZPlot.getPlotItem().enableAutoRange()

            self.textbox.setText("")
            self.textbox.setEnabled(True)
            self.savebutton.setEnabled(True)
        
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('Analysis ended with error')
            msg.exec_()
            
        if self.analysis_window == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Results")
            msg.setInformativeText('Suggested results shawn.\nIf you want to change the analysis parameters, set the window\'s edges')
            msg.exec_()
                


        return