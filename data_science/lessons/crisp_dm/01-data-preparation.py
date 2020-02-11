# Gathering & Wrangling
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read dataset in DataFrame df
df = pd.read_csv('data_science/resources/survey_results_public.csv')
df.head()

# Read dataset schema in a DataFrame df2
df2 = pd.read_csv('data_science/resources/survey_results_schema.csv')

# Show the questions that where asked when filling in column CousinEducation
list(df2[df2.Column == 'CousinEducation']['Question'])

# The CousinEducation may contain severan semi-colon-separated values in a cell...
study = df['CousinEducation'].value_counts().reset_index()
study.head()

# Rename the columns of the study DataFrame
study.rename(columns={'index': 'method', 'CousinEducation': 'count'}, inplace=True)
study.head()

# Extract all possible individual answers to the CousinEducation question
possible_vals = set()
df['CousinEducation'].apply(
    lambda ans: [possible_vals.add(v.strip()) for v in ans.split(';')] if type(ans) == str else None)


# Create a function to count how many times each value appears
def total_count(src_df, col1, col2, look_for):
    """
    INPUT:
    src_df - The Pandas DataFrame to search
    col1 - The column name to look through
    col2 - The column you want to count values from
    look_for - A list of strings you want to search for in each row of df[col]

    OUTPUT:
    new_df - A DataFrame of each look_for with the count of how often it shows up
    """
    from collections import defaultdict
    new_df = defaultdict(int)

    for val in look_for:
        for idx in range(src_df.shape[0]):
            if val in src_df[col1][idx]:
                new_df[val] += int(src_df[col2][idx])

    # Create a DataFrame from a dictionary, by taking entries as rows, with the keys as row indexes
    new_df = pd.DataFrame(pd.Series(new_df)).reset_index()
    new_df.columns = [col1, col2]
    new_df.sort_values('count', ascending=False, inplace=True)

    return new_df


study_df = total_count(study, 'method', 'count', possible_vals)

# Add a column with the percent of students that choose each option
study_df['perc'] = study_df['count'] / np.sum(study_df['count'])


def clean_and_plot(src_df, title='Method of Educating Suggested', plot=True):
    """
    INPUT
        df - a dataframe holding the CousinEducation column
        title - string the title of your plot
        axis - axis object
        plot - bool providing whether or not you want a plot back

    OUTPUT
        study_df - a dataframe with the count of how many individuals
        Displays a plot of pretty things related to the CousinEducation column. Using:
        https://pandas.pydata.org/pandas-docs/stable/style.html
    """
    cln_study = src_df['CousinEducation'].value_counts().reset_index()
    cln_study.rename(columns={'index': 'method', 'CousinEducation': 'count'}, inplace=True)
    cln_study_df = total_count(cln_study, 'method', 'count', possible_vals)

    cln_study_df.set_index('method', inplace=True)
    if plot:
        (cln_study_df / cln_study_df.sum()).plot(kind='bar', legend=None)
        plt.title(title)
        plt.show()
    props_study_df = cln_study_df / cln_study_df.sum()
    return props_study_df


ed_1 = df[df['HigherEd'] == 1]  # Subset df to only those with HigherEd of 1
ed_0 = df[df['HigherEd'] == 0]  # Subset df to only those with HigherEd of 0

# Check your subset is correct - you should get a plot that was created using pandas styling
# which you can learn more about here: https://pandas.pydata.org/pandas-docs/stable/style.html
ed_1_perc = clean_and_plot(ed_1, 'Higher Formal Education', plot=False)
ed_0_perc = clean_and_plot(ed_0, 'Max of Bachelors Higher Ed', plot=False)

comp_df = pd.merge(ed_1_perc, ed_0_perc, left_index=True, right_index=True)
comp_df.columns = ['ed_1_perc', 'ed_0_perc']
comp_df['Diff_HigherEd_Vals'] = comp_df['ed_1_perc'] - comp_df['ed_0_perc']
comp_df.style.bar(subset=['Diff_HigherEd_Vals'], align='mid', color=['#d65f5f', '#5fba7d'])


# BOOTCAMPS

not_bootc_df = df[df['TimeAfterBootcamp'].isnull() == True]
bootc_df = df[df['TimeAfterBootcamp'].isnull() == False]

# Are bootcamps helping people under-represented in the technical community?
# Compute mean participation per gender ("breakdown") in bootcamps
bootc_df['Gender'].value_counts() / (bootc_df.shape[0] - sum(bootc_df['Gender'].isnull()))
# Versus mean non-participation per gender in bootcamps
not_bootc_df['Gender'].value_counts() / (not_bootc_df.shape[0] - sum(not_bootc_df['Gender'].isnull()))

# Breakdown by Formal Education
bootc_df['FormalEducation'].value_counts() / (bootc_df.shape[0] - sum(bootc_df['FormalEducation'].isnull()))
not_bootc_df['FormalEducation'].value_counts() / (not_bootc_df.shape[0] - sum(not_bootc_df['FormalEducation'].isnull()))

# Breakdown by time that takes after the bootcamp to get a job. Here we see that most participants already had a job
bootc_df['TimeAfterBootcamp'].value_counts() / bootc_df.shape[0]

# Breakdown by salary, using a histogram
bootc_df['Salary'].hist(bins=20)





