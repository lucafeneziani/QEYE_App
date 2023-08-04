import numpy as np
from scipy.signal import savgol_filter, find_peaks
from scipy.optimize import curve_fit
from constants import *
import scipy.special as spspec
import math

DIRECTORY = '/Users/lucafeneziani/Desktop/QEYE/QEYE_App/'

def mlfc_analysis(data_array, manual_window_def=False, equivalence = TO_WE):

    filter_dim = 7            # optimal = 7
    negative_signal = 'no'    # negative signal removal: yes or no
    threshold_percent = 0.05  #
    window_add = 0            # both side of the peak

    
    # BORFELD CURVES
    file_bortfeld  = DIRECTORY + 'bortfeld_curves_mlfc.py' #Bortfeld theoretical curves
    with open(file_bortfeld) as bor_file: #create bortfeld curve matrix (one per ch)
        lines = bor_file.readlines()


    channels = len(data_array)  # number of acquisition channels
    x_coord = np.arange(channels)
    x_coord_we = ((x_coord+1)*equivalence).tolist() # coordinates of channels converted to water equivalent thickness
    # signal inversion (from negative to positive signal)
    # data_array = [elem*(-1) for elem in data_array]
    # smoothing
    signal = Smooth(data_array,filter_dim)
    #remove negative part of signal -> electronic noise
    if negative_signal=='yes':                           
        for elem in range(channels):
            if signal[elem]<0: signal[elem]=0
    # finding maximum
    peak_val = max(signal)
    peak_pos = np.argmax(signal)
    
    # BIAS REMOVAL
    lim_sx = peak_pos-50
    if lim_sx < 0: 
        lim_sx = 0
    lim_dx = peak_pos+50
    if lim_dx > channels-1:
        lim_dx = channels-1
    bias_ch = np.concatenate((x_coord[0:lim_sx],x_coord[lim_dx:channels+1]))
    bias_signal = np.concatenate((signal[0:lim_sx],signal[lim_dx:channels+1]))
    popt_lin = curve_fit(Lin,bias_ch,bias_signal)[0]
    bias = []
    for i in range(channels):
        bias.append(Lin(i,popt_lin[0],popt_lin[1]))
    for i in range(channels):
        signal[i] -= bias[i]
        #if signal[i] < 0:
        #    signal[i] = 0
    # new maximum
    peak_val = max(signal)
    peak_pos = np.argmax(signal)
    
    #print('Peak channel: ',peak_pos)
    #print('Peak value: ',peak_val)

    if manual_window_def == False:
        # ANALYSIS WINDOW DEFINITION (ROI for convolution):
        threshold = peak_val*threshold_percent
        stop_a = peak_pos#limits initialized to the peak
        stop_b = peak_pos
        while signal[stop_a]>threshold:#limit set to the window left border
            stop_a -= 1
            if stop_a == 0:#no values below THR
                #print('lower bound not found: too low threshold')
                break
        stop_a -= window_add #adding chs on the left if needed
        if stop_a<0:#max limit at 0
            stop_a = 0
        while signal[stop_b]>threshold:#limit set to the window right border
            stop_b += 1
            if stop_b == channels-1:#no values below THR
                #print('upper bound not found: too low threshold')
                break
        stop_b += window_add #adding chs on the right if needed
        if stop_b>channels-1:#max limit at last channel
            stop_b = channels-1
        

    else:
        # MANUAL WINDOWS DEFINITION
        if 0 < manual_window_def[0] < channels:
            stop_a = manual_window_def[0]
        else:
            stop_a = 0

        if 0 < manual_window_def[1] < channels:
            stop_b = manual_window_def[1]
        else:
            stop_b = channels - 1
        

    #print('window = ({},{})'.format(stop_a,stop_b))
    
    # RECONSTRUCTION WITH BORTFELD CURVES:
    memory = np.zeros(channels)
    bort_fin = np.zeros(channels)

    for R in range(stop_a,stop_b,1):
        line = lines[R]
        vect = line.split("\t")
        vect.remove('\n')
        for i in range(channels):
            bort_val = float(vect[i])*signal[R]
            bort_fin[i]=memory[i]+bort_val
        memory = bort_fin

    # CALCULATE PARAMETERS ----------------------------------------------------------------------------------------------------------------------------------------
    bort_peak_pos = np.argmax(bort_fin)
    pos_sides = calc_sides(bort_fin, x_coord, PEAK_WIDTH_PERC)
    peak_sides = calc_sides(bort_fin, x_coord_we, PEAK_WIDTH_PERC)
    peak_width = (peak_sides[1]-peak_sides[0])
    plt_mean = np.mean(bort_fin[:10])
    peak_mean = np.mean(bort_fin[math.ceil(pos_sides[0]):math.floor(pos_sides[1])])
    #print("Peak size indeces {} - {} ".format(math.ceil(pos_sides[0]), math.floor(pos_sides[1])))
    #print("Peak in the region {} - {} mm".format(peak_sides[0], peak_sides[1]))
    #print("Peak width at 90 % is {} mm".format(peak_width))
    #print("Peak position afer treatement is {} mm".format(bort_peak_pos)) 
    cl_range = find_cl_range(bort_fin, x_coord_we, bort_peak_pos, CLINICAL_RANGE_PERC)
    #print("CLinical range is {} mm".format(cl_range))
    peak_plt_ratio = peak_mean/plt_mean # peak to plateau ratio
    rawcoord_list = x_coord_we
    rawdata_list = data_array
    coord_list = x_coord_we
    bort_norm = [el * (peak_val/peak_mean) for el in bort_fin]
    

    # Normalization
    rawdata_max = np.mean(np.sort(rawdata_list)[-10::])
    rawdata_list = rawdata_list/rawdata_max*100
    bort_max = np.mean(np.sort(bort_norm)[-10::])
    bort_norm = bort_norm/bort_max*100
    
    entrance_dose = np.mean(bort_norm[0:10])

    # Modulation
    marker_pos, dose_at_marker = find_marker(coord_list, bort_norm, 0.7)
    modulation = cl_range - marker_pos
    
    results = {
        "windows_range":[stop_a,stop_b],
        "peak_pos":{"value":float(peak_pos*equivalence), "unit":"mm"},
        "pp_ratio":{"value":float(peak_plt_ratio),"unit":" "},
        "cl_range":{"value":float(cl_range),"unit":"mm"},
        "peak_width":{"value":float(peak_width),"unit":"mm"},
        "coordinates_raw":rawcoord_list,
        "raw_data":rawdata_list,
        "coordinates_fit": coord_list,
        "fit_data": bort_norm,
        "entrance_dose":{"value":float(entrance_dose), "unit":"%"},
        "modulation":{"value":float(modulation), "unit":"mm"},
        "marker":{"value":float(marker_pos), "unit":"mm"},
        "dose_at_marker":{"value":float(dose_at_marker), "unit":"%"},
    }

    return results

def find_marker(x, y, slope):
    '''
    markerpos = np.argmax(y)
    '''
    deriv = np.gradient(y)
    for markerpos in range(len(y)):
        if deriv[markerpos] < slope:
            continue
        else:
            break
    marker = x[markerpos]
    value = y[markerpos]
    #print(marker)
    return marker, value


def Smooth(y, box_pts):                               # convoluzione con un filtro costante di dimensione box_pts = media dei valori nel filtro
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same').tolist()
    return y_smooth

def Lin(x,a,b):                                       # Retta per il fit delle code
    return a*x+b

# research of a specific % level on both sides of the Bragg peak
# x => data, y => coordinates, value => % level
def calc_sides(x, y, value):
    max_val = np.amax(x)
    max_index = np.where(x == max_val)[0][0]
    half_max = value*max_val
    left_half = 0
    right_half = 0
    for cnt in range(1, max_index):
       val = x[cnt]
       if(val >= half_max):
           w1 = np.abs(value - val/max_val)
           w2 = np.abs(value - x[cnt - 1]/max_val)
           pos1 = y[cnt]
           pos2 = y[cnt - 1]
           left_half = ((pos1*w2) + (pos2*w1))/(w1+w2)
           break
    for cnt2 in range(max_index+1, len(x)-1):
        val2 = x[cnt2]
        if(val2 <= half_max):
            w3 = np.abs(value - val2/max_val)
            w4 = np.abs(value - x[cnt2 - 1]/max_val)
            pos3 = y[cnt2]
            pos4 = y[cnt2 - 1]
            right_half = ((pos3*w4) + (pos4*w3))/(w3+w4)
            break
    values = np.array([left_half, right_half])
    return values

#Calculation of the clinical range (90 % of the peak in the distal fall-off)
def find_cl_range(x, y, max_index, perc):
    count = 0
    max = x[max_index]
    max_perc = perc*max
    for val in x[max_index+1:] :
        if val <= max_perc :
            w1 = np.abs(perc - val/max)
            w2 = np.abs(perc - x[max_index + count]/max)
            pos1 = y[count + 1 + max_index]
            pos2 = y[count + max_index]
            cl_range = ((pos1*w2) + (pos2*w1))/(w1+w2)
            return cl_range
        else:
            count = count + 1