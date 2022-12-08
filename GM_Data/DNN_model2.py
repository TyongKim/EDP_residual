"""
The code predicts thestandard deviation, and correlation coefficients of
the EDP residuals by using three deep neural network (DNN) models.

The DNN model is already trained by using a database consisting 38,000 building
structures with 19 building heights (from 2 to 20 stories), 
20 damping ratios (from0 to 40%), and 100 artificial variations. 
By using 1,499 ground motions, 56,962,000 ( = 38, 000 × 1, 499) EDP residuals of 
the building structures are employed.

The details are found in Section 4 of the following reference.
Kang, C., Kim, T., Kwon, O., and Song, J. (2023). Deep neural network-based 
regional seismic loss assessment considering correlation between EDP residual of 
building structures, Earthquake Engineering and Structural Dynamics, 
https://doi.org/10.1002/eqe.3775.

Developed by Chulyoung Kang from Korea Atomic Energy Research Institute (KAERI)
Dec 8, 2022
"""

# Import libraries
import numpy as np
import tensorflow as tf
from tensorflow import keras

#%% Import DNN models
NN_model_disp_std = keras.models.load_model('DNN_Model2_disp_std_final.h5')
NN_model_idr_std  = keras.models.load_model('DNN_Model2_idr_std_final.h5')

NN_model_disp_corr = keras.models.load_model('DNN_Model2_disp_corr_final.h5')
NN_model_idr_corr  = keras.models.load_model('DNN_Model2_idr_corr_final.h5')

#%% Target structural systems (we asuume a certain situation)
# ith structure
period_1_i = 1.379; period_2_i = 0.442; damping_i = 0.02
# jth structure
period_1_j = 1.883; period_2_j = 0.608; damping_j = 0.05

Input_std = np.array([[np.log(period_1_i), (period_1_i-period_2_i)/period_1_i, damping_i],
                      [np.log(period_1_j), (period_1_j-period_2_j)/period_1_j, damping_j]])

Input_corr = np.array([[np.log(period_1_i), (period_1_i-period_2_i)/period_1_i, damping_i,
                        np.log(period_1_j), (period_1_j-period_2_j)/period_1_j, damping_j]])                       

#%% Predict thorugh DNN models
# standard deviation (EDP: Roof displacement)
Output_disp_std = NN_model_disp_std.predict(Input_std)
Output_disp_std = np.exp(Output_disp_std)

# standard deviation (EDP: Maximum IDR)
Output_idr_std = NN_model_idr_std.predict(Input_std)
Output_idr_std = np.exp(Output_idr_std)

# Correlation coefficient (EDP: Roof displacement)
Output_disp_corr = NN_model_disp_corr.predict(Input_corr)

# Correlation coefficient (EDP: Maximum IDR)
Output_idr_std_corr = NN_model_idr_corr.predict(Input_corr)