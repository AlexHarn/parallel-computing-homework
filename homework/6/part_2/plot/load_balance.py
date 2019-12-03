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

for version in ['v2_square', 'v3', 'v2']:
    if version == 'v2':
        DATA_PATH = '../../part_1/results/'
    fig, axs = plt.subplots(3, sharex='col', gridspec_kw={'hspace': .2,
                                                          'wspace': 0})

    for i, n in enumerate(ns):
        t_min = []
        t_avg = []
        t_max = []

        for p in ps:
            fname = '{}_{}_{}.out'.format(version, p, n)
            with open(DATA_PATH + fname, 'r') as fstream:
                out = fstream.readlines()
            if version == 'v2_square' or version == 'v2':
                t_min.append(float(out[4].split(' ')[-1]))
                t_avg.append(float(out[5].split(' ')[-1]))
                t_max.append(float(out[6].split(' ')[-1]))

                for j in [9, 13, 17, 21]:
                    t_min[-1] += float(out[j-1].split(' ')[-1])
                    t_avg[-1] += float(out[j].split(' ')[-1])
                    t_max[-1] += float(out[j+1].split(' ')[-1])
            else:
                t_min.append(float(out[4].split(' ')[-1]))
                t_avg.append(float(out[5].split(' ')[-1]))
                t_max.append(float(out[6].split(' ')[-1]))

                for j in [9, 13, 17, 21, 25]:
                    t_min[-1] += float(out[j-1].split(' ')[-1])
                    t_avg[-1] += float(out[j].split(' ')[-1])
                    t_max[-1] += float(out[j+1].split(' ')[-1])

        t_min = np.asarray(t_min)
        t_avg = np.asarray(t_avg)
        t_max = np.asarray(t_max)

        axs[i].plot(ps, t_min, label='Min',
                    linestyle='--', marker='o')
        axs[i].plot(ps, t_avg, label='Avg',
                    linestyle='--', marker='o')
        axs[i].plot(ps, t_max, label='Max',
                    linestyle='--', marker='o')

        axs[i].set_title("N = {}".format(n))
        axs[i].set_ylabel("Time / s")

    handles, labels = fig.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys(), loc='upper center',
               ncol=3, borderaxespad=2, bbox_to_anchor=(.5, 1.03),
               frameon=True)
    axs[-1].set_xlabel(r"Number of cores $p$")
    axs[-1].set_xticks(ps)
    plt.savefig('{}_load_balance.pdf'.format(version))
    plt.clf()
print("Done.")
