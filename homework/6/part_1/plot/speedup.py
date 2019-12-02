import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict
from pylab import rcParams

rcParams['figure.figsize'] = 10, 10
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 15

DATA_PATH = '../results/'

ps = np.arange(14, 154, 14)
ns = np.array([100000000, 500000000, 2000000000])

for version in ['v1', 'v2']:
    fig, axs = plt.subplots(3, sharex='col', sharey='col',
                            gridspec_kw={'hspace': .2, 'wspace': 0})

    for i, n in enumerate(ns):
        total = []
        for p in ps:
            fname = '{}_{}_{}.out'.format(version, p, n)
            with open(DATA_PATH + fname, 'r') as fstream:
                out = fstream.readlines()
            total.append(float(out[2].split(' ')[-1]))
        total = np.asarray(total)
        speedup = total[0]/total
        efficiency = speedup/ps*14

        axs[i].axhline(1., color='k')
        axs[i].plot(ps, speedup, label='Speedup',
                    linestyle='--', marker='o')
        axs[i].plot(ps, efficiency, label='Efficiency',
                    linestyle='--', marker='o')
        axs[i].set_title("N = {}".format(n))

    handles, labels = fig.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys(), loc='upper center',
               ncol=3, borderaxespad=2,
               frameon=True)
    axs[-1].set_xlabel(r"Number of cores $p$")
    # axs[-1].set_xlim(0.8, 28.2)
    axs[-1].set_xticks(ps)
    plt.savefig('{}_speedup.pdf'.format(version))
    plt.clf()
print("Done.")
