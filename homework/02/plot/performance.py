import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams

rcParams['figure.figsize'] = 10, 5
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 15

N, M, B, speedup, l1_naiv, l1_opt, l2_naiv, l2_opt, l3_naiv, l3_opt = \
    np.loadtxt('../data.txt', unpack=True)

# speedup against B
B = B.astype(np.int32)
bs = np.unique(B)
su = []
for b in bs:
    mask = B == b
    su.append(np.average(speedup[mask]))
plt.plot(bs, su, '.')
plt.xlabel(r'$B$')
plt.ylabel('Average Speedup')
plt.savefig('speedup_for_all_bs.pdf')
plt.clf()

# cache misses and speedup against B for N=M=10000
B = B.astype(np.int32)
bs = np.unique(B)
bs = bs[bs <= 512]
l1 = []
l2 = []
l3 = []
su = []
for b in bs:
    mask = np.logical_and(B == b, np.logical_and(M == 10000, N == 10000))
    l1.append(np.average(l1_opt[mask]/l1_naiv[mask]))
    l2.append(np.average(l2_opt[mask]/l2_naiv[mask]))
    l3.append(np.average(l3_opt[mask]/l3_naiv[mask]))
    su.append(np.average(speedup[mask]))
plt.plot(bs, l3, '.', label='L3 Misses')
plt.plot(bs, l2, '.', label='L2 Misses')
plt.plot(bs, l1, '.', label='L1 Misses')
plt.plot(bs, su, '.', label='Speedup')
plt.axvline(32)
plt.axvline(285)
plt.xlabel(r'$B$')
plt.ylabel('Ratio Optimized/Naiv')
plt.legend(loc='lower left', bbox_to_anchor= (-.1, 1.01), ncol=8,
            borderaxespad=0, frameon=False)
# plt.show()
plt.savefig('square_against_B.pdf')
plt.clf()

# cache misses for a narrow matrix
B = B.astype(np.int32)
bs = np.unique(B)
bs = bs[bs <= 512]
l1 = []
l2 = []
l3 = []
su = []
for b in bs:
    mask = np.logical_and(B == b, np.logical_and(M == 100000, N == 200))
    l1.append(np.average(l1_opt[mask]/l1_naiv[mask]))
    l2.append(np.average(l2_opt[mask]/l2_naiv[mask]))
    l3.append(np.average(l3_opt[mask]/l3_naiv[mask]))
    su.append(np.average(speedup[mask]))
plt.plot(bs, l3, '.', label='L3 Misses')
plt.plot(bs, l2, '.', label='L2 Misses')
plt.plot(bs, l1, '.', label='L1 Misses')
plt.plot(bs, su, '.', label='Speedup')
plt.xlabel(r'$B$')
plt.ylabel('Ratio Optimized/Naiv')
plt.legend(loc='lower left', bbox_to_anchor= (-.1, 1.01), ncol=8,
            borderaxespad=0, frameon=False)
# plt.show()
plt.savefig('narrow_against_B.pdf')
plt.clf()

# cache misses for a wide matrix
l1 = []
l2 = []
l3 = []
su = []
for b in bs:
    mask = np.logical_and(B == b, np.logical_and(N == 100000, M == 200))
    l1.append(np.average(l1_opt[mask]/l1_naiv[mask]))
    l2.append(np.average(l2_opt[mask]/l2_naiv[mask]))
    l3.append(np.average(l3_opt[mask]/l3_naiv[mask]))
    su.append(np.average(speedup[mask]))
plt.plot(bs, l3, '.', label='L3 Misses')
plt.plot(bs, l2, '.', label='L2 Misses')
plt.plot(bs, l1, '.', label='L1 Misses')
plt.plot(bs, su, '.', label='Speedup')
plt.xlabel(r'$B$')
plt.ylabel('Ratio Optimized/Naiv')
plt.legend(loc='lower left', bbox_to_anchor= (-.1, 1.01), ncol=8,
            borderaxespad=0, frameon=False)
# plt.show()
plt.savefig('wide_against_B.pdf')
plt.clf()

# different square matrices for fixed B=200
mask = np.logical_and(N == M, B == 200)
l1 = l1_opt[mask]/l1_naiv[mask]
l2 = l2_opt[mask]/l2_naiv[mask]
l3 = l3_opt[mask]/l3_naiv[mask]
su = speedup[mask]

plt.plot(N[mask], l3, '.', label='L3 Misses')
plt.plot(N[mask], l2, '.', label='L2 Misses')
plt.plot(N[mask], l1, '.', label='L1 Misses')
plt.plot(N[mask], su, '.', label='Speedup')
plt.xlabel(r'$N$')
plt.ylabel('Ratio Optimized/Naiv')
plt.legend(loc='lower left', bbox_to_anchor= (-.1, 1.01), ncol=8,
            borderaxespad=0, frameon=False)
# plt.show()
plt.savefig('fixed_B_different_squares.pdf')
plt.clf()

# different square matrices for fixed B=200
mask = np.logical_and(N == M, B == 200)
l1 = l1_opt[mask]/l1_naiv[mask]
l2 = l2_opt[mask]/l2_naiv[mask]
l3 = l3_opt[mask]/l3_naiv[mask]
su = speedup[mask]

plt.plot(N[mask], l3, '.', label='L3 Misses')
plt.plot(N[mask], l2, '.', label='L2 Misses')
plt.plot(N[mask], l1, '.', label='L1 Misses')
plt.plot(N[mask], su, '.', label='Speedup')
plt.xlabel(r'$N=M$')
plt.ylabel('Ratio Optimized/Naiv')
plt.legend(loc='lower left', bbox_to_anchor= (-.1, 1.01), ncol=8,
            borderaxespad=0, frameon=False)
# plt.show()
plt.savefig('fixed_B_different_squares.pdf')
plt.clf()

# B=200, M=10000 N varied
mask = np.logical_and(M == 10000, B == 200)
l1 = l1_opt[mask]/l1_naiv[mask]
l2 = l2_opt[mask]/l2_naiv[mask]
l3 = l3_opt[mask]/l3_naiv[mask]
su = speedup[mask]

plt.plot(N[mask], l3, '.', label='L3')
plt.plot(N[mask], l2, '.', label='L2')
plt.plot(N[mask], l1, '.', label='L1')
plt.plot(N[mask], su, '.', label='Speedup')
plt.xlabel(r'$N$')
plt.ylabel('Ratio Optimized/Naiv')
plt.legend(loc='lower left', bbox_to_anchor= (-.1, 1.01), ncol=8,
            borderaxespad=0, frameon=False)
# plt.show()
plt.savefig('fixed_B_M_different_N.pdf')
plt.clf()

# B=200, N=10000 M varied
mask = np.logical_and(N == 10000, B == 200)
l1 = l1_opt[mask]/l1_naiv[mask]
l2 = l2_opt[mask]/l2_naiv[mask]
l3 = l3_opt[mask]/l3_naiv[mask]
su = speedup[mask]

plt.plot(M[mask], l3, '.', label='L3')
plt.plot(M[mask], l2, '.', label='L2')
plt.plot(M[mask], l1, '.', label='L1')
plt.plot(M[mask], su, '.', label='Speedup')
plt.xlabel(r'$M$')
plt.ylabel('Ratio Optimized/Naiv')
plt.legend(loc='lower left', bbox_to_anchor= (-.1, 1.01), ncol=8,
            borderaxespad=0, frameon=False)
# plt.show()
plt.savefig('fixed_B_N_different_M.pdf')
plt.clf()
