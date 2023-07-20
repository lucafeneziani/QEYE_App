#-----------------------------------------constants.py-----------------------------------
# useful constants for the analysis procedures
#----------------------------------------------------------------------------------------

# CLINICLAL RANGES
CLINICAL_RANGE_PERC = 0.9
PEAK_WIDTH_PERC = 0.5

#CONSTANT FOR DEPTH-DOSE PROFILE FITTING
BRAGG_GAMMA_FUNC = 1.565 # no unit - gamma function value (Bortfeld model)
#BRAGG_ALPHA = 0.0022 #cm*MeV^{-p} in water
#BRAGG_P = 1.77 #no unit, in water
BRAGG_ALPHA_AL = 0.00146137480 #cm*MeV^{-p} - alpha parameter in the analytical relationship Energy - Range for aluminum
BRAGG_P_AL = 1.70525347 #no unit - p parameter in the analytical relationship Energy - Range for aluminum
BRAGG_ALPHA_CU = 0.00185679 #cm*MeV^{-p} - alpha parameter in the analytical relationship Energy - Range for copper
BRAGG_P_CU = 1.68973459 #no unit - p parameter in the analytical relationship Energy - Range for copper
BRAGG_ALPHA = (BRAGG_ALPHA_AL+BRAGG_ALPHA_CU)/2
BRAGG_P = (BRAGG_P_AL+BRAGG_P_CU)/2
#BRAGG_ALPHA = 0.001288253135486655 #cm*MeV^{-p} - alpha parameter in the analytical relationship Energy - Range
#BRAGG_P = 1.7293451613367292 #no unit - p parameter in the analytical relationship Energy - Range
BRAGG_BETA = 0.012 #cm^{-1} - beta parameter value (Bortfeld model)
BRAGG_GAMMA = 0.6 #no unit - gamma parameter value (Bortfeld model)
BRAGG_SIGMA_MONO_FACT = 0.012 # - (Bortfeld model)
BRAGG_SIGMA_MONO_EXP = 0.935 #no unit - (Bortfeld model)
BRAGG_SIGMA_E0_FACTOR = 0.01 #no unit - (Bortfeld model)
BRAGG_EPSILON_MIN = 0.0
BRAGG_EPSILON_MAX = 0.2

#QUBE CONSTANTS:
TO_WE = 0.120 # mm we per channel - each ionization chamber module corresponds to xx cm WEPL

#QEYE CONSTANTS:
TO_EYETISSUE = 0.2 # invented value - waiting for real one
TO_PERSPEX = 0.3   # invented value - waiting for real one

# GENERAL
CHANNELS = 512
STEP = 0.00485 #cm (Cu+Kp+Cu+Py/2)
DEPTHMIN = STEP
DEPTHMAX = DEPTHMIN*(CHANNELS+1) #cm
PHI0     = 1.0 #cm-2
EPSILON  = 0.1
BETA     = 0.012
GAMMA    = 0.6

## MATERIALS
# COPPER
Cu_density  = 8.96   #g/cm3
Cu_thick    = 0.0011 #cm
Cu_alpha = 0.000426674555889869
Cu_p_val = 1.7457546509328448
Cu_electronic_density = 2.4624572052043544e+24
# KAPTON
Kp_density  = 1.42   #g/cm3
Kp_thick    = 0.0025 #cm
Kp_alpha = 0.001538487731203791
Kp_p_val = 1.7933728333618606
Kp_electronic_density = 4.383977340715678e+23
# PYRALUX
Py_density  = 1.42   #g/cm3
Py_thick    = 0.0050 #cm
Py_alpha = 0.001538487731203791
Py_p_val = 1.7933728333618606
Py_electronic_density = 4.383977340715678e+23
# MLFC
MLFC_alpha = 0.0009736213425109618
MLFC_p_val = 1.7661051372581726
MLFC_density  = 3.1301030927835054    #g/cm3
MLFC_thick    = 0.0097 #cm
MLFC_electronic_density = 8.974627687614782e+23 #cm-3
MLFC_alpha_prime = 0.23385287457512216 #MeV/cm