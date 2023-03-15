# "On Security and Energy Efficiency in Android Smartphones"
This repository contains the data and statistical analysis of "On Security and Energy Efficiency in Android Smartphones".

### Extraction
The `extractor.ipynb` notebook extracts the execution time and energy consumption information produced by EBServer into
a `.csv` file. One must specify the `app_id`, which can be found in the outputs of EBServer, and the `data_dir`, 
which is the directory that contains the output files. To specify the output file, simply change the filename in the last
cell. The execution time is presented in milliseconds and the energy in joules.

### Statistical Analysis
The `stats.ipynb` notebook reads the extracted data in `.csv` format and performs a series of statistical tests:
 - Normality tests: Shapiro-Wilks, D'Agostino's K², Anderson-Darling
 - Homogeinety of Variance test: Levene
 - Statistical Significance: ANOVA, A/B testing (random sampling)

Furthermore, it calculates the average percentual difference between the average execution time or energy consumption, 
depending on the metric being studied, and produces charts to aid with the analysis.
