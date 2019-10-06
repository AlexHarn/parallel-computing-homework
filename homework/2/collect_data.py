import numpy as np
import matplotlib.pyplot as plt
import os

RUN_PATH = './RUNS/'

data = []
for fn in os.listdir(RUN_PATH):
    try:
        N, M, B = fn.split('_')
    except ValueError:
        continue
    # extract speedup
    if os.path.isfile(RUN_PATH + fn + '/out'):
        with open(RUN_PATH + fn + '/out', 'r') as out:
            s = out.read()
            if len(s) > 0:
                speedup = float(s.replace('\n', '')[-4:])
            else:
                continue
    # extract L1 misses
    if os.path.isfile(RUN_PATH + fn + '/L1'):
        with open(RUN_PATH + fn + '/L1', 'r') as out:
            s = out.read()
            if len(s) > 0:
                for line in s.split('\n'):
                    if 'optMultiplication' in line:
                        l1_opt = float(" ".join(line.split()).split(' ')[2])
                    elif 'naiveMultiplication' in line:
                        l1_naiv = float(" ".join(line.split()).split(' ')[2])
    # extract L2 misses
    if os.path.isfile(RUN_PATH + fn + '/L2'):
        with open(RUN_PATH + fn + '/L2', 'r') as out:
            s = out.read()
            if len(s) > 0:
                for line in s.split('\n'):
                    if 'optMultiplication' in line:
                        l2_opt = float(" ".join(line.split()).split(' ')[2])
                    elif 'naiveMultiplication' in line:
                        l2_naiv = float(" ".join(line.split()).split(' ')[2])
    # extract L3 misses
    if os.path.isfile(RUN_PATH + fn + '/L3'):
        with open(RUN_PATH + fn + '/L3', 'r') as out:
            s = out.read()
            if len(s) > 0:
                for line in s.split('\n'):
                    if 'optMultiplication' in line:
                        l3_opt = float(" ".join(line.split()).split(' ')[2])
                    elif 'naiveMultiplication' in line:
                        l3_naiv = float(" ".join(line.split()).split(' ')[2])
    data.append([int(N), int(M), int(B), speedup,
                 l1_naiv, l1_opt,
                 l2_naiv, l2_opt,
                 l3_naiv, l3_opt])

data = np.asarray(data)
np.savetxt('data.txt', data,
           header='N M B speedup l1_naiv l1_opt l2_naiv l2_opt l3_naiv l3_opt')
