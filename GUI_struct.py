import numpy as np
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QPushButton, QLabel, QFileDialog
import pyqtgraph as pg
import os

import functions
import configuration_params


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
        # ENABLE/DISABLE VARIABLES

        self.mlfc_enable     = False
        self.bortfeld_enable = False
        self.calibZ_enable   = False
        self.isflipped       = False
        self.Zdataplot       = False
        self.Zfitplot        = False

        #########################################################################
        # GUI STYLE
        
        button_style = 'background-color: None'
        enable_style = 'background-color: None'
        textstyle = QFont()
        textstyle.setBold(True)
        textstyle2 = QFont(None,15)
        textstyle2.setBold(True)
        self.pen_data = pg.mkPen(color=(255, 0, 0), width=3)
        self.pen_fit = pg.mkPen(color=(0, 0, 255), width=3, style=Qt.DashLine)

        #########################################################################
        # CONFIGURATION PARAMS

        self.detector_params  = configuration_params.configs

        #########################################################################
        # TOP

        # Bar
        self.barlabel = QLabel(self)
        self.pixmap = QPixmap('/Users/lucafeneziani/Desktop/QEYE_App/images/bar.png')
        self.barlabel.setPixmap(self.pixmap)
        self.barlabel.resize(round(width), round(0.08*height))
        self.barlabel.move(round(0.0*width), round(0.0*height))

        # De.Tec.Tor Logo
        self.logolabel = QLabel(self)
        self.pixmap = QPixmap('/Users/lucafeneziani/Desktop/QEYE_App/images/DeTecTor.png')
        self.pixmap = self.pixmap.scaled(round(0.25*width), round(0.1*height),Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.logolabel.setPixmap(self.pixmap)
        self.logolabel.resize(round(0.27*width), round(0.08*height))
        self.logolabel.move(round(0.73*width), round(0.0*height))
        self.logolabel.setStyleSheet('background-color: None')

        # Device logo
        self.logolabel = QLabel(self)
        self.pixmap = QPixmap('/Users/lucafeneziani/Desktop/QEYE_App/images/detectors/logo_QEYE.png')
        self.pixmap = self.pixmap.scaled(round(0.15*width), round(0.1*height),Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.logolabel.setPixmap(self.pixmap)
        self.logolabel.resize(round(0.27*width), round(0.08*height))
        self.logolabel.move(round(0.05*width), round(0.0*height))
        self.logolabel.setStyleSheet('background-color: None')

        #########################################################################
        # LEFT SIDE

        # Z Plot
        self.ZPlot = pg.PlotWidget(self)
        self.ZPlot.resize(round(0.65*width), round(0.45*height))
        self.ZPlot.move(round(0.02*width), round(0.15*height))
        self.ZPlot.setBackground('w')

        # Shaw Z Raw Data button
        self.shawZraw = QPushButton(self)
        self.shawZraw.setText("Raw Data")
        self.shawZraw.resize(round(0.07*width), round(0.05*height))
        self.shawZraw.move(round(0.67*width), round(0.15*height))
        self.shawZraw.clicked.connect(self.Shaw_Z_Data)
        self.shawZraw.setStyleSheet(button_style)
        self.shawZraw.setEnabled(False)

        # Shaw Z Analyzed Data button
        self.shawZfit = QPushButton(self)
        self.shawZfit.setText("Fit Data")
        self.shawZfit.resize(round(0.07*width), round(0.05*height))
        self.shawZfit.move(round(0.67*width), round(0.20*height))
        self.shawZfit.clicked.connect(self.Shaw_Z_Fit)
        self.shawZfit.setStyleSheet(button_style)
        self.shawZfit.setEnabled(False)

        # Reset Z Plot button
        self.resetZplot = QPushButton(self)
        self.resetZplot.setText("Reset axes")
        self.resetZplot.resize(round(0.07*width), round(0.05*height))
        self.resetZplot.move(round(0.67*width), round(0.55*height))
        self.resetZplot.clicked.connect(lambda: self.ZPlot.getPlotItem().enableAutoRange())
        self.resetZplot.setStyleSheet(button_style)
        self.resetZplot.setEnabled(False)

        
        #########################################################################
        # RESULTS LABEL

        self.labelResults = QLabel(self)
        self.labelResults.move(round(0.02*width), round(0.65*height))
        self.labelResults.resize(round(0.75*width), round(0.25*height))
        self.labelResults.setStyleSheet('background-color: None; border: 2px solid blue; border-radius: 10px')
        
        # Profile Z
        self.labelResultsZt = QLabel(self)
        self.labelResultsZt.move(round(0.29*width), round(0.65*height))
        self.labelResultsZt.resize(round(0.15*width), round(0.07*height))
        self.labelResultsZt.setText('\t\tProfile Z')
        self.labelResultsZt.setFont(textstyle2)
        self.labelResultsZt.setStyleSheet('background-color: None')
        #
        self.labelResultsZt = QLabel(self)
        self.labelResultsZt.move(round(0.29*width), round(0.65*height))
        self.labelResultsZt.resize(round(0.15*width), round(0.25*height))
        self.labelResultsZt.setText('\n\n\nPeak position:\n\nPeak-plateau ratio:\n\nClinical range (R80):\n\nPeak width (@80%):')
        self.labelResultsZt.setFont(textstyle)
        self.labelResultsZt.setStyleSheet('background-color: None')
        #
        self.labelResultsZ = QLabel(self)
        self.labelResultsZ.move(round(0.44*width), round(0.65*height))
        self.labelResultsZ.resize(round(0.10*width), round(0.25*height))
        self.labelResultsZ.setText('\n\n\n--\n\n--\n\n--\n\n--')
        self.labelResultsZ.setFont(textstyle)
        self.labelResultsZ.setStyleSheet('background-color: None')
        

        #########################################################################
        # RIGHT SIDE

        # Z File load button
        self.loadZdata = QPushButton(self)
        self.loadZdata.setText("Load Z Data")
        self.loadZdata.resize(round(0.2*width), round(0.05*height))
        self.loadZdata.move(round(0.79*width), round(0.2*height))
        self.loadZdata.clicked.connect(self.Load_Z_Data)
        self.loadZdata.setStyleSheet(button_style)

        # Z File label
        self.labelZfile = QLabel(self) 
        self.labelZfile.setText("File IN Z:")
        self.labelZfile.resize(round(0.045*width), round(0.03*height))
        self.labelZfile.move(round(0.8*width), round(0.25*height))
        self.labelZfile.setStyleSheet('border: 1px solid gray; border: None')
        #
        self.labelZfile = QLabel(self) 
        self.labelZfile.setText('')
        self.labelZfile.resize(round(0.135*width), round(0.03*height))
        self.labelZfile.move(round(0.845*width), round(0.25*height))
        self.labelZfile.setStyleSheet('background-color: lightgray; border: None')

        # Z File reverse button
        self.reverseZdata = QPushButton(self)
        self.reverseZdata.setText("Reverse Z Data")
        self.reverseZdata.resize(round(0.2*width), round(0.05*height))
        self.reverseZdata.move(round(0.79*width), round(0.3*height))
        self.reverseZdata.clicked.connect(self.Reverse_Z_Data)
        self.reverseZdata.setStyleSheet(button_style)
        self.reverseZdata.setEnabled(False)

        # Enable Z switch button
        self.enableZ = QPushButton(self)
        self.enableZ.setText("Enable Z")
        self.enableZ.resize(round(0.1*width), round(0.05*height))
        self.enableZ.move(round(0.79*width), round(0.35*height))
        self.enableZ.clicked.connect(self.Enable_Z)
        self.enableZ.setStyleSheet(enable_style)
        self.enableZ.setEnabled(False)

        # Z Calibration load button
        self.loadZcalib = QPushButton(self)
        self.loadZcalib.setText("Load Z Calib")
        self.loadZcalib.resize(round(0.2*width), round(0.05*height))
        self.loadZcalib.move(round(0.79*width), round(0.42*height))
        self.loadZcalib.clicked.connect(self.Load_Z_Calibration)
        self.loadZcalib.setStyleSheet(button_style)
        self.loadZcalib.setEnabled(False)

        # Z Calib label 
        self.labelZcalib = QLabel(self) 
        self.labelZcalib.setText("Calib Z:")  
        self.labelZcalib.resize(round(0.045*width), round(0.03*height))
        self.labelZcalib.move(round(0.8*width), round(0.47*height))
        self.labelZcalib.setStyleSheet('border: 1px solid gray; border: None')
        #
        self.labelZcalib = QLabel(self) 
        self.labelZcalib.setText('')
        self.labelZcalib.resize(round(0.135*width), round(0.03*height))
        self.labelZcalib.move(round(0.845*width), round(0.47*height))
        self.labelZcalib.setStyleSheet('background-color: lightgray; None')

        # Enable Z Calib switch button
        self.enableZcalib = QPushButton(self)
        self.enableZcalib.setText("Apply calib Z")
        self.enableZcalib.resize(round(0.1*width), round(0.05*height))
        self.enableZcalib.move(round(0.79*width), round(0.51*height))
        self.enableZcalib.clicked.connect(self.Apply_Z_Calib)
        self.enableZcalib.setStyleSheet(enable_style)
        self.enableZcalib.setEnabled(False)


        # Reset All button
        self.resetall = QPushButton(self)
        self.resetall.setText("Reset all")
        self.resetall.resize(round(0.2*width), round(0.05*height))
        self.resetall.move(round(0.79*width), round(0.7*height))
        self.resetall.clicked.connect(self.Reset_all)
        self.resetall.setStyleSheet('background-color: lightgray; color: red')

        # Analyze button
        self.analyze = QPushButton(self)
        self.analyze.setText("ANALYZE")
        self.analyze.setFont(textstyle)
        self.analyze.resize(round(0.2*width), round(0.1*height))
        self.analyze.move(round(0.79*width), round(0.75*height))
        self.analyze.clicked.connect(self.Analyze)
        self.analyze.setStyleSheet('background-color: lightgreen')
        self.analyze.setEnabled(False)

        #########################################################################

        

    ########################################################################################################################################
    def Load_Z_Data(self):
        '''
        file ='./data/mlfc/20220111_084114_profileZ.dat'
        '''
        file = QFileDialog.getOpenFileName(self, os.getcwd())[0]
        
        data = np.loadtxt(file, dtype=str, delimiter='\t')
        self.labelZfile.setText(file.split('/')[-1])
        
        self.Z_Time = data[-1][0].astype(float)
        self.Z_Data = data[-1][1::].astype(float)*-1

        self.Z_data_x = range(len(self.Z_Data))
        self.Z_data_y = self.Z_Data
        self.ZPlot.clear()
        self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)

        self.shawZraw.setEnabled(True)
        self.reverseZdata.setEnabled(True)
        self.enableZ.setEnabled(True)
        self.loadZcalib.setEnabled(True)
        self.analyze.setEnabled(True)
        self.resetZplot.setEnabled(True)
        self.Zdataplot = True


    def Reverse_Z_Data(self):
        self.Z_data_y = np.flip(self.Z_data_y)
        if self.isflipped:
            self.isflipped = False
        else:
            self.isflipped = True

        self.ZPlot.clear()
        self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)

        self.Zdataplot = True
        if self.Zfitplot:
            self.ZPlot.plot(self.Z_fit_x, self.Z_fit_y, pen = self.pen_fit)
        return
    
    def Enable_Z(self):
        if self.mlfc_enable:
            self.mlfc_enable = False
            self.enableZ.setStyleSheet('background-color: None; color: None')
        else:
            self.mlfc_enable = True
            self.enableZ.setStyleSheet('background-color: None; color: green')
        return


    def Load_Z_Calibration(self):

        file = QFileDialog.getOpenFileName(self, os.getcwd())[0]
        data = np.loadtxt(file, dtype=str, delimiter = '\t')
        self.labelZcalib.setText(file.split('/')[-1])

        self.calibZ_vector_orig = np.transpose(data)[1][1::].astype(float)
        self.calibZ_vector_flip = np.flip(self.calibZ_vector_orig)

        self.enableZcalib.setEnabled(True)
        return
   

    def Apply_Z_Calib(self):
        if self.isflipped:
            self.calibZ_vector = self.calibZ_vector_flip
        else:
            self.calibZ_vector = self.calibZ_vector_orig

        if self.calibZ_enable:
            self.Z_data_y = self.Z_data_y / self.calibZ_vector
            self.ZPlot.clear()
            self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            self.calibZ_enable = False
            self.enableZcalib.setStyleSheet('background-color: None; color: None')
        else:
            self.Z_data_y = self.Z_data_y * self.calibZ_vector
            self.ZPlot.clear()
            self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            self.calibZ_enable = True
            self.enableZcalib.setStyleSheet('background-color: None; color: green')
        return
    
    
    def Shaw_Z_Data(self):
        self.ZPlot.clear()
        if self.Zdataplot:
            self.Zdataplot = False
            if self.Zfitplot:
                self.ZPlot.plot(self.Z_fit_x, self.Z_fit_y, pen = self.pen_fit)
        else:
            self.Zdataplot = True
            self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            if self.Zfitplot:
                self.ZPlot.plot(self.Z_fit_x, self.Z_fit_y, pen = self.pen_fit)
        return
    
    def Shaw_Z_Fit(self):
        self.ZPlot.clear()
        if self.Zfitplot:
            self.Zfitplot = False
            if self.Zdataplot:
                self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
        else:
            self.Zfitplot = True
            if self.Zdataplot:
                self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            self.ZPlot.plot(self.Z_fit_x, self.Z_fit_y, pen = self.pen_fit)
        return
    
    
    def Reset_all(self):

        # Plot
        self.ZPlot.clear()

        # Data
        self.Z_Data = []

        # Variables
        self.mlfc_enable   = False
        self.calibZ_enable = False
        self.isflipped     = False
        self.Zdataplot     = False
        self.Zfitplot      = False

        # Label
        self.labelZfile.setText('')
        self.labelZcalib.setText('')
        self.labelResultsZ.setText('\n\n\n--\n\n--\n\n--\n\n--')
        self.labelResults.setText('')
        self.enableZ.setStyleSheet('background-color: None; color: None')
        self.enableZcalib.setStyleSheet('background-color: None; color: None')

        # button
        self.shawZraw.setEnabled(False)
        self.shawZfit.setEnabled(False)
        self.reverseZdata.setEnabled(False)
        self.enableZ.setEnabled(False)
        self.loadZcalib.setEnabled(False)
        self.enableZcalib.setEnabled(False)
        self.analyze.setEnabled(False)
        self.resetZplot.setEnabled(False)
        
        return
    
    def Analyze(self):

        # MLFC Analysis
        if self.mlfc_enable:

            self.Zres = functions.mlfc_analysis(self.Z_data_y)
            self.Z_data_x = self.Zres['coordinates_raw']
            self.Z_data_y = self.Zres['raw_data']
            self.Z_fit_x = self.Zres['coordinates_fit']
            self.Z_fit_y = self.Zres['fit_data']

            self.ZPlot.clear()
            self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            self.ZPlot.plot(self.Z_fit_x, self.Z_fit_y, pen = self.pen_fit)
            self.shawZfit.setEnabled(True)
            self.Zdataplot = True
            self.Zfitplot = True
            self.labelResultsZ.setText('\n\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}'.format(self.Zres['peak_pos']['value'],self.Zres['peak_pos']['unit'],
                                                                                           self.Zres['pp_ratio']['value'],self.Zres['pp_ratio']['unit'],
                                                                                           self.Zres['cl_range']['value'],self.Zres['cl_range']['unit'],
                                                                                           self.Zres['peak_width']['value'],self.Zres['peak_width']['unit']))
        
        
        return