#  Calcolo della curva di Bortfeld per la dose
#  La funzione Bortfeld(E0) restituisce un vettore di dosi per ogni punto
#    del range specificato per l'energia iniziale E0

import numpy as np
import matplotlib.pyplot as plt
import scipy.special as spspec
from constants import *


alpha       = MLFC_alpha
p_val       = MLFC_p_val
density     = MLFC_density
alpha_prime = MLFC_alpha_prime


def DOSE(z,R0):

    #sigma
    E0 = pow(R0/alpha,1/p_val)
    num = pow(p_val,3)*pow(alpha,2/p_val)
    den = 3*p_val-2
    esp = 3-2/p_val
    sigma2_mono = alpha_prime*num*pow(R0,esp)/den
    sigma2_E0 = pow(0.01*E0,2)
    sigma = np.sqrt(sigma2_mono+sigma2_E0*pow(alpha*p_val,2)*pow(E0,2*p_val-2))

    #dose
    zeta = (R0-z)/sigma
    anum = np.exp(-0.25*pow(zeta,2))*pow(sigma,1/p_val)*spspec.gamma(1/p_val)
    aden = np.sqrt(2*np.pi)*density*p_val*pow(alpha,1/p_val)*(1+BETA*R0)
    b = (1/sigma)*spspec.pbdv(-1/p_val,-zeta)[0]
    c = ((BETA/p_val)+(GAMMA*BETA)+(EPSILON/R0))*spspec.pbdv(-1/p_val-1,-zeta)[0]
    return PHI0*(anum/aden)*(b+c)


def BORTFELD(R0):
    
    dose = []
    for i in np.arange(DEPTHMIN,DEPTHMAX,STEP):
        new_dose = DOSE(i,R0)
        if new_dose >= 0:
            dose.append(new_dose)
        else:
            dose.append(0)
    return dose


# CREATE FILE

bortfelds = []
title = str('bortfeld_curves_mlfc.py')

f = open(title,'w')
for i in range(1,CHANNELS+1,1):
    bortfeld = BORTFELD(i*STEP)
    bortfelds.append(bortfeld)
    for j in range(0,CHANNELS,1):
        f.write('{}\t'.format(bortfeld[j]))
    f.write('\n')

f.close()
np.save('bortfeld_curves_mlfc', np.array(bortfelds))

# PLOT FOR 5 ENERGIES
curva = []
depth = []

for i in np.arange(DEPTHMIN,DEPTHMAX,STEP):
    depth.append(i)

    
for i in range(30,80,10):
    R = alpha*pow(i,p_val)
    dose = BORTFELD(R)
    mass = max(dose)
    for j in range(0,512,1):
        dose[j] = dose[j]/mass *100
    curva.append(dose)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(depth, curva[0], c='black', marker='None', markersize=2, label= '30 MeV')
ax.plot(depth, curva[1], c='y', marker='None', markersize=2, label= '40 MeV')
ax.plot(depth, curva[2], c='b', marker='None', markersize=2, label= '50 MeV')
ax.plot(depth, curva[3], c='r', marker='None', markersize=2, label= '60 MeV')
ax.plot(depth, curva[4], c='g', marker='None', markersize=2, label= '70 MeV')
ax.get_xaxis().set_label_text('depth [cm]', fontsize=14)
ax.get_yaxis().set_label_text('relative dose [%]', fontsize=14)
ax.legend(loc = 1, fontsize = 10, frameon = False)
ax.set_title('BORTFELD')
plt.show()