import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import ticker
from collections import OrderedDict
from scipy.optimize import curve_fit
from pylab import rcParams

rcParams['figure.figsize'] = 10, 5
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 15

DATA_PATH = '../results/'
ps = np.array([1, 2, 5, 10, 20, 100, 250])

for n in [1000, 100000, 10000000]:
    print("Working on n = {}...".format(n))

    # part b)

    fig, axs = plt.subplots(2, sharex='col', sharey='col',
                            gridspec_kw={'hspace': .2, 'wspace': 0},
                            figsize=(10, 10))

    p2p = []
    collective = []
    for p in ps:
        fname = '{}_{}.out'.format(n, p+1)
        with open(DATA_PATH + fname, 'r') as fstream:
            out = fstream.readlines()
        p2p.append(float(out[-8][-9:-1]))
        collective.append(float(out[-1][-9:-1]))
    p2p = np.asarray(p2p)
    collective = np.asarray(collective)

    p2p_speedup = p2p[0]/p2p
    p2p_efficiency = p2p_speedup/ps

    collective_speedup = collective[0]/collective
    collective_efficiency = collective_speedup/ps

    axs[0].axhline(1., color='k')
    axs[0].plot(ps, p2p_speedup, label='Speedup', linestyle='--', marker='o')
    axs[0].plot(ps, p2p_efficiency, label='Efficiency', linestyle='--',
                marker='o')
    axs[0].set_title('Point-to-point')

    axs[1].axhline(1., color='k')
    axs[1].plot(ps, collective_speedup, label='Speedup', linestyle='--',
                marker='o')
    axs[1].plot(ps, collective_efficiency, label='Efficiency', linestyle='--',
                marker='o')
    axs[1].set_title('Collective')

    handles, labels = fig.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys(), loc='upper center',
               ncol=3, borderaxespad=2,
               frameon=True)
    axs[-1].set_xlabel("Number of MPI processes")
    axs[-1].set_xscale('log')
    axs[-1].set_xticks(ps)
    axs[-1].get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    plt.savefig('{}.pdf'.format(n))
    plt.clf()

    # part c)
    idx = [0, 1, 2, 3, 4]
    if n == 10000000:
        idx = [0, 1, 2, 3, 4, 5]
    elif n == 1000:
        idx = [0, 1, 2]

    def f(p, a, b):
        return a*n/p + b*np.log2(p)

    popt, pcov = curve_fit(f, ps[idx], collective[idx])
    p_lin = np.linspace(ps[0], (ps[idx])[-1])
    plt.plot(p_lin, f(p_lin, *popt), label='Fit')
    plt.plot(ps[idx], collective[idx], 'o', label='Data')
    plt.legend()
    plt.xlabel(r'$p$')
    plt.ylabel(r'$t\,/\,$s')
    plt.savefig('fit_{}.pdf'.format(n))
    plt.clf()

    perr = np.sqrt(np.diag(pcov))
    print("Fit results for n = {}".format(n))
    print(" a = {} +- {}".format(popt[0], perr[0]))
    print(" b = {} +- {}".format(popt[1], perr[1]))

print("Done.")
