# EDP_residual

## Software introduction
This software predicts the standard deviation and correlation of EDP residuals using deep neural network (DNN) models. This page shares codes to construct a database and develop DNN models. Note that due to the storage issue, the constructed database would not be shared but the trained DNN models can be downloaded.

## Developers
Developed by Chulyoung Kang (cykang@kaeri.re.kr), Taeyong Kim (tyong.kim@mail.utoronto.ca), Oh-Sung Kwon (os.kwon@utoronto.ca), and Junho Song (junhosong@snu.ac.kr)


Korea Atomic Energy Research Institute (KAERI), University of Toronto (UofT), and Seoul National University (SNU)

## Reference
Kang, C.1, Kim, T.1, Kwon, O., and Song, J. (2023). Deep neural network-based regional seismic loss assessment considering correlation between EDP residual of building structures, Earthquake Engineering and Structural Dynamics, (Accepted) 

The paper was invited to a special issue “AI and Data-driven Methods in Earthquake Engineering.”

## Required software and libraries
Python 3 with Numpy version '1.20.2', Scipy version '1.7.3', Tensorflow version '2.9.1'


OpenSees version '3.3.0'; https://opensees.berkeley.edu/OpenSees/user/download.php

## File description
1. Construct_SDDB.py: This code helps you construct a seismic demand database of linear single-degree-of-freedom (SDOF) systems having different stiffness (or period) and damping coefficients. To run this code, OpenSees is required. Moreover, a set of ground motions needs to be downloaded from the NGA-WEST database.

2. DNN_model1.py: This code helps users how to use the DNN model developed in Section 3 of the authors' paper. The mean, standard deviation, and correlation coefficients of the EDP residulas are predicted from the DNN models.

3. DNN_model2.py: This code helps users how to use the DNN model developed in Section 4 of the authors' paper. The standard deviation and correlation coefficients of the EDP resiudals are predicted from the DNN models.

4. Numerical_example.py: Thiis code copmares the predicted EDP residuals from the DNN model 1 and DNN model 2. Based on this code, users can easily write their own code for their projects or research.