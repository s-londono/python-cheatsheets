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


def simulate_random_assignment(df, num_simulations=200000):
    """
    Simulates random assignment to experimental group and compares it to the assignment in the dataset
    :param df: Dataset
    :param num_simulations: Number of simulations to run
    :return: P-value computed from the simulations and the real proportion of experimental observations
    """
    total_observations = data.shape[0]
    total_sim_experimental_group = 0

    diff_exp_group_to_hipothesis_mean = np.abs(data["condition"].mean() - 0.5)

    print(f"Difference of experimental group proportion to 0.5: {diff_exp_group_to_hipothesis_mean}")

    # Create Discrete Uniform distribution with values 0 and 1
    rv = stats.randint(0, 2)

    print(f"Running {num_simulations} simulations. Observations: {total_observations}")

    for i in range(0, num_simulations):
        # Randomly generate observations from distribution rv, which simulate users that saw the new page
        diff_btw_mean_experimental_obs = np.abs(rv.rvs(size=total_observations).mean() - 0.5)

        if diff_btw_mean_experimental_obs >= diff_exp_group_to_hipothesis_mean:
            total_sim_experimental_group += 1

    sim_p_value = total_sim_experimental_group / num_simulations

    print(f"Simulation p-value: {sim_p_value}")

    return sim_p_value

# Simulation: FAST alternative way

# Get number of trials and number of 'successes'
n_obs = data.shape[0]
n_control = data.groupby('condition').size()[0]

# Simulate outcomes under null hypothesis, compare to observed outcome
p = 0.5
n_trials = 200_000
samples = np.random.binomial(n_obs, p, n_trials)

print(np.logical_or(samples <= n_control, samples >= (n_obs - n_control)).mean())

# 2. Analytic approach:
# Use either the exact Binomial distribution to compute a p-value for the test or the Normal distribution approximation.
# Recall that this is possible thanks to our large sample size and the Central Limit Theorem.
# To get a precise p-value, you should also perform a continuity correction, either adding or subtracting 0.5 to
# the total count before computing the area underneath the curve. (e.g. If we had 415/850 assigned to the control group,
# then the normal approximation would take the area to the left of  (415+0.5)/850 = 0.489  and to the right of
# (435−0.5)/850 = 0.511)

# Get number of trials and number of 'successes'
n_obs = data.shape[0]
n_control = data.groupby('condition').size()[0]

# Compute a z-score and p-value. Should be a Binomial distribution with p = 0.5 and n = n_obs
p = 0.5
mean = p * n_obs
sd = np.sqrt(n_obs * p * (1-p))

# As to the CLT, the sum of 'condition' records is Normally distributed. Compute the Z-Score
z = ((n_control + 0.5) - mean) / sd

print(z)
print(2 * stats.norm.cdf(z))

# 2. CHECK THE EVALUATION METRIC

# Move on to performing a hypothesis test on the evaluation metric: the click-through rate. In this case, we want to
# see that the experimental group has a significantly larger click-through rate than the control group, a one-tailed
# test.

# First, compute the difference in click rates in the experimental vs. control groups
p_click = data.groupby('condition').mean()['click']
print(f"Click rate. Experimental vs. control groups: {p_click[1] - p_click[0]}")

# 1. Simulation-based approach:
# You'll need the overall click-through rate as the common proportion to draw simulated values from for each group.
# You may also want to perform more simulations since there's higher variance for this test.

# Get number of trials and overall 'success' rate under null
n_control = data.groupby('condition').size()[0]
n_exper = data.groupby('condition').size()[1]
p_null = data['click'].mean()

# Simulate outcomes under null, compare to observed outcome
n_trials = 200_000
ctrl_clicks = np.random.binomial(n_control, p_null, n_trials)
exp_clicks = np.random.binomial(n_exper, p_null, n_trials)
samples = exp_clicks / n_exper - ctrl_clicks / n_control
print((samples >= (p_click[1] - p_click[0])).mean())

# 2. Analytic approach:
# There are a few analytic approaches possible here, but you'll probably make use of the normal approximation again
# in these cases. In addition to the pooled click-through rate, you'll need a pooled standard deviation in order to
# compute a z-score. While there is a continuity correction possible in this case as well, it's much more
# conservative than the p-value that a simulation will usually imply. Computing the z-score and resulting p-value
# without a continuity correction should be closer to the simulation's outcomes, though slightly more optimistic
# about there being a statistical difference between groups

# Get number of trials and overall 'success' rate under null hypothesis
n_control = data.groupby('condition').size()[0]
n_exper = data.groupby('condition').size()[1]
p_null = data['click'].mean()

# Compute standard error, z-score, and p-value. What distribution is this?
se_p = np.sqrt(p_null * (1 - p_null) * (1 / n_control + 1 / n_exper))
z = (p_click[1] - p_click[0]) / se_p
p_value = 1 - stats.norm.cdf(z)

print(f"Std. error. P-value: {p_value}")

