%% 
% The code predicts the standard deviation, and correlation coefficients of 
% EDP residuals of building structures using the first and second DNN-based frameworks

% The details are found in Section 3 and 4 of the following reference.
% Kang, C., Kim, T., Kwon, O., and Song, J. (2023). Deep neural network-based 
% regional seismic loss assessment considering correlation between EDP residual 
% of building structures, Earthquake Engineering and Structural Dynamics, 
% https://doi.org/10.1002/eqe.3775.

% Developed by Chluyoung Kang from Korea Atomic Energy Research Institute (KAERI)
% Dec 8, 2022

clear; clc

%% First DNN-based framework
% Building i (Story: 9, Damping ratio: 2%)
% Building j (Story: 12, Damping ratio: 5%)
load('Building_data.mat')

[EDP_Var_i, xi_i, delta_i] = Func_Var(story_i, mu_i, std_i, corr_i, Gamman_i, Eigvec_i, h_i);
[EDP_Var_j, xi_j, delta_j] = Func_Var(story_j, mu_j, std_j, corr_j, Gamman_j, Eigvec_j, h_j);
EDP_Cov = Func_Cov(story_i, story_j, mu_i, mu_j, std_i, std_j, corr_ij, Gamman_i, Gamman_j, Eigvec_i, Eigvec_j, h_i, h_j);

% Equation (23) in the reference paper
Derived_corr = EDP_Cov/sqrt(EDP_Var_i)/sqrt(EDP_Var_j);

% Equation (25) in the reference paper
Derived_log_corr = 1/xi_i/xi_j*log(1+Derived_corr*delta_i*delta_j);

% Modification factor is introduced for pairs of the first mode period
% and damping ratio to improve the standard deviation in the form, 𝜎(𝑇_1,𝜉)=𝜎(𝑇_1,𝜉 = 0)×𝑀𝐹.
% Tables (4 & 5) in the reference paper
load('Modification factors.mat')

[~, zero_damp_xi_i] = Func_Var(story_i, mu_zero_damp_i, std_zero_damp_i, corr_zero_damp_i, Gamman_i, Eigvec_i, h_i);
[~, zero_damp_xi_j] = Func_Var(story_j, mu_zero_damp_j, std_zero_damp_j, corr_zero_damp_j, Gamman_j, Eigvec_j, h_j);

MF_i = interp2(Period_list, Damp_list, MF_IDR', T_1_i, Damp_i);
MF_j = interp2(Period_list, Damp_list, MF_IDR', T_1_j, Damp_j);

DNN_Model1_std_i = zero_damp_xi_i * MF_i;
DNN_Model1_std_j = zero_damp_xi_j * MF_j;
DNN_Model1_corr_ij = Derived_log_corr;

Results_DNN_Model1 = [DNN_Model1_std_i; DNN_Model1_std_j; DNN_Model1_corr_ij];

%% Second DNN-based framework
% Result from DNN_Model2.py
DNN_Model2_std_i = 0.3172;
DNN_Model2_std_j = 0.4014;
DNN_Model2_corr_ij = 0.7249;

Results_DNN_Model2 = [DNN_Model2_std_i; DNN_Model2_std_j; DNN_Model2_corr_ij];

%% Response history analysis (RHA)
RHA_std_i = 0.3169;
RHA_std_j = 0.4017;
RHA_corr_ij = 0.7258;

Results_RHA = [RHA_std_i; RHA_std_j; RHA_corr_ij];

%% Compare the results
Results = table([DNN_Model1_std_i; DNN_Model1_std_j; DNN_Model1_corr_ij],[DNN_Model2_std_i;DNN_Model2_std_j; DNN_Model2_corr_ij],[RHA_std_i; RHA_std_j; RHA_corr_ij],'VariableNames',{'DNN_Model1','DNN_Model2','RHA'},'RowNames',{'xi_i','xi_j','rho_ij'})
