# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 13:42:46 2025

@author: 368809
"""

import numpy as np

def wave_power_model(GEOIND, Lval, MLTval, NOS=100, SIMPLE=False):

    file = '../data/Bw.npz'
    
    data = np.load(file)
    
    bw_prob_model = data['bw_prob_model']
    L_prob = data['L_val']
    MLT_prob = data['MLT_val']
    xx_prob = data['Bw_log']
    Hp30_range = data['Hp30_Level']
    BAND_STR = data['BAND_STR']
    
    dL_prob = L_prob[1] - L_prob[0]
    dMLT_prob = MLT_prob[1] - MLT_prob[0]

    GEOIND = np.asarray(GEOIND)
    Lval = np.asarray(Lval)
    MLTval = np.asarray(MLTval)

    n_times = len(GEOIND)
    bw_model = np.full((n_times, len(BAND_STR), NOS), np.nan) # time x band x # of samples
    bw_model_MED = np.full((n_times, len(BAND_STR)), np.nan)
    bw_model_025 = np.full((n_times, len(BAND_STR)), np.nan)
    bw_model_050 = np.full((n_times, len(BAND_STR)), np.nan)
    bw_model_075 = np.full((n_times, len(BAND_STR)), np.nan)

    # Monte Carlo Sampling
    rng = np.random.default_rng()

    for TT in range(n_times):
        LL = np.where((Lval[TT] >= L_prob) & (Lval[TT] < L_prob + dL_prob))[0]
        MM = np.where((MLTval[TT] >= MLT_prob) & (MLTval[TT] < MLT_prob + dMLT_prob))[0]
        AA = np.where((GEOIND[TT] >= Hp30_range[:-1]) & (GEOIND[TT] < Hp30_range[1:]))[0]

        if len(LL) == 0 or len(MM) == 0 or len(AA) == 0:
            continue

        bw_prob_tmp = bw_prob_model[LL[0], MM[0], :, AA[0], :]  # Shape: power_bin x band
        bw_cumul = np.cumsum(bw_prob_tmp, axis=0) * (xx_prob[1] - xx_prob[0])

        # Sampling using inverse transform method
        for BIDX in range(len(BAND_STR)):
            rand_vals = rng.uniform(size=NOS)
            interpolated_vals = np.interp(rand_vals, bw_cumul[:, BIDX], xx_prob)
            bw_model[TT, BIDX, :] = np.sqrt(10 ** interpolated_vals)

            bw_model_MED[TT, BIDX] = np.median(bw_model[TT, BIDX, :])
            bw_model_025[TT, BIDX] = np.sqrt(10 ** np.interp(0.16, bw_cumul[:, BIDX], xx_prob)) # lower bound 16% quantile; equivalent to 1sigma
            bw_model_050[TT, BIDX] = np.sqrt(10 ** np.interp(0.5, bw_cumul[:, BIDX], xx_prob)) # median 50% quantile
            bw_model_075[TT, BIDX] = np.sqrt(10 ** np.interp(0.84, bw_cumul[:, BIDX], xx_prob)) # upper bound 84% quantile; equivalent to 1sigma

    if SIMPLE:
        return {
            'bw_model': bw_model,
            'Variables': ['GEOIND', 'BAND (He, H)', '# OF SAMPLE']
        }
    else:
        return {
            'bw_model': bw_model,
            'bw_model_LOW': bw_model_025,
            'bw_model_MED': bw_model_050,
            'bw_model_HIGH': bw_model_075,
            'Variables': ['GEOIND', 'BAND (He, H)', 'MEDIAN', 'LOW [0.16]', 'MED [0.50]', 'HIGH [0.84]']
        }


# script starts

# load input file
# input format --> 'tilt_1min', 'f107interpol_1min', 'hp30_1min', 'hp30star_1min', 'pdyn_1min', 'p_l', 'p_mlt', 'p_mlat', 'p_dlpp', 'p_lpp'
res = np.loadtxt('../input/RF_model_input.txt')
# load input file

# GEOIND = res[:, 2]
# Lval = np.linspace(3, 6, num=len(GEOIND))
# MLTval =  np.full(len(GEOIND), 16)

GEOIND = res[:, 2]
Lval = res[:, 5]
MLTval = res[:, 6]

res = wave_power_model(GEOIND, Lval, MLTval, NOS=100, SIMPLE=False)

data = np.full((len(GEOIND), 6), np.nan) # time, [Low He, Med He, High He, Low H, Med H, High H]
data[:, 0] = res['bw_model_LOW'][:, 0]
data[:, 1] = res['bw_model_MED'][:, 0]
data[:, 2] = res['bw_model_HIGH'][:, 0]
data[:, 3] = res['bw_model_LOW'][:, 1]
data[:, 4] = res['bw_model_MED'][:, 1]
data[:, 5] = res['bw_model_HIGH'][:, 1]

# write wave power in .dat
np.savetxt('../output/output_Bw.dat', data, fmt='%-10s', header='LowerBound(He)\tMedian(He)\tUpperBound(He)\tLowerBound(H)\tMedian(H)\tUpperBound(H)')



