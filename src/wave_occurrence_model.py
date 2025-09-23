# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:00:47 2025

@author: 368809
"""
# wave flag
# H-left column, He-right column
# (1)-wave, (0)-no wave, (-1)-N/A due to no input

import numpy as np
                
# load wave model
file_path = '../data/wave_occurrence_model_XGBoost.npy'

file = '../data/Bw.npz'

data = np.load(file)

var_name = np.array(['tilt_1min', 'f107interpol_1min', 'hp30_1min', 'hp30star_1min', 'pdyn_1min', 'p_l', 'p_mlt', 'p_mlat', 'p_dlpp', 'p_lpp'])

restored_array = np.load(file_path, allow_pickle=True)
RA_item = restored_array.item()
RA_keys = RA_item.keys()
model_h = RA_item['model_h']
model_he = RA_item['model_he']
# load wave model

thr = np.loadtxt('../input/Threshold.txt')
threshold_h = thr[0]
threshold_he = thr[1]

# load input file
# input format --> 'tilt_1min', 'f107interpol_1min', 'hp30_1min', 'hp30star_1min', 'pdyn_1min', 'p_l', 'p_mlt', 'p_mlat', 'p_dlpp', 'p_lpp'
res = np.loadtxt('../input/RF_model_input.txt') # 
# load input file

flag_h = np.full(len(res), -1)
flag_he = np.full(len(res), -1)

X_test = res

idx_fin = np.argwhere(~np.isnan(np.sum(X_test, axis = 1)))
idx_fin = np.reshape(idx_fin, np.shape(idx_fin)[0])
X_test = X_test[idx_fin, :]



# H-band model run
flag_h_tmp = model_h.predict_proba(X_test)
flag_h_tmp = (flag_h_tmp[:, 1] > threshold_h).astype(int)

# H-band model run
flag_he_tmp = model_he.predict_proba(X_test)
flag_he_tmp = (flag_he_tmp[:, 1] > threshold_he).astype(int)


flag_h[idx_fin] = flag_h_tmp
flag_he[idx_fin] = flag_he_tmp

data = np.transpose(np.vstack((flag_h, flag_he)))
np.savetxt('../output/output_Occurrence.dat', data, fmt='%d', delimiter='\t')
