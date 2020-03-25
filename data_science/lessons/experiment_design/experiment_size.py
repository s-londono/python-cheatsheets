# EXPERIMENT SIZE

# We can use the knowledge of our desired practical significance boundary to plan out our experiment.
# By knowing how many observations we need in order to detect our desired effect to our desired level of reliability,
# we can see how long we would need to run our experiment and whether or not it is feasible.

# Let's use the example from the video, where we have a baseline click-through rate of 10% and want to see a
# manipulation increase this baseline to 12%. How many observations would we need in each group in order to detect
# this change with power 1−𝛽=.80 (i.e. detect the 2% absolute increase 80% of the time),
# at a Type I error rate of 𝛼=.05?

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# METHOD 1: TRIAL AND ERROR

# Every sample size will have a level of power associated with it; testing multiple sample sizes will gradually allow
# us to narrow down the minimum sample size required to obtain our desired power level. This isn't a particularly
# efficient method, but it can provide an intuition for how experiment sizing works.

# The power() function follows these steps:

# 1. Under the null hypothesis, we should have a critical value for which the Type I error rate is at
# our desired alpha level.

# 2. The power is the proportion of the distribution under the alternative hypothesis that is past that
# previously-obtained critical value.


def power(p_null, p_alt, n, alpha=.05, plot=True):
    """
    Compute the power of detecting the difference in two populations with
    different proportion parameters, given a desired alpha rate.

    Input parameters:
        p_null: base success rate under null hypothesis
        p_alt : desired success rate to be detected, must be larger than
                p_null
        n     : number of observations made in each group
        alpha : Type-I error rate
        plot  : boolean for whether or not a plot of distributions will be
                created

    Output value:
        power : Power to detect the desired difference, under the null.
    """

    # Compute the power
    se_null = np.sqrt((p_null * (1 - p_null) + p_null * (1 - p_null)) / n)
    null_dist = stats.norm(loc=0, scale=se_null)
    p_crit = null_dist.ppf(1 - alpha)

    se_alt = np.sqrt((p_null * (1 - p_null) + p_alt * (1 - p_alt)) / n)
    alt_dist = stats.norm(loc=p_alt - p_null, scale=se_alt)
    beta = alt_dist.cdf(p_crit)

    if plot:
        # Compute distribution heights
        low_bound = null_dist.ppf(.01)
        high_bound = alt_dist.ppf(.99)
        x = np.linspace(low_bound, high_bound, 201)
        y_null = null_dist.pdf(x)
        y_alt = alt_dist.pdf(x)

        # Plot the distributions
        plt.plot(x, y_null)
        plt.plot(x, y_alt)
        plt.vlines(p_crit, 0, np.amax([null_dist.pdf(p_crit), alt_dist.pdf(p_crit)]),
                   linestyles='--')
        plt.fill_between(x, y_null, 0, where=(x >= p_crit), alpha=.5)
        plt.fill_between(x, y_alt, 0, where=(x <= p_crit), alpha=.5)

        plt.legend(['null', 'alt'])
        plt.xlabel('difference')
        plt.ylabel('density')
        plt.show()

    # return power
    return 1 - beta


# METHOD 2: ANALYTIC SOLUTION

# Now that we've got some intuition for power by using trial and error, we can now approach a closed-form solution
# for computing a minimum experiment size. The key point to notice is that, for an 𝛼 and 𝛽 both < .5, the critical
# value for determining statistical significance will fall between our null click-through rate and our alternative,
# desired click-through rate. So, the difference between 𝑝0 and 𝑝1 can be subdivided into the distance from 𝑝0 to the
# critical value 𝑝∗ and the distance from 𝑝∗ to 𝑝1.

def experiment_size(p_null, p_alt, alpha=.05, beta=.20):
    """
    Compute the minimum number of samples needed to achieve a desired power
    level for a given effect size.

    Input parameters:
        p_null: base success rate under null hypothesis
        p_alt : desired success rate to be detected
        alpha : Type-I error rate
        beta  : Type-II error rate

    Output value:
        n : Number of samples required for each group to obtain desired power
    """

    # Get necessary z-scores and standard deviations (@ 1 obs per group)
    z_null = stats.norm.ppf(1 - alpha)
    z_alt = stats.norm.ppf(beta)
    sd_null = np.sqrt(p_null * (1 - p_null) + p_null * (1 - p_null))
    sd_alt = np.sqrt(p_null * (1 - p_null) + p_alt * (1 - p_alt))

    # Compute and return minimum sample size
    p_diff = p_alt - p_null
    n = ((z_null * sd_null - z_alt * sd_alt) / p_diff) ** 2
    return np.ceil(n)


print(experiment_size(.1, .12))

# NOTES ON INTERPRETATION

# The example explored above is a one-tailed test, with the alternative value greater than the null.
# The power computations performed in the first part will not work if the alternative proportion is greater than
# the null, e.g. detecting a proportion parameter of 0.88 against a null of 0.9. You might want to try to rewrite
# the code to handle that case! The same issue should not show up for the second approach, where we directly
# compute the sample size.

# If you find that you need to do a two-tailed test, you should pay attention to two main things. First of all,
# the "alpha" parameter needs to account for the fact that the rejection region is divided into two areas.
# Secondly, you should perform the computation based on the worst-case scenario, the alternative case with
# the highest variability. Since, for the binomial, variance is highest when 𝑝=.5, decreasing as 𝑝 approaches 0 or 1,
# you should choose the alternative value that is closest to .5 as your reference when
# computing the necessary sample size.

# Note as well that the above methods only perform sizing for statistical significance, and do not take into account
# practical significance. One thing to realize is that if the true size of the experimental effect is the same as the
# desired practical significance level, then it's a coin flip whether the mean will be above or below the practical
# significance bound. This also doesn't even consider how a confidence interval might interact with that bound.
# In a way, experiment sizing is a way of checking on whether or not you'll be able to get what you want from
# running an experiment, rather than checking if you'll get what you need.

# ALTERNATIVE APPROACHES

# There are also tools and Python packages that can also help with sample sizing decisions, so you don't need to solve
# for every case on your own. The sample size calculator here is applicable for proportions, and provides the same
# results as the methods explored above. (Note that the calculator assumes a two-tailed test, however.) Python
# package "statsmodels" has a number of functions in its power module that perform power and sample size calculations.
# Unlike previously shown methods, differences between null and alternative are parameterized as an effect size
# (standardized difference between group means divided by the standard deviation). Thus, we can use these functions
# for more than just tests of proportions. If we want to do the same tests as before, the proportion_effectsize
# function computes Cohen's h as a measure of effect size. As a result, the output of the statsmodel functions will
# be different from the result expected above. This shouldn't be a major concern since in most cases, you're not
# going to be stopping based on an exact number of observations. You'll just use the value to
# make general design decisions.

# Example of using statsmodels for sample size calculation.
# Leave out the "nobs" parameter to solve for it
NormalIndPower().solve_power(effect_size=proportion_effectsize(.12, .1), alpha=.05, power=0.8, alternative='larger')