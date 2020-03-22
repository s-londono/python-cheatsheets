# Sources:
#   https://docs.scipy.org/doc/scipy/reference/stats.html

import scipy.stats as stats

# RANDOM DISTRIBUTIONS

# Binomial distribution
n = 100
p = 0.3

# Create instance
rb = stats.binom(n, p)

# Generate random numbers
rb.rvs(size=10)
rb.rvs(size=(5, 10))

# Compute Moments (m: mean, v: variance, s: skey, k: kurtosis)
rb.mean()
rb.var()
rb.std()

mean, var, skew, kurt = rb.stats(moments='mvsk')
means, vrs, skews, kurts = stats.binom.stats(n, p, moments='mvsk')

# Probability Mass Function
k = 12
rb.pmf(k)
stats.binom.pmf(k, n, p)

# Cumulative Distribution Function
rb.cdf(k)
stats.binom.cdf(k, n, p)
