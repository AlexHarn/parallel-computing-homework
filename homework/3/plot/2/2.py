import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pylab import rcParams
import os

rcParams['figure.figsize'] = 10, 5
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 15

# Get all stream runs
stream = []
for fn in os.listdir('./stream_runs/'):
    if fn.endswith('.out'):
        n = fn[:-4]
        with open('./stream_runs/' + fn, "r") as myfile:
            data = myfile.readlines()
        bandwidth = data[-7].split()[1]
        if bandwidth != 'inf':
            bandwidth = float(bandwidth)
            stream.append([n, bandwidth])

stream = np.asarray(stream, np.float)
stream.sort(axis=0)
stream = stream.T

# ----------------------------------- GCC -------------------------------------
o1 = np.loadtxt('./gcc_o1.dat', delimiter=',')
df = pd.DataFrame(o1, columns=['N', 'R', 'elapsed_time', 'MB/s'])
o1 = df.groupby('N').mean().reset_index()

o3 = np.loadtxt('./gcc_o3.dat', delimiter=',')
df = pd.DataFrame(o3, columns=['N', 'R', 'elapsed_time', 'MB/s'])
o3 = df.groupby('N').mean().reset_index()

o3_native = np.loadtxt('./gcc_o3_native.dat', delimiter=',')
df = pd.DataFrame(o3_native, columns=['N', 'R', 'elapsed_time', 'MB/s'])
o3_native = df.groupby('N').mean().reset_index()


plt.semilogx(o1['N'], o1['MB/s'], label='-O1')
plt.semilogx(o3['N'], o3['MB/s'], label='-O3')
plt.semilogx(o3_native['N'], o3_native['MB/s'], label='-O3 -march=native')
plt.semilogx(stream[0], stream[1], label='STREAM')
plt.ylabel('MB/s')
plt.xlabel(r'$N$')
plt.legend()
# plt.show()
plt.savefig('gcc.pdf')
plt.clf()

# ---------------------------------- Intel ------------------------------------
o1 = np.loadtxt('./intel_o1.dat', delimiter=',')
df = pd.DataFrame(o1, columns=['N', 'R', 'elapsed_time', 'MB/s'])
o1 = df.groupby('N').mean().reset_index()

o3 = np.loadtxt('./intel_o3.dat', delimiter=',')
df = pd.DataFrame(o3, columns=['N', 'R', 'elapsed_time', 'MB/s'])
o3 = df.groupby('N').mean().reset_index()

o3_avx = np.loadtxt('./intel_o3_AVX.dat', delimiter=',')
df = pd.DataFrame(o3_avx, columns=['N', 'R', 'elapsed_time', 'MB/s'])
o3_avx = df.groupby('N').mean().reset_index()

fast = np.loadtxt('./intel_fast.dat', delimiter=',')
df = pd.DataFrame(fast, columns=['N', 'R', 'elapsed_time', 'MB/s'])
fast = df.groupby('N').mean().reset_index()

plt.semilogx(o1['N'], o1['MB/s'], label='-O1')
plt.semilogx(o3['N'], o3['MB/s'], label='-O3')
plt.semilogx(o3_avx['N'], o3_avx['MB/s'], label='-O3 -xAVX')
plt.semilogx(fast['N'], fast['MB/s'], label='-fast')
plt.semilogx(stream[0], stream[1], label='STREAM')
plt.ylabel('MB/s')
plt.xlabel(r'$N$')
plt.legend()
# plt.show()
plt.savefig('icc.pdf')
plt.clf()
