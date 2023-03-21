import numpy as np
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit
import pyqtgraph as pg
import os

import functions
import configuration_params
from constants import TO_WE, CLINICAL_RANGE_PERC


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
        self.analysis_window = False

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
        self.pen_fit2 = pg.mkPen(color=(0, 200, 0), width=3, style=Qt.DashLine)
        self.pen_roi = pg.mkPen(color=(50,50,50), width=1)

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
        self.ZPlot.setLabel('left','counts')
        self.ZPlot.setLabel('bottom','channels')
        self.ZPlot.setTitle('Profile Z total counts')
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
        self.shawZfit.setText("Auto Fit")
        self.shawZfit.resize(round(0.07*width), round(0.05*height))
        self.shawZfit.move(round(0.67*width), round(0.20*height))
        self.shawZfit.clicked.connect(self.Shaw_Z_Fit)
        self.shawZfit.setStyleSheet(button_style)
        self.shawZfit.setEnabled(False)
        #
        self.shawZfit2 = QPushButton(self)
        self.shawZfit2.setText("Manual Fit")
        self.shawZfit2.resize(round(0.07*width), round(0.05*height))
        self.shawZfit2.move(round(0.67*width), round(0.25*height))
        self.shawZfit2.clicked.connect(self.Shaw_Z_Fit2)
        self.shawZfit2.setStyleSheet(button_style)
        self.shawZfit2.setEnabled(False)

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
        self.labelResultsZt.move(round(0.37*width), round(0.65*height))
        self.labelResultsZt.resize(round(0.3*width), round(0.07*height))
        self.labelResultsZt.setText('\t  Analysis results\nautomatic:\t\t  manual:')
        self.labelResultsZt.setFont(textstyle2)
        self.labelResultsZt.setStyleSheet('background-color: None')
        #
        self.labelResultsZt = QLabel(self)
        self.labelResultsZt.move(round(0.2*width), round(0.65*height))
        self.labelResultsZt.resize(round(0.16*width), round(0.25*height))
        self.labelResultsZt.setText('\n\n\nWindow\'s range:\n\nPeak position:\n\nPeak-plateau ratio:\n\nClinical range (R{:d}):\n\nPeak width (@{:d}%):'.format(int(CLINICAL_RANGE_PERC*100), int(CLINICAL_RANGE_PERC*100)))
        self.labelResultsZt.setFont(textstyle)
        self.labelResultsZt.setStyleSheet('background-color: None')
        #
        self.labelResultsZ = QLabel(self)
        self.labelResultsZ.move(round(0.35*width), round(0.65*height))
        self.labelResultsZ.resize(round(0.12*width), round(0.25*height))
        self.labelResultsZ.setText('\n\n\n--\n\n--\n\n--\n\n--\n\n--')
        self.labelResultsZ.setFont(textstyle)
        self.labelResultsZ.setStyleSheet('background-color: None')
        #
        self.labelResultsZm = QLabel(self)
        self.labelResultsZm.move(round(0.51*width), round(0.65*height))
        self.labelResultsZm.resize(round(0.12*width), round(0.25*height))
        self.labelResultsZm.setText('\n\n\n--\n\n--\n\n--\n\n--\n\n--')
        self.labelResultsZm.setFont(textstyle)
        self.labelResultsZm.setStyleSheet('background-color: None')
        

        #########################################################################
        # RIGHT SIDE

        # Z File load button
        self.loadZdata = QPushButton(self)
        self.loadZdata.setText("Load Z Data")
        self.loadZdata.resize(round(0.2*width), round(0.05*height))
        self.loadZdata.move(round(0.79*width), round(0.15*height))
        self.loadZdata.clicked.connect(self.Load_Z_Data)
        self.loadZdata.setStyleSheet(button_style)

        # Z File label
        self.labelZfile = QLabel(self) 
        self.labelZfile.setText("File IN Z:")
        self.labelZfile.resize(round(0.045*width), round(0.03*height))
        self.labelZfile.move(round(0.8*width), round(0.2*height))
        self.labelZfile.setStyleSheet('border: 1px solid gray; border: None')
        #
        self.labelZfile = QLabel(self) 
        self.labelZfile.setText('')
        self.labelZfile.resize(round(0.135*width), round(0.03*height))
        self.labelZfile.move(round(0.845*width), round(0.2*height))
        self.labelZfile.setStyleSheet('background-color: lightgray; border: None')

        # Z File reverse button
        self.reverseZdata = QPushButton(self)
        self.reverseZdata.setText("Reverse Z Data")
        self.reverseZdata.resize(round(0.2*width), round(0.05*height))
        self.reverseZdata.move(round(0.79*width), round(0.25*height))
        self.reverseZdata.clicked.connect(self.Reverse_Z_Data)
        self.reverseZdata.setStyleSheet(button_style)
        self.reverseZdata.setEnabled(False)

        # Enable Z switch button
        self.enableZ = QPushButton(self)
        self.enableZ.setText("Enable Z")
        self.enableZ.resize(round(0.1*width), round(0.05*height))
        self.enableZ.move(round(0.79*width), round(0.3*height))
        self.enableZ.clicked.connect(self.Enable_Z)
        self.enableZ.setStyleSheet(enable_style)
        self.enableZ.setEnabled(False)

        # Z Calibration load button
        self.loadZcalib = QPushButton(self)
        self.loadZcalib.setText("Load Z Calib")
        self.loadZcalib.resize(round(0.2*width), round(0.05*height))
        self.loadZcalib.move(round(0.79*width), round(0.37*height))
        self.loadZcalib.clicked.connect(self.Load_Z_Calibration)
        self.loadZcalib.setStyleSheet(button_style)
        self.loadZcalib.setEnabled(False)

        # Z Calib label 
        self.labelZcalib = QLabel(self) 
        self.labelZcalib.setText("Calib Z:")  
        self.labelZcalib.resize(round(0.045*width), round(0.03*height))
        self.labelZcalib.move(round(0.8*width), round(0.42*height))
        self.labelZcalib.setStyleSheet('border: 1px solid gray; border: None')
        #
        self.labelZcalib = QLabel(self) 
        self.labelZcalib.setText('')
        self.labelZcalib.resize(round(0.135*width), round(0.03*height))
        self.labelZcalib.move(round(0.845*width), round(0.42*height))
        self.labelZcalib.setStyleSheet('background-color: lightgray; None')

        # Enable Z Calib switch button
        self.enableZcalib = QPushButton(self)
        self.enableZcalib.setText("Apply calib Z")
        self.enableZcalib.resize(round(0.1*width), round(0.05*height))
        self.enableZcalib.move(round(0.79*width), round(0.45*height))
        self.enableZcalib.clicked.connect(self.Apply_Z_Calib)
        self.enableZcalib.setStyleSheet(enable_style)
        self.enableZcalib.setEnabled(False)

        # Manual choose button
        self.manualbutton = QPushButton(self)
        self.manualbutton.setText("Select window manually")
        self.manualbutton.resize(round(0.2*width), round(0.05*height))
        self.manualbutton.move(round(0.79*width), round(0.55*height))
        self.manualbutton.clicked.connect(self.ManualWindow)
        self.manualbutton.setStyleSheet(enable_style)
        self.manualbutton.setEnabled(False)

        # Windows edges label
        self.leftlabel = QLabel(self) 
        self.leftlabel.setText('left edge:\t0 ch\t0 mm w.e.\nright edge:\t0 ch\t0 mm w.e.')
        self.leftlabel.resize(round(0.2*width), round(0.05*height))
        self.leftlabel.move(round(0.8*width), round(0.61*height))
        self.leftlabel.setStyleSheet('border: None')

        # Manual window button
        self.manual_window = QPushButton(self)
        self.manual_window.setText("Set window's edges")
        self.manual_window.resize(round(0.2*width), round(0.03*height))
        self.manual_window.move(round(0.79*width), round(0.68*height))
        self.manual_window.clicked.connect(self.Set_Windows_edge)
        self.manual_window.setEnabled(False)

        # Reset All button
        self.resetall = QPushButton(self)
        self.resetall.setText("Reset all")
        self.resetall.resize(round(0.2*width), round(0.05*height))
        self.resetall.move(round(0.79*width), round(0.8*height))
        self.resetall.clicked.connect(self.Reset_all)
        self.resetall.setStyleSheet('background-color: lightgray; color: red')

        # Analyze button
        self.analyze = QPushButton(self)
        self.analyze.setText("ANALYZE")
        self.analyze.setFont(textstyle)
        self.analyze.resize(round(0.2*width), round(0.1*height))
        self.analyze.move(round(0.79*width), round(0.85*height))
        self.analyze.clicked.connect(self.Analyze)
        self.analyze.setStyleSheet('background-color: lightgreen')
        self.analyze.setEnabled(False)

        #########################################################################

        
    
    ########################################################################################################################################
    def Load_Z_Data(self):

        self.Reset_all()
        
        try:
            '''
            data =np.loadtxt('./data/mlfc/20220111_084114_profileZ.dat', dtype=str, delimiter = '\t')
            '''
            file = QFileDialog.getOpenFileName(self, os.getcwd())[0]
            data = np.loadtxt(file, dtype=str, delimiter='\t')
            self.labelZfile.setText(file.split('/')[-1])
            
            self.Z_Time = data[-1][0].astype(float)
            self.Z_Data = data[-1][1::].astype(float)*-1

            self.Z_data_x = range(len(self.Z_Data))
            self.Z_data_y = self.Z_Data
            self.ZPlot.clear()
            self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
            self.ZPlot.setLabel('bottom','channels')
            self.ZPlot.getPlotItem().enableAutoRange()

            self.shawZraw.setEnabled(True)
            self.reverseZdata.setEnabled(True)
            self.enableZ.setEnabled(True)
            self.loadZcalib.setEnabled(True)
            self.analyze.setEnabled(True)
            self.resetZplot.setEnabled(True)
            self.manualbutton.setEnabled(True)
        
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('Unrecognized data format - Check the upload')
            msg.exec_()


    def Reverse_Z_Data(self):
        self.Z_data_y = np.flip(self.Z_data_y)
        if self.isflipped:
            self.isflipped = False
        else:
            self.isflipped = True

        self.ZPlot.removeItem(self.Zraw)
        self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)

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

        try:
            file = QFileDialog.getOpenFileName(self, os.getcwd())[0]
            data = np.loadtxt(file, dtype=str, delimiter = '\t')
            self.labelZcalib.setText(file.split('/')[-1])

            self.calibZ_vector_orig = np.transpose(data)[1][1::].astype(float)
            self.calibZ_vector_flip = np.flip(self.calibZ_vector_orig)

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
            if self.isflipped:
                self.calibZ_vector = self.calibZ_vector_flip
            else:
                self.calibZ_vector = self.calibZ_vector_orig

            if self.calibZ_enable:
                self.Z_data_y = self.Z_data_y / self.calibZ_vector
                self.ZPlot.removeItem(self.Zraw)
                self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
                self.calibZ_enable = False
                self.enableZcalib.setStyleSheet('background-color: None; color: None')
            else:
                self.Z_data_y = self.Z_data_y * self.calibZ_vector
                self.ZPlot.removeItem(self.Zraw)
                self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
                self.calibZ_enable = True
                self.enableZcalib.setStyleSheet('background-color: None; color: green')

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
        self.Z_data_y = self.Z_Data

        self.Zraw = self.ZPlot.plot(self.Z_data_x, self.Z_data_y, pen = self.pen_data)
        self.ZPlot.setLabel('bottom','channels')
        self.ZPlot.getPlotItem().enableAutoRange()
        self.leftline = pg.InfiniteLine(pos=self.Z_data_x[0], pen=self.pen_roi, angle=90, movable=True)
        self.rightline = pg.InfiniteLine(pos=self.Z_data_x[-1], pen=self.pen_roi, angle=90, movable=True)
        
        self.ZPlot.addItem(self.leftline)
        self.ZPlot.addItem(self.rightline)

        self.manual_window.setEnabled(True)
        self.manual_window.setStyleSheet('background-color: None; color: None')
        self.leftlabel.setText('left edge:\t0 ch\t0 mm w.e.\nright edge:\t0 ch\t0 mm w.e.')
        self.shawZfit.setEnabled(False)
        self.shawZfit2.setEnabled(False)
        self.analysis_window = False
        
        return


    def Set_Windows_edge(self):
        
        if self.analysis_window == False:
            
            line1 = int(self.leftline.value())
            line2 = int(self.rightline.value())
            left = min(line1,line2)
            right = max(line1,line2)
            self.leftlabel.setText('left edge:\t{} ch\t{:.2f} mm w.e.\nright edge:\t{} ch\t{:.2f} mm w.e.'.format(left,left*TO_WE,right,right*TO_WE))
        
            self.analysis_window = [left, right]
            
            self.manual_window.setStyleSheet('background-color: None; color: green')
        
        else:
            self.analysis_window = False
            self.leftlabel.setText('left edge:\t0 ch\t0 mm w.e.\nright edge:\t0 ch\t0 mm w.e.')
            self.manual_window.setStyleSheet('background-color: None; color: None')

        return
    

    def Shaw_Z_Data(self):
        if self.Zraw.isVisible():
            self.Zraw.hide()
        else:
            self.Zraw.show()
        return
    
    
    def Shaw_Z_Fit(self):
        if self.Zfit.isVisible():
            self.Zfit.hide()
        else:
            self.Zfit.show()
        return
    
    def Shaw_Z_Fit2(self):
        if self.Zfit2.isVisible():
            self.Zfit2.hide()
        else:
            self.Zfit2.show()
        return
    
    
    def Reset_all(self):

        # Plot
        self.ZPlot.clear()
        self.ZPlot.setLabel('bottom','channels')

        # Data
        self.Z_Data = []

        # Variables
        self.mlfc_enable     = False
        self.calibZ_enable   = False
        self.isflipped       = False
        self.analysis_window = False

        # Label
        self.labelZfile.setText('')
        self.labelZcalib.setText('')
        self.labelResultsZ.setText('\n\n\n--\n\n--\n\n--\n\n--\n\n--')
        self.labelResultsZm.setText('\n\n\n--\n\n--\n\n--\n\n--\n\n--')
        self.labelResults.setText('')
        self.enableZ.setStyleSheet('background-color: None; color: None')
        self.enableZcalib.setStyleSheet('background-color: None; color: None')
        self.manual_window.setStyleSheet('background-color: None; color: None')
        self.leftlabel.setText('left edge:\t0 ch\t0 mm w.e.\nright edge:\t0 ch\t0 mm w.e.')

        # button
        self.shawZraw.setEnabled(False)
        self.shawZfit.setEnabled(False)
        self.shawZfit2.setEnabled(False)
        self.reverseZdata.setEnabled(False)
        self.enableZ.setEnabled(False)
        self.loadZcalib.setEnabled(False)
        self.enableZcalib.setEnabled(False)
        self.analyze.setEnabled(False)
        self.resetZplot.setEnabled(False)
        self.manualbutton.setEnabled(False)
        self.manual_window.setEnabled(False)
        
        return
    
    def Analyze(self):

        # MLFC Analysis
        if self.mlfc_enable:

            try:
                self.Zres_auto = functions.mlfc_analysis(self.Z_data_y, False)
                
                self.ZPlot.clear()
                self.ZPlot.setLabel('bottom','depth [cm w.e.]')

                self.Zraw = self.ZPlot.plot(self.Zres_auto['coordinates_raw'], self.Zres_auto['raw_data'], pen = self.pen_data)
                self.Zfit = self.ZPlot.plot(self.Zres_auto['coordinates_fit'], self.Zres_auto['fit_data'], pen = self.pen_fit)
                self.shawZfit.setEnabled(True)
                self.labelResultsZ.setText('\n\n\n{} / [{:.2f},{:.2f}]\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}'.format(self.Zres_auto['windows_range'],self.Zres_auto['windows_range'][0]*TO_WE,self.Zres_auto['windows_range'][1]*TO_WE,
                                                                                            self.Zres_auto['peak_pos']['value'],self.Zres_auto['peak_pos']['unit'],
                                                                                            self.Zres_auto['pp_ratio']['value'],self.Zres_auto['pp_ratio']['unit'],
                                                                                            self.Zres_auto['cl_range']['value'],self.Zres_auto['cl_range']['unit'],
                                                                                            self.Zres_auto['peak_width']['value'],self.Zres_auto['peak_width']['unit']))
            

                if self.analysis_window != False:
                    self.Zres_man = functions.mlfc_analysis(self.Z_data_y, self.analysis_window)
                    self.Zfit2 = self.ZPlot.plot(self.Zres_man['coordinates_fit'], self.Zres_man['fit_data'], pen = self.pen_fit2)
                    self.shawZfit2.setEnabled(True)
                    self.labelResultsZm.setText('\n\n\n{} / [{:.2f},{:.2f}]\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}\n\n{:.2f}\t{}'.format(self.Zres_man['windows_range'],self.Zres_man['windows_range'][0]*TO_WE,self.Zres_man['windows_range'][1]*TO_WE,
                                                                                                self.Zres_man['peak_pos']['value'],self.Zres_man['peak_pos']['unit'],
                                                                                                self.Zres_man['pp_ratio']['value'],self.Zres_man['pp_ratio']['unit'],
                                                                                                self.Zres_man['cl_range']['value'],self.Zres_man['cl_range']['unit'],
                                                                                                self.Zres_man['peak_width']['value'],self.Zres_man['peak_width']['unit']))
            
                self.ZPlot.getPlotItem().enableAutoRange()
            
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Warning")
                msg.setInformativeText('Analysis ended with error - see terminal output for further details')
                msg.exec_()
                

            if self.analysis_window == False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Results")
                msg.setInformativeText('Suggested results shawn.\nIf you want to change the analysis, select the window')
                msg.exec_()
                

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Warning")
            msg.setInformativeText('Nothing to analyze:\nload files and press enable button')
            msg.exec_()
        
        self.manual_window.setEnabled(False)

        return