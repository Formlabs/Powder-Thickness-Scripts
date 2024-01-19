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
* There *must* be two rows in the file whose first entries are `"Adjusted, direct"`. These correspond to the improved powder thickness values from the Keyence. Immediately above each must be a row with the corresponding originally-estimated thicknesses. Immediately below the `"Adjusted, direct"` row must be two rows of raw measured data.