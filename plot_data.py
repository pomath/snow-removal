import matplotlib.pyplot as plt
from array import array
x = array('f')
y = array('f')
with open('averages.snr') as f:
    f.readline()
    for line in f:
        tmp = line.split()
        x.append(float(tmp[1]))
        y.append(float(tmp[2]))

plt.plot(x,y)
ax = plt.gca()
plt.xlabel('DOY')
plt.ylabel('SNR')
plt.title(r'MIN0 2016 $40^{\circ} - 50^{\circ}$ Average L2 SNR')
plt.savefig('averages.png')
