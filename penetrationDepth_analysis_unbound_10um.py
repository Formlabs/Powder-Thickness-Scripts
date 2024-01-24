#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:19:01 2023

@author: iris.celebi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 17:13:51 2023

@author: iris.celebi

"""

import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog

from scipy.optimize import curve_fit
import pandas as pd
import seaborn as sns

import argparse

def askFilePath():
    root = tk.Tk()
    root.withdraw()    
    file_path = filedialog.askopenfilename()
    #file_path = filedialog.askdirectory()
    return file_path


def exp_fit(measurement: np.array, d: np.array):
    """_summary_

    Args:
        measurement (np.array): numpy array of measured intensity as a function of thickness

    Returns:
        Output of exp fitting (I_0, alpha), where
            exp function is of the form f(d) = I_0 * exp(-1 * alpha * (d - c)) 
    """

    alpha_guess = 0.02                # corresponds to 50um
    c_guess = 5
    
    p_fit, cov_matrix = curve_fit(exponential_decay, d, measurement, p0=[alpha_guess, c_guess])
    #p_fit, cov_matrix = curve_fit(exponential_decay, d, measurement, p0=[alpha_guess, c_guess],
                               #bounds=([0, -30], [np.inf, 100]))
    
    alpha_fit, c_fit = p_fit    
    penetration_depth = 1/alpha_fit
    
    # Calculate standard errors for fitted parameters
    std_err_I_0 = np.sqrt(cov_matrix[0, 0])
    std_err_alpha = np.sqrt(cov_matrix[1, 1])
    # Calculate the 95% confidence interval for the fitted curve
    confidence_interval = 1.96 * np.array([std_err_I_0, std_err_alpha])  

    return alpha_fit, c_fit, penetration_depth, confidence_interval

def inv_exp_fit(measurement: np.array, d: np.array, c: float):
    """_summary_

    Args:
        measurement (np.array): numpy array of measured intensity as a function of thickness

    Returns:
        Output of exp fitting (I_0, alpha), where
            exp function is of the form f(d) = I_0 * exp(-1 * alpha * d) 
    """

    I_0_guess = np.max(measurement)
    alpha_guess = 0.02                # in microns
    
    
    p_fit, cov_matrix = curve_fit(inv_exponential_decay, d, measurement, p0=[I_0_guess, alpha_guess, c])
    # Extract the fitted parameters
    I_0_fit, alpha_fit, c = p_fit    

    
    # Calculate standard errors for fitted parameters
    std_err_I_0 = np.sqrt(cov_matrix[0, 0])
    std_err_alpha = np.sqrt(cov_matrix[1, 1])
    # Calculate the 95% confidence interval for the fitted curve
    confidence_interval = 1.96 * np.array([std_err_I_0, std_err_alpha])  # 95% confidence interval

    return I_0_fit, alpha_fit, confidence_interval


def exponential_decay(d: np.array, alpha: float, c: float):
    """Returns the exp function

    Args:
        d (np.array): Array of length values
        I_0 (float): Initial light intentisty
        alpha (float): attenuation coefficient

    Returns:
        np.array: exp decay function of d
    """
    return 100 * np.exp(-1 * alpha * (d - c)) # doesnt really change much
    #return I_0 * np.exp(-1 * alpha * d)


def inv_exponential_decay(d: np.array, I_0: float, alpha: float, c: float):
    """Returns the exp function

    Args:
        d (np.array): Array of length values
        I_0 (float): Initial light intentisty
        alpha (float): attenuation coefficient

    Returns:
        np.array: exp decay function of d
    """
    return (1 - (np.exp(-1 * alpha * (d - c))))*I_0
            


def analyze(df, filename, include_zero=False):
   # df is a pandas.DataFrame as generated by:
   # df = pd.read_csv(path, header=None)
    
    #x_val_rownums = df[df.iloc[:,0] == "Adjusted, direct"].index.tolist()
    #print(f"Adjusted, direct: row numbers: {x_val_rownums}")

    #d_values = df.iloc[1, 2:].values.astype(float)
    #d_values = df.iloc[x_val_rownums[0], 2:].values.astype(float)

    if include_zero:
        # first line includes zero point
        d_values = df["Thickness"].values

    else:
        # this line excludes zero point
        d_values = df["Thickness"].values[1:]


    # try with base data, which should be immediately above the adjusted data
    #d_values = df.iloc[x_val_rownums[0] -1, 2:].values.astype(float)
    
    d_plot = np.linspace(0, 500, 500)
    
    #reflectance_baseline = float(df.iloc[2, 0])/0.99
    # below is original but probably wrong because there's a date at the top in A1 which was supposedly not there when Iris was using this
    #reflectance_measurements =  df.iloc[2:4, 2:].values.astype(float)   

    # instead, this is correct
    #reflectance_measurements =  df.iloc[3:5, 2:].values.astype(float)   

    # however, I want to extract below the row titled, "Adjusted, direct" because the row numbers may get messed up as I do my thing
    # assume the first mention of "Adjusted, direct" is associated with reflectance, and the second mention is associated with transmission
    # create a list of indices of rows with "Adjusted, direct":
    
    #reflectance_baseline = float(df.iloc[x_val_rownums[0]+1, 0])/0.99
    #reflectance_measurements =  df.iloc[x_val_rownums[0]+1:x_val_rownums[0]+3, 2:].values.astype(float)   
    ##reflectance_measurements = reflectance_measurements - float(df.iloc[2, 1]) 
    #reflectance_measurements = reflectance_measurements - float(df.iloc[x_val_rownums[0]+1, 1]) 
    #reflectance_measurements = reflectance_measurements / reflectance_baseline *100
    
    #transmission_baseline = float(df.iloc[x_val_rownums[1]+1, 0])
    #transmission_measurements = df.iloc[x_val_rownums[1] + 1:x_val_rownums[1] + 3, 2:].values.astype(float) / transmission_baseline *100

    if include_zero:
        # first line takes all values including zero
        transmission_measurements = df["Relative_Transmission"].values*100

    else:
        # this line ignores zero
        transmission_measurements = df["Relative_Transmission"].values[1:]*100
    

    # TRANSMISSION
    
    #t_mean_measured = np.mean(transmission_measurements, axis=0)
    #t_range_values = np.max(transmission_measurements,axis=0) - np.min(transmission_measurements,axis=0)   
    
    # we're ignoring the zero point
    #t_alpha_fit, t_c_fit, penetration_depth, confidence_interval = exp_fit(transmission_measurements[1:], d_values[1:])
    t_alpha_fit, t_c_fit, penetration_depth, confidence_interval = exp_fit(transmission_measurements, d_values)
    #t_alpha_fit, t_c_fit, penetration_depth, confidence_interval = exp_fit(t_mean_measured[np.isfinite(t_mean_measured)], d_values[np.isfinite(d_values)])
    transmission_fit = exponential_decay(d_plot, t_alpha_fit, t_c_fit)
    

    # REFLECTION
    
    #r_mean_measured = np.mean(reflectance_measurements, axis=0)
    
    ##r_I_0_fit, r_alpha_fit, confidence_interval_r = inv_exp_fit(r_mean_measured[0:], d_values[0:], t_c_fit)
    #r_I_0_fit, r_alpha_fit, confidence_interval_r = inv_exp_fit(r_mean_measured[np.isfinite(r_mean_measured)], d_values[np.isfinite(d_values)], t_c_fit)
    #reflection_fit = inv_exponential_decay(d_plot, r_I_0_fit, r_alpha_fit, t_c_fit)
   
    
   # ABSORBANCE
    
    #absorbance = 100 - (transmission_fit + reflection_fit)
   
   
    
   # PLOT
   
    plt.rcParams['font.size'] = 20
    plt.figure(figsize=(10, 6))
    
    #sns.scatterplot(x=d_values, y=r_mean_measured, color='green', label='Measured R', s = 100)
    #sns.lineplot(x=d_plot, y=reflection_fit, color='green')    
    #plt.errorbar(x=d_values, y=r_mean_measured, yerr=t_range_values, fmt='o', color='green', alpha=0.5, elinewidth=2.5)
        
    #sns.scatterplot(x=d_values, y=t_mean_measured, color='blue', label='Measured T', s = 100)
    sns.scatterplot(x=d_values, y=transmission_measurements, color='blue', label='Measured T', s = 100)
    sns.lineplot(x=d_plot, y=transmission_fit, color='blue', label=f'Dp = {1/t_alpha_fit:.2f} um')
    
    confidence_bounds = np.array([transmission_fit + confidence_interval[0], 
                                  transmission_fit - confidence_interval[0]])
    
    plt.fill_between(d_plot, confidence_bounds[0], confidence_bounds[1], color='lightblue', alpha=0.5)   
    #plt.errorbar(x=d_values, y=t_mean_measured, yerr=t_range_values, fmt='o', color='blue', alpha=0.5, elinewidth=2.5)

    print(f"penetration_depth: {penetration_depth :.2f}")
    print(f"95% Confidence Interval for penetration_depth: [{penetration_depth - confidence_interval[0]:.2f}, {penetration_depth + confidence_interval[0]:.2f}]")

    #sns.scatterplot(x=d_values, y=100 - (t_mean_measured + r_mean_measured), color='red', label='Calculated A', s = 100)
    #sns.lineplot(x=d_plot, y=absorbance, color='red')   
    ##filtered = savgol_filter(100 - (t_mean_measured + r_mean_measured), window_length=6, polyorder=3)
    ##sns.lineplot(x=d_values, y=filtered, color='red')     
    
    sns.despine()
    plt.ylim(0, 110)
    #plt.xlim(t_c_fit-5, 500)
    plt.xlim(0, 500)
    plt.xlabel('Thickness Values (um)')
    plt.ylabel('Intensity')
    plt.title(filename)
    plt.legend()
    plt.show()
    
    #%%
    # Calculate total abs by accounting for reflection
    
    total_absorbance = []
    
    for d in d_plot:
        
        d_transmittance = exponential_decay(d, t_alpha_fit, t_c_fit)
        #d_reflectance = inv_exponential_decay(d, r_I_0_fit, r_alpha_fit, t_c_fit)
        
        #d_absorbance = 100 - (d_transmittance + d_reflectance)
        
        #total_absorbance.append(d_absorbance + d_transmittance/100 * inv_exponential_decay(1000, r_I_0_fit, r_alpha_fit, t_c_fit)/100 * d_absorbance)
        

    # Create a new figure and plot the total absorbance values
    
    d_transmittance_110 = exponential_decay(110, t_alpha_fit, t_c_fit)
    #d_reflectance_110 = inv_exponential_decay(110, r_I_0_fit, r_alpha_fit, t_c_fit)
    #d_absorbance_110 = 100 - (d_transmittance_110 + d_reflectance_110)
    
    #total_absorbance_110 = d_absorbance_110 + d_transmittance_110/100*inv_exponential_decay(1000, r_I_0_fit, r_alpha_fit, t_c_fit)/100 * d_absorbance_110
    
    
    d_value = 110 #um layer thickness
    ind = np.argmin(np.abs(d_plot - d_value))
    
    print(f'Transmission at 110um = {exponential_decay(d_value, t_alpha_fit, t_c_fit):.2f}')
    print(f'Transmission bulk = {exponential_decay(500, t_alpha_fit, t_c_fit):.2f}')
    
    #print(f'Reflectance at 110um = {inv_exponential_decay(d_value, r_I_0_fit, r_alpha_fit, t_c_fit):.2f}')
    #print(f'Reflectance bulk = {inv_exponential_decay(500, r_I_0_fit, r_alpha_fit, t_c_fit):.2f}')

    #print(f'Absorbance at 110um = {absorbance[ind]:.2f}')
    #print(f'Absorbance bulk = {absorbance[-1]:.2f}')
    #print(f'Total Absorbance at 110um = {total_absorbance_110:.2f}')
    print(f'C = {t_c_fit}')
    
    
    
    
    '''
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=d_plot, y=total_absorbance, color='purple', label='Total Absorbance')
    sns.lineplot(x=d_plot, y=absorbance, color='red', label='Absorbance')
    plt.xlabel('Thickness Values (um)')
    plt.ylabel('Intensity %')
    plt.title('Total absorbance calculation')
    plt.legend()
    plt.show()
    '''
    
    '''
    # SAVE FIT AS CSV
    
    # Create a DataFrame
    df = pd.DataFrame({
        'thickness': d_plot,
        'transmission': transmission_fit,
        'reflection': reflection_fit,
        'absorption':absorbance
    })
    
    # Save to CSV
    df.to_csv( filename+'_DpMeasurements.csv', index=False)
    '''
    
def main() -> None:

    """

    """
    path = askFilePath()

    parser = argparse.ArgumentParser()
    parser.add_argument("--includeZero", action="store_true")
    parser.add_argument("--title", default="", type=str)
    
    if os.path.isfile(path):
        try:
            assert path.endswith('.csv')

            #df = pd.read_csv(path, header=None)

            # read with header
            df = pd.read_csv(path)
            #df = pd.read_csv(path, header=None).dropna()
            #filename = os.path.splitext(os.path.basename(path))[0]
            if parser.parse_args().title == "":
                filename = os.path.splitext(os.path.basename(path))[0]
            else:
                filename = parser.parse_args().title

            
            analyze(df, filename, include_zero=parser.parse_args().includeZero)
            
        except AssertionError:
            print('Invalid path,must supply valid csv')


        
if __name__ == "__main__":
    main()






