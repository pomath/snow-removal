import matplotlib.pyplot as plt
from array import array
x = array('f')
y = array('f')
with open('averages.snr') as f:
    for line in f:
        tmp = line.split()
        x.append(float(tmp[1]))
        y.append(float(tmp[2]))

plt.plot(x,y)
ax = plt.gca()
plt.xlim(0, 365)
plt.savefig('averages.png')
