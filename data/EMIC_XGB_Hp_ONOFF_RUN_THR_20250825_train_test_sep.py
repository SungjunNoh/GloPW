# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 15:24:24 2025

@author: 368809
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:00:47 2025

@author: 368809
"""

import site
site.addsitedir(r"C:\Users\368809\Anaconda3")

import sys
sys.path.append(r"C:\Users\368809\Anaconda3")
import numpy as np

                
print(sys.path)

ver = '20250825_train_test_sep'
# load wave model
# file_path = 'C:\\Users\\368809\\sjnoh\\Project\\CK\\EMIC\\Data\\RandomForest_Model\\model_xgb_Hp_PAB_20250131_threshold.npy'
file_path = 'C:\\Users\\368809\\sjnoh\\Project\\CK\\EMIC\\Data\\RandomForest_Model\\model_xgb_Hp_PAB_SMOTE_'+ver+'_threshold.npy'


var_name = np.array(['tilt_1min', 'f107interpol_1min', 'hp30_1min', 'hp30star_1min', 'pdyn_1min', 'p_l', 'p_mlt', 'p_mlat', 'p_dlpp', 'p_lpp'])

restored_array = np.load(file_path, allow_pickle=True)
RA_item = restored_array.item()
RA_keys = RA_item.keys()
model_h = RA_item['model_h']
model_he = RA_item['model_he']
# load wave model


thr = np.loadtxt(r'C:\Users\368809\sjnoh\Project\CK\EMIC\Data\RandomForest_Model\input\Threshold.txt')
threshold_h = thr[0]
threshold_he = thr[1]

# load input file
res = np.loadtxt(r'C:\Users\368809\sjnoh\Project\CK\EMIC\Data\RandomForest_Model\input\RF_model_input.txt')
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
np.savetxt(r'C:\Users\368809\sjnoh\Project\CK\EMIC\Data\RandomForest_Model\input\RF_model_output.txt', data, fmt='%d', delimiter='\t')
