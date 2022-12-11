"""
The code shows an architecutre of DNN models used in "DNN_model1.py."


The details are found in Section 3 of the following reference.
Kang, C., Kim, T., Kwon, O., and Song, J. (2023). Deep neural network-based 
regional seismic loss assessment considering correlation between EDP residual of 
building structures, Earthquake Engineering and Structural Dynamics, 
https://doi.org/10.1002/eqe.3775.

Developed by Taeyong Kim from the University of Toronto
Dec 11, 2022
"""

# Import libraries
from tensorflow import keras

#%% Three DNN models are presented as follows
# Mean model
def define_model_mean():
    input_mnist = keras.Input(shape=(3,))
    model1 = keras.layers.Dense(units=64)(input_mnist)
    model1 = keras.layers.Activation(activation='relu')(model1)
    model1 = keras.layers.Dense(units=32)(model1)
    model1 = keras.layers.Activation(activation='relu')(model1)
    model1 = keras.layers.Dense(units=16)(model1)
    model1 = keras.layers.Activation(activation='relu')(model1)
    model1 = keras.layers.Dense(units=32,
                                kernel_regularizer 
                                = keras.regularizers.L2(0.0002))(model1)
    model1 = keras.layers.Activation(activation='relu')(model1)    
    model1 = keras.layers.Dense(units=64,
                                kernel_regularizer 
                                = keras.regularizers.L2(0.0002))(model1)
    model1 = keras.layers.Activation(activation='relu')(model1)
    model1 = keras.layers.Dense(units=1)(model1)
    model1 = keras.layers.Activation(activation='linear')(model1)    

    return keras.Model(inputs=input_mnist, outputs=model1)

NN_model_mean = define_model_mean()

# Standard deviation model
def define_model_std():
    input_mnist = keras.Input(shape=(3,))
    model1 = keras.layers.Dense(units=64)(input_mnist)
    model1 = keras.layers.Activation(activation='relu')(model1)
    model1 = keras.layers.Dense(units=32)(model1)
    model1 = keras.layers.Activation(activation='relu')(model1)
    model1 = keras.layers.Dense(units=16)(model1)
    model1 = keras.layers.Activation(activation='relu')(model1)
    model1 = keras.layers.Dense(units=32)(model1)
    model1 = keras.layers.Activation(activation='relu')(model1)    
    model1 = keras.layers.Dense(units=64,
                                kernel_regularizer 
                                = keras.regularizers.L2(0.0001))(model1)
    model1 = keras.layers.Activation(activation='relu')(model1)
    model1 = keras.layers.Dense(units=1)(model1)
    model1 = keras.layers.Activation(activation='linear')(model1)    

    return keras.Model(inputs=input_mnist, outputs=model1)

NN_model_std = define_model_std()

# Correlation model
def define_model_corr():
    input_mnist = keras.Input(shape=(6,1))
    model1 = keras.layers.Conv1D(filters = 32, 
                                 kernel_size=2, padding='same')(input_mnist)
    model1 = keras.layers.Activation(activation='relu')(model1)  
    model1 = keras.layers.Conv1D(filters = 64,
                                 kernel_size=2, padding='same')(model1)
    model1 = keras.layers.Activation(activation='relu')(model1)
    model1 = keras.layers.Flatten()(model1)

    
    model2 = keras.layers.Conv1D(filters = 32, 
                                 kernel_size=4, padding='same')(input_mnist)
    model2 = keras.layers.Activation(activation='relu')(model2)   
    model2 = keras.layers.Conv1D(filters = 64,
                                 kernel_size=4, padding='same')(model2)
    model2 = keras.layers.Activation(activation='relu')(model2)
    model2 = keras.layers.Flatten()(model2)
    
    model = keras.layers.concatenate([model1, model2], axis = 1)
    
    model = keras.layers.Dense(units=128)(model)
    model = keras.layers.Activation(activation='relu')(model)   
    model = keras.layers.Dense(units=64)(model)
    model = keras.layers.Activation(activation='relu')(model)   
    model = keras.layers.Dense(units=1)(model)
    model = keras.layers.Activation(activation='tanh')(model)    

    return keras.Model(inputs=input_mnist, outputs=model)


NN_model_corr = define_model_corr()
