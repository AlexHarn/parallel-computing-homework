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

for version in ['v2_square', 'v3']:
    fig, axs = plt.subplots(3, sharex='col', gridspec_kw={'hspace': .2,
                                                          'wspace': 0})

    for i, n in enumerate(ns):
        data = {
                'Total': [],
                'Generate': [],
                'Binning': [],
                'Pivoting': [],
                'Distribute': [],
                'Local Sort': [],
                'Gathering': [],
               }
        for p in ps:
            fname = '{}_{}_{}.out'.format(version, p, n)
            with open(DATA_PATH + fname, 'r') as fstream:
                out = fstream.readlines()
            data['Total'].append(float(out[2].split(' ')[-1]))
            if version == 'v2_square':
                data['Generate'].append(float(out[5].split(' ')[-1]))
                data['Binning'].append(float(out[9].split(' ')[-1]))
                data['Distribute'].append(float(out[13].split(' ')[-1]))
                data['Local Sort'].append(float(out[17].split(' ')[-1]))
                data['Gathering'].append(float(out[21].split(' ')[-1]))
            else:
                data['Generate'].append(float(out[5].split(' ')[-1]))
                data['Binning'].append(float(out[9].split(' ')[-1]))
                data['Pivoting'].append(float(out[13].split(' ')[-1]))
                data['Distribute'].append(float(out[17].split(' ')[-1]))
                data['Local Sort'].append(float(out[21].split(' ')[-1]))
                data['Gathering'].append(float(out[25].split(' ')[-1]))

        for key in data:
            if key == 'Pivoting':
                continue
            data[key] = np.asarray(data[key])

            axs[i].plot(ps, data[key], label=key,
                        linestyle='--', marker='o')
        if version == 'v3':
            data['Pivoting'] = np.asarray(data['Pivoting'])

            axs[i].plot(ps, data['Pivoting'], label='Pivoting',
                        linestyle='--', marker='o')

        axs[i].set_title("N = {}".format(n))
        axs[i].set_ylabel("Time / s")

    handles, labels = fig.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys(), loc='upper center',
               ncol=3, borderaxespad=2, bbox_to_anchor=(.5, 1.03),
               frameon=False)
    axs[-1].set_xlabel(r"Number of cores $p$")
    axs[-1].set_xticks(ps)
    plt.savefig('{}_times.pdf'.format(version))
    plt.clf()
print("Done.")
