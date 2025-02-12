import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict
from pylab import rcParams

rcParams['figure.figsize'] = 10, 10
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 15

DATA_PATH = '../results/'

n_threads = np.array([1, 2, 4, 8, 14, 28])
for matrix in ['it-2004', 'twitter7', 'sk-2005']:
    print("Working on matrix {}...".format(matrix))
    fig, axs = plt.subplots(3, sharex='col', sharey='col',
                            gridspec_kw={'hspace': .2, 'wspace': 0})
    for i, block_size in enumerate([2048, 8192, 32768]):
        conversion = []
        csc = []
        csb = []
        for threads in n_threads:
            fname = '{}_{}_{}.out'.format(matrix, threads, block_size)
            with open(DATA_PATH + fname, 'r') as fstream:
                out = fstream.readlines()
            conversion.append(float(out[-4][-5:]))
            csc.append(float(out[-2][-5:]))
            csb.append(float(out[-1][-5:]))
        conversion = np.asarray(conversion)
        csc = np.asarray(csc)
        csb = np.asarray(csb)

        axs[i].axhline(1., color='k')
        axs[i].plot(n_threads, conversion, label='Conversion',
                    linestyle='--', marker='o')
        axs[i].plot(n_threads, csc, label='CSC',
                    linestyle='--', marker='o')
        axs[i].plot(n_threads, csb, label='CSB',
                    linestyle='--', marker='o')
        axs[i].set_title("Blocksize {}".format(block_size))
        axs[i].set_ylabel("Speedup")

    handles, labels = fig.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys(), loc='upper center',
               ncol=3, borderaxespad=2,
               frameon=True)
    axs[-1].set_xlabel("Number of threads")
    axs[-1].set_xlim(0.8, 28.2)
    axs[-1].set_xticks([1, 2, 4, 8, 14, 28])
    plt.savefig('{}.pdf'.format(matrix))
    plt.clf()
print("Done.")
