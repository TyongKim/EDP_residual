"""
The code predicts the mean, standard deviation, and correlation coefficients of
the EDP residuals by using three deep neural network (DNN) models.

The DNN model is already trained by using a seismic demand database that is 
constructed through "Construct_SDDB.py"

The details are found in Section 3 of the following reference.
Kang, C., Kim, T., Kwon, O., and Song, J. (2023). Deep neural network-based regional seismic loss assessment considering correlation between EDP residual of building structures, Earthquake Engineering and Structural Dynamics, https://doi.org/10.1002/eqe.3775.


Developed by Taeyong Kim from the University of Toronto
Nov 12, 2022
"""

# Import libraries
import numpy as np
import tensorflow as tf
from tensorflow import keras

#%% Import period and damping values
Stiffness = np.load('stiffness.npy')
g = 9.81 # gravitational acceleration
period = 2*np.pi*np.sqrt(1/g/Stiffness);
damping = np.asarray([0.00, 0.001, 0.005, 0.010, 0.015,
                      0.02, 0.025, 0.03, 0.035, 0.04, 
                      0.05, 0.07, 0.10, 0.12, 0.15, 
                      0.20, 0.25, 0.30, 0.35, 0.40]) # 20 steps

#%% Import DNN models

NN_model_mean =  keras.models.load_model('DNN_Model1_mean_final.h5')
NN_model_std =  keras.models.load_model('DNN_Model1_std_final.h5')
NN_model_corr = keras.models.load_model('DNN_Model1_corr_final.h5')

#%% Target structural systems (we asuume a certain situation)
# ith structure
period_1_i = 0.32; period_k_i = 0.095; damping_k_i = 0.02
# jth structure
period_1_j = 3.377; period_j_l = 0.7; damping_l_j = 0.05

Input_DNN = np.array([[np.log(period_1_i), (period_1_i-period_k_i)/period_1_i, damping_k_i],
                      [np.log(period_1_j), (period_1_j-period_j_l)/period_1_j, damping_l_j]])

Input_corr = np.array([[np.log(period_1_i), (period_1_i-period_k_i)/period_1_i, damping_k_i,
                        np.log(period_1_j), (period_1_j-period_j_l)/period_1_j, damping_l_j]])           

#%% Predict thorugh DNN models
# Mean
Output_mean = NN_model_mean.predict(Input_DNN)
Output_mean = np.exp(Output_mean)

# standard deviation
Output_std = NN_model_std.predict(Input_DNN)
Output_std = np.exp(Output_std)

# Correlation coefficient
Output_corr = NN_model_corr.predict(Input_corr)

