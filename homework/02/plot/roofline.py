import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams

rcParams['figure.figsize'] = 10, 5
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 15


def performance(I):
    if I > 3.167:
        return 95
    else:
        return 30*I


plt.plot([0, 3.167], [0, 95], 'b-')
plt.plot([3.167, 10], [95, 95], 'b-', label='Performance')
plt.xlabel(r'Arithmetic Intensity$\,/\,\mathrm{FLOP}/\mathrm{byte}$')
plt.ylabel(r'Performance$\,/\,GFLOP/s$')
plt.vlines(3.167, 0, 95, colors='g',
           label=r'$I_{\mathrm{crit}} = 3.167\,\mathrm{FLOP}/\mathrm{byte}$')
plt.vlines(3/8, 0, performance(3/8), colors='r',
           label=r'$I = 3/8\,\mathrm{FLOP}/\mathrm{byte}$')
plt.ylim(0, 100)
plt.xlim(0, 10)
plt.legend()
plt.savefig('roofline.pdf')

print(performance(3/8), performance(3/4))
