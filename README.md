# Powder Optical Penetration Experiments--Analysis Scripts
This is a collection of analysis scripts to help out with the laser penetration experiments. All the files take different kinds of inputs and do slightly different things, as documented below. However, all have the same requirements, so these are detailed first.

## Requirements
* Seaborn
* Matplotlib
* Numpy
* Pandas
* Tkinter
* Scipy

## Scripts

### `penetrationDepth_analysis_unbound_10um.py`
Generates a plot of transmission vs thickness and fits a an exponential. Calculates penetration depth based on the fitted function. Upon execution, the user is prompted to select a file. The selected file must have a `.csv` extension, and must be a comma-separated file with data similar to the following:
```csv
Micrometer,Thickness,Transmitted,Relative_Transmission
0,0,41.7,1.000
100,33.3,16.7,0.400
150,80,4.4,0.106
200,126.7,1.1,0.026
250,173.4,0.3,0.007
300,220.1,0.3,0.007
```

It is important that there are columns with titles are `Thickness` and `Relative_Transmission`, which respectively contain the estimated thickness in $\mu m$ and relative transmission in the range of (0, 1) where 1 corresponds to an empty sample holder. It is important that the first row of data in the file (the row immediately after the labels) corresponds to the zero-point (the zero-thickness sample with a relative transmission of 1). By default, this zero-point is ignored for both plotting and fitting, but this can be toggled with command-line arguments.
#### Arguments
`--includeZero`: if set, makes the script include the zero-point in both the plot and the fit. If not set, then the zero-point will be ignored.

### `penetrationDepth_analysis_unbound.py`
Generates a plot of transmission vs thickness and fits a an exponential.
However, this file is designed to work with the format used originally for the 1um laser measurements.
Calculates penetration depth based on the fitted function. Upon execution, the user is prompted to select a file. The selected file must have a `.csv` extension, and must be a comma-separated file with data similar to the following:

```csv
Reflection,0.8A,,,,,,,,,,,,
base,0.00,115.00,170.00,220.00,275.00,335.00,440,,,,,,
"Adjusted, direct",0.00,40.50,74.40,127.75,187.00,241.50,333.71,,,,,,
1.42,0.037,0.103,0.150,0.160,0.165,0.166,0.166,,,,,,
,,0.107,0.142,0.161,0.168,0.166,0.166,,,,,,
,,,,,,,,,,,,,
Transmission,1A,,,,,,,,,,,,
base,0.00,115.00,170.00,220.00,275.00,335.00,440,,,,,,
"Adjusted, direct",0.00,40.50,74.40,127.75,187.00,241.50,333.71,,,40.5,74.4,127.75,187
505.00,501.00,234.00,63.90,19.20,6.70,1.60,0.25,,,,,,
,,223.00,63.40,18.20,6.20,1.50,0.24,,,,,,
```

What's important with this file is the following:
* There *must* be two rows in the file whose first entries are `"Adjusted, direct"`. These correspond to the improved powder thickness values from the Keyence. 
* Immediately above each must be a row with the corresponding originally-estimated thicknesses. 
* Immediately below the `"Adjusted, direct"` row must be two rows of raw measured data.
* The fist instance of this pattern must correspond to reflection measurements, the second must correspond to transmission measurements.

### `penetrationDepth_montecarlo_1um.py`
Performs Monte Carlo analysis of the effect of thickness uncertainty on penetration depth. That is, given a standard deviation for each thickness, gets a bunch of sets of simulated thickness measurements and fits associates given transmittance values with them. Fits an exponential to these data points and calculates penetration depth with the same technique that is used by the aforementioned scripts. Then, reports on the distribution of these different penetration depths: draws a histogram and reports mean penetration depth, standard deviation, and KS fits to various distributions.

The selected CSV should look similar to the following:

```csv
Thickness setpoint,Mean Keyence Thickness,Keyence Thickness Standard Deviation,Transmission 1,Transmission 2,Baseline
shim_100,38.880000,6.957781,297.00000,303.00000,501.00000
shim_100 + shim_50,79.000000,8.451543,166.50000,172.00000,501.00000
shim_210,125.400000,12.720936,92.80000,87.00000,501.00000
shim_210 + shim_50,183.220000,12.142670,44.90000,45.30000,501.00000
shim_210 + shim_100,239.820000,10.087796,22.30000,25.40000,501.00000
shim_210 + shim_210,335.600000,10.265368,8.90000,9.80000,501.00000
```

note the first newline is after the word `Baseline`; I can't figure out how to disable text wrapping.

The important thing is the columns starting with `Mean Keyence Thickness`, `Keyence Thickness Standard Deviation`, `Transmission 1`, `Transmission 2`, and `Baseline`. The first row must contain exactly these names.

### `ks_thickness_tester.py`
Performs a Kolmogorov-Smirnov test to see whether a set of given materials' thicknesses seem to come from the same population as a set of other materials' thicknesses.
Asks the user for a CSV file, which must look like the following:
```csv
Iris's measurements,Keyence PA12,Keyence Raw,Keyence blend 1,Keyence blend 4
115.00,,44.00,45.00,37.00
170.00,,82.00,89.00,89.00
220.00,,135.00,142.00,121.00
275.00,,173.00,190.00,161.00
335.00,,238.00,239.00,229.00
440,,338,347,335
115.00,23,29,43,
170.00,68,95,70,
220.00,105,120,118,
275.00,177,175,172,
335.00,238,232,,
440,319,346,329,
``` 

The important thing is that one column is titled `Iris's measurements`, and this is just the shim settings so the program knows what to compare with what. The other requirement is that there should be columns with titles that match the `--sample1Name` argument, which defaults to `Keyence PA12` but can be a list of material names. Also, one of the two following requirements must be satisfied:
either each of the names specified in `--sample2Name` should match a column name in the CSV, or (if `--sample2Name` is not given) each of the columns except for `Iris's measurements` should have a material and associated thicknesses. If there are any extraneous columns, they will mess everything up.

#### Usage
```
python ks_thickness_tester.py --sample1Name "Keyence PA12" "Keyence Raw" --sample2Name "Keyence blend 1" "Keyence blend 4"
```

This creates two samples that will be fed into the KS test: one is composed of the PA12 and raw nylon, the other is composed of blend 1 and blend 4. The two samples are compared against one another via the aforementioned KS test. If `--sample2Name` were omitted, all the remaining materials would be put into sample 2, which in this case would have exactly the same behaviour as the example usage given above (because the remaining materials are blend 1 and blend 4, which we initially put explicitly into sample 2).

