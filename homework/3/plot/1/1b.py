import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pylab import rcParams

rcParams['figure.figsize'] = 10, 5
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 15

# ----------------------------------- GCC -------------------------------------
o1 = np.loadtxt('./gcc_o1.dat', delimiter=',')
df = pd.DataFrame(o1, columns=['N', 'R', 'elapsed_time', 'GFLOP/s'])
o1 = df.groupby('N').mean().reset_index()

o3 = np.loadtxt('./gcc_o3.dat', delimiter=',')
df = pd.DataFrame(o3, columns=['N', 'R', 'elapsed_time', 'GFLOP/s'])
o3 = df.groupby('N').mean().reset_index()

o3_native = np.loadtxt('./gcc_o3_native.dat', delimiter=',')
df = pd.DataFrame(o3_native, columns=['N', 'R', 'elapsed_time', 'GFLOP/s'])
o3_native = df.groupby('N').mean().reset_index()

plt.semilogx(o1['N'], o1['GFLOP/s'], label='-O1')
plt.semilogx(o3['N'], o3['GFLOP/s'], label='-O3')
plt.semilogx(o3_native['N'], o3_native['GFLOP/s'], label='-O3 -march=native')
plt.axhline(2.4, ls='--', label='Theoretical 1 FLOP/Cycle')
plt.axhline(2*2.4, ls='--', label='Theoretical FMA (2 FLOP/Cycle)')
plt.ylabel('GFLOP/s')
plt.xlabel(r'$N$')
plt.legend()
# plt.show()
plt.savefig('1b_gcc.pdf')
plt.clf()

# ---------------------------------- Intel ------------------------------------
o1 = np.loadtxt('./intel_o1.dat', delimiter=',')
df = pd.DataFrame(o1, columns=['N', 'R', 'elapsed_time', 'GFLOP/s'])
o1 = df.groupby('N').mean().reset_index()

o3 = np.loadtxt('./intel_o3.dat', delimiter=',')
df = pd.DataFrame(o3, columns=['N', 'R', 'elapsed_time', 'GFLOP/s'])
o3 = df.groupby('N').mean().reset_index()

o3_avx = np.loadtxt('./intel_o3_AVX.dat', delimiter=',')
df = pd.DataFrame(o3_avx, columns=['N', 'R', 'elapsed_time', 'GFLOP/s'])
o3_avx = df.groupby('N').mean().reset_index()

fast = np.loadtxt('./intel_fast.dat', delimiter=',')
df = pd.DataFrame(fast, columns=['N', 'R', 'elapsed_time', 'GFLOP/s'])
fast = df.groupby('N').mean().reset_index()

plt.semilogx(o1['N'], o1['GFLOP/s'], label='-O1')
plt.semilogx(o3['N'], o3['GFLOP/s'], label='-O3')
plt.semilogx(o3_avx['N'], o3_avx['GFLOP/s'], label='-O3 -xAVX')
plt.semilogx(fast['N'], fast['GFLOP/s'], label='-fast')
plt.axhline(2.4, ls='--', label='Theoretical 1 FLOP/Cycle')
plt.axhline(2*2.4, ls='--', label='Theoretical FMA (2 FLOP/Cycle)')
plt.ylabel('GFLOP/s')
plt.xlabel(r'$N$')
plt.legend()
# plt.show()
plt.savefig('1b_icc.pdf')
plt.clf()
