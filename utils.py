import pandas as pd
import scipy.stats as stat
import math
import random
from distutils.log import warn
import numpy as np


def remove_outliers(df: pd.DataFrame, data_col: str) -> pd.DataFrame:
    data = df[data_col]

    # Calculate the quantiles of the column
    q1, q3 = data.quantile(.25), data.quantile(.75)
    iqr = q3 - q1

    # Set the lower and upper bounds for the column
    min = q1 - (1.5 * iqr)
    max = q3 + (1.5 * iqr)

    # Select rows that have a value in the column within the bounds
    return df[(df[data_col] > min) & (df[data_col] < max)]


# determines whether or not a sample follows a normal distribution
# https://stats.stackexchange.com/questions/350443/how-do-i-get-the-p-value-of-ad-test-using-the-results-of-scipy-stats-anderson
def anderson(data) -> float:
    ad, _, _ = stat.anderson(data)

    ad = ad * (1 + (.75/50) + 2.25/(50**2))

    if ad >= .6:
        p = math.exp(1.2937 - 5.709*ad - .0186*(ad**2))
    elif ad >= .34:
        p = math.exp(.9177 - 4.279*ad - 1.38*(ad**2))
    elif ad > .2:
        p = 1 - math.exp(-8.318 + 42.796*ad - 59.938*(ad**2))
    else:
        p = 1 - math.exp(-13.436 + 101.14*ad - 223.73*(ad**2))

    return p


# performs random sampling to compare two samples that are not normally distributed
#   H0: df1 and df2 have the same distribution, the difference in samples is due to chance
#   H1: df1's average is lower than df2's
def random_sampling(df1: pd.DataFrame, df2: pd.DataFrame, col: str, reps: int, log = True) -> tuple[float, list[float]]:
    
    df1_len, df2_len = len(df1), len(df2)

    if df1_len != df2_len and log:
        warn(f"The number of samples is not the same!\n\tdf1 : {df1_len}\n\tdf2 : {df2_len}")
    
    df = pd.concat([df1, df2])
    df.reset_index()
    df_len = len(df)

    max_combs = math.factorial(df_len) / (math.factorial(df1_len) * math.factorial(df_len - df1_len))
    if max_combs < reps and log:
        warn(f"The number of possible combinations is {max_combs}, and you are using {reps} repetitions!")

    list_idx = [*range(df_len)]
    
    mean_diffs = []
    for _ in range(reps):
        samples = random.sample(list_idx, df_len)
        sample1_idx = samples[:df1_len]
        sample2_idx = samples[df1_len:]

        sample1 = df.iloc[sample1_idx]
        sample2 = df.iloc[sample2_idx]

        mean_diff = sample1[col].mean() - sample2[col].mean()
        mean_diffs.append(mean_diff)

    org_mean_diff = df1[col].mean() - df2[col].mean()
    # pvalue = np.mean(abs(mean_diffs) >= abs(org_mean_diff))
    pvalue = np.mean([abs(x) >= abs(org_mean_diff) for x in mean_diffs])

    # pvalue = np.count_nonzero(pd.Series(mean_diffs) <= org_mean_diff) / reps

    return pvalue, mean_diffs, org_mean_diff