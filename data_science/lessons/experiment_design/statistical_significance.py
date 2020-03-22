# Two groups:
#   1. Got modified page
#   2. Got original page
# Metrics:
#   1. Which version of the page did the user receive?
#   2. Did the user access the download page?
# Goal:
#   To perform a statistical test on both recorded metrics to see if there is a statistical difference
#   between the two groups
import os
from time import time
import numpy as np
import pandas as pd
import scipy.stats as stats
from statsmodels.stats import proportion as proptests
import matplotlib.pyplot as plt

if not os.getcwd().endswith("experiment_design"):
    os.chdir("data_science/lessons/experiment_design")

# The condition column is 0: control group, 1: experimental group
# The click column is 0: did not click, 1: did click
data = pd.read_csv('data/statistical_significance_data.csv')
data.head(10)

# 1. CHECK THE INVARIANT METRIC

# Check that the number of visitors assigned to each group is similar. It's important to check the invariant metrics
# as a prerequisite so that our inferences on the evaluation metrics are founded on solid ground. If we find that the
# two groups are imbalanced on the invariant metric, then this will require us to look carefully at how the visitors
# were split so that any sources of bias are accounted for. It's possible that a statistically significant difference
# in an invariant metric will require us to revise random assignment procedures and re-do data collection

# In this case, we want to do a two-sided hypothesis test on the proportion of visitors assigned to one of the
# conditions. Choosing the control or the experimental condition doesn't matter: you'll get the same result either way
# There are two avenues:

# 1. Simulation-based approach:
# Simulate the number of visitors that would be assigned to each group for the number of total observations, assuming
# that we have an expected 50/50 split. Do this many times (200000 repetitions should provide a good speed-variability
# balance in this case) and then see in how many simulated cases we get as extreme or more extreme a deviation from
# 50/50 that we actually observed.
# The proportion of flagged simulation outcomes gives us a p-value on which to assess our observed proportion.
# We hope to see a larger p-value, insufficient evidence to reject the null hypothesis

num_simulations = 200000
total_obs = data.shape[0]

diff_exp_group_to_mean = np.abs(data["condition"].mean() - 0.5)
print(f"Difference of experimental group proportion to 0.5: {diff_exp_group_to_mean}")

# Uniform distribution, discrete values 0 and 1
rv = stats.randint(0, 2)
total_sim_egroup = 0

start_time = time()

print(f"Running {num_simulations} simulations. Observations: {total_obs}")

for i in range(0, num_simulations):
    sim_diff_exp_group_to_mean = np.abs(rv.rvs(size=total_obs).mean() - 0.5)

    if sim_diff_exp_group_to_mean >= diff_exp_group_to_mean:
        total_sim_egroup += 1

sim_p_value = total_sim_egroup / num_simulations

print(f"Simulation p-value: {sim_p_value}")

print(f"Running time: {time() - start_time}")

# 2. Analytic approach:
# Use either the exact Binomial distribution to compute a p-value for the test or the Normal distribution approximation.
# Recall that this is possible thanks to our large sample size and the Central Limit Theorem.
# To get a precise p-value, you should also perform a continuity correction, either adding or subtracting 0.5 to
# the total count before computing the area underneath the curve. (e.g. If we had 415/850 assigned to the control group,
# then the normal approximation would take the area to the left of  (415+0.5)/850 = 0.489  and to the right of
# (435−0.5)/850 = 0.511)

