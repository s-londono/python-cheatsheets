import math
import matplotlib.pyplot as plt
from .GeneralDistribution import Distribution


class Binomial(Distribution):
    """ Binomial distribution class for calculating and
    visualizing a Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring

    """
    def __init__(self, p=0.5, n=10):
        self.p = p
        self.n = n
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())

    def calculate_mean(self):
        """Function to calculate the mean from p and n

        Args:
            None

        Returns:
            float: mean of the data set

        """
        self.mean = self.p * self.n
        return self.mean

    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set

        """
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        return self.stdev

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.

        Args:
            file_name: name of the file to read the data from. Should contains 0s and 1s only

        Returns:
            float: the p value
            float: the n value

        """
        # Compute p, probability of success and n, number of variables in the object
        self.n = len(self.data)
        self.p = sum(self.data) / self.n

        # Update mean and standard deviation
        self.calculate_mean()
        self.calculate_stdev()

        return self.p, self.n

    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """
        plt.hist(self.data)
        plt.title("Histogram of Data (Binomial)")
        plt.xlabel("Levels")
        plt.ylabel("Number of observations")

    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.

        Args:
            k (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """
        n = self.n
        p = self.p

        multiplier = math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

        return multiplier * (math.pow(p, k) * math.pow((1 - p), n - k))

    # TODO: Use a bar chart to plot the probability density function from
    # k = 0 to k = n

    #   Hint: You'll need to use the pdf() method defined above to calculate the
    #   density function for every value of k.

    #   Be sure to label the bar chart with a title, x label and y label

    #   This method should also return the x and y values used to make the chart
    #   The x and y values should be stored in separate lists

    # write a method to output the sum of two binomial distributions. Assume both distributions have the same p value.
    def plot_histogram_pdf(self):
        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """
        x = []
        y = []

        # calculate the x values to visualize
        for k in range(0, self.n):
            x.append(k)
            y.append(self.pdf(k))

        # make the plots
        fig, axes = plt.subplots(2, sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Binomial Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y

    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution

        """
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise error

        return Binomial(self.p, (self.n + other.n))

    def __repr__(self):
        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Binomial object

        """
        return f"mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n}"

