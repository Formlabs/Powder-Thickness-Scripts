import pandas as pd
from scipy.stats import kstest
from scipy.stats import ks_2samp
from scipy.stats import norm
import numpy as np

# to open a file
import os
import tkinter as tk
from tkinter import filedialog


import argparse


def askFilePath():
    root = tk.Tk()
    root.withdraw()    
    file_path = filedialog.askopenfilename()
    #file_path = filedialog.askdirectory()
    return file_path

def analyze_ks(df, sample1=["Keyence PA12"], sample2=None, checkGaussian=False):
    # get all unique shim settings:
    settings = df["Iris's measurements"].unique()

    # create list to hold KS results
    ks_results = {}

    print(f"checkGaussian: {parser.parse_args().checkGaussian}")

    for setting in settings:
        sample1_thicknesses = df[df["Iris's measurements"]==setting][sample1]
        if sample2 is None:
            other_thicknesses = df[df["Iris's measurements"]==setting].drop(["Iris's measurements", *sample1], axis=1)
        else:
             other_thicknesses = df[df["Iris's measurements"]==setting][sample2]

        #ks_results.append(ks_2samp(PA12_thicknesses, other_thicknesses))
        if checkGaussian:
            ks_results[setting] = kstest(np.ravel(sample1_thicknesses.values[np.isfinite(sample1_thicknesses)]), lambda x: norm.cdf(x, loc=np.mean(np.ravel(sample1_thicknesses.values[np.isfinite(sample1_thicknesses)])), scale=np.std(np.ravel(sample1_thicknesses.values[np.isfinite(sample1_thicknesses)]), ddof=1)))
            print(f"Sample 1 mean: {np.mean(np.ravel(sample1_thicknesses.values[np.isfinite(sample1_thicknesses)]))}")
            print(f"Sample 1 standard deviation: {np.std(np.ravel(sample1_thicknesses.values[np.isfinite(sample1_thicknesses)]), ddof=1)}")
        else:
            ks_results[setting] = (ks_2samp(np.ravel(sample1_thicknesses[np.isfinite(sample1_thicknesses)]), np.ravel(other_thicknesses)[np.isfinite(np.ravel(other_thicknesses))]))

    return ks_results


path = askFilePath()

parser = argparse.ArgumentParser()
parser.add_argument("--sample1Name", nargs='*', default=["Keyence PA12"])
parser.add_argument("--sample2Name", nargs='*', default=None)
parser.add_argument("--checkGaussian", action="store_true")

if os.path.isfile(path):
        try:
            assert path.endswith('.csv')

            #df = pd.read_csv(path, header=None)

            # read with header
            df = pd.read_csv(path)
            results = analyze_ks(df, sample1=parser.parse_args().sample1Name, sample2=parser.parse_args().sample2Name, checkGaussian=parser.parse_args().checkGaussian)
            #print(results)
            for key in results.keys():
                 print(f"{key}, {results[key].pvalue}")
            
        except AssertionError:
            print('Invalid path,must supply valid csv')

