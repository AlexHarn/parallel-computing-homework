import numpy as np
from uncertainties import ufloat
import matplotlib.pyplot as plt
from pylab import rcParams

rcParams['figure.figsize'] = 10, 5
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 15

DATA_PATH = '../results/'

for version in ['sequential', 'block', 'cyclic']:
    print("Working on", version)

    times = []
    fname = '{}_benchmark.out'.format(version)
    with open(DATA_PATH + fname, 'r') as fstream:
        lines = fstream.readlines()
    for line in lines:
        if line.startswith('Time elapsed'):
            times.append(float(line[14:23]))
    times = np.asarray(times)/10000000
    if version == 'sequential':
        tau_s = ufloat(np.mean(times), np.std(times, ddof=1))
        tau = tau_s
    elif version == 'block':
        tau_b = ufloat(np.mean(times), np.std(times, ddof=1))
        tau = tau_b
    elif version == 'cyclic':
        tau_c = ufloat(np.mean(times), np.std(times, ddof=1))
        tau = tau_c
    print('Tau for {} is: {}'.format(version, tau))

print('Worst case for sequential:',
      tau_s*pow(2, 32), 's =', tau_s*pow(2, 32)/3600)

km = pow(2, 32)

k1 = 13 * km//14
k2 = km - 23
k3 = km//14 - 1


def T(k, p, tau):
    return (np.mod(k, km//p) + 1)*tau.n


print("k1 = {}, k2 = {}, k3 = {}".format(k1, k2, k3))
print("T1 = {}, T2 = {}, T3 = {}".format(T(k1, 14, tau_b),
                                         T(k2, 14, tau_b),
                                         T(k3, 14, tau_b)))
all_ps = np.arange(1, 29)
ps = np.array([8, 12, 14, 16, 22, 28])
plt.plot(all_ps, T(k1, all_ps, tau_b), 'r--', label=r'$k_1$ Prediction')
plt.plot(all_ps, T(k2, all_ps, tau_b), 'g--', label=r'$k_2$ Prediction')
plt.plot(all_ps, T(k3, all_ps, tau_b), 'b--', label=r'$k_3$ Prediction')

for k in [k1, k2, k3]:
    m_p = []
    m_t = []
    for p in ps:
        fname = '{}_{}.out'.format(k, p)
        with open(DATA_PATH + fname, 'r') as fstream:
            lines = fstream.readlines()
        if len(lines) == 16:
            m_p.append(p)
            m_t.append(float(lines[-1][14:23]))

    m_p = np.asarray(m_p)
    m_t = np.asarray(m_t)

    if k == k1:
        label = r'$k_1$ Measured'
        color = 'r'
    elif k == k2:
        label = r'$k_2$ Measured'
        color = 'g'
    elif k == k3:
        label = r'$k_3$ Measured'
        color = 'b'

    plt.plot(m_p, m_t, 'x', color=color, label=label)

plt.ylabel(r'$T$ / s')
plt.xlabel(r'$p$')
plt.legend()
plt.xticks([0, 5, 20, 25] + ps.tolist())
plt.savefig('block.pdf')
plt.clf()

for k in [k1, k2, k3]:
    m_p = []
    m_t = []
    for p in ps:
        fname = 'cyclic_{}_{}.out'.format(k, p)
        with open(DATA_PATH + fname, 'r') as fstream:
            lines = fstream.readlines()
        if len(lines) == 16:
            m_p.append(p)
            m_t.append(float(lines[-1][14:23]))

    m_p = np.asarray(m_p)
    m_t = np.asarray(m_t)

    if k == k1:
        label = r'$k_1$ Measured'
        color = 'r'
    elif k == k2:
        label = r'$k_2$ Measured'
        color = 'g'
    elif k == k3:
        label = r'$k_3$ Measured'
        color = 'b'

    plt.plot(m_p, m_t, 'x', color=color, label=label)

plt.ylabel(r'$T$ / s')
plt.xlabel(r'$p$')
plt.xticks(ps)
plt.legend()
plt.savefig('cyclic.pdf')
