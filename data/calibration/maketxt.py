f = open('QEYE_calib.txt','w')

f.write('CH number\tCalib factor\n')

for i in range(512):
    f.write('{}\t{}\n'.format(i,1.0))

f.close()

