import pandas as pd
#from scipy.stats import kstest
from scipy.stats import ks_2samp
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

def analyze_ks(df, sample1="Keyence PA12"):
    # get all unique shim settings:
    settings = df["Iris's measurements"].unique()

    # create list to hold KS results
    ks_results = {}

    for setting in settings:
        sample1_thicknesses = df[df["Iris's measurements"]==setting][sample1]
        other_thicknesses = df[df["Iris's measurements"]==setting].drop(["Iris's measurements", sample1], axis=1)

        #ks_results.append(ks_2samp(PA12_thicknesses, other_thicknesses))
        ks_results[setting] = (ks_2samp(sample1_thicknesses[np.isfinite(sample1_thicknesses)], np.ravel(other_thicknesses)[np.isfinite(np.ravel(other_thicknesses))]))

    return ks_results


path = askFilePath()

parser = argparse.ArgumentParser()
parser.add_argument("--sample1Name", default="Keyence PA12", type=str)

if os.path.isfile(path):
        try:
            assert path.endswith('.csv')

            #df = pd.read_csv(path, header=None)

            # read with header
            df = pd.read_csv(path)
            results = analyze_ks(df, sample1=parser.parse_args().sample1Name)
            #print(results)
            for key in results.keys():
                 print(f"{key}, {results[key].pvalue}")
            
        except AssertionError:
            print('Invalid path,must supply valid csv')

