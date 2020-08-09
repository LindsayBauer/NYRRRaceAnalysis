from os import path
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd


annual_files = [str(year) + ".json" for year in range(2010,2020)]

NUM_AGE_BRACKETS = 8

def get_race_years():
    years = []
    for i in range(len(annual_files)):
        years.append(annual_files[i][:4])
    return years


def get_runners_data(year):
    """Return data on every runner from a given years race"""
    getData = pd.read_json(path.join(Path.cwd(), 'Data', year),
                               orient='columns')['response']
    return pd.DataFrame.from_records(getData['items'])


def get_age_distribution():
    """Return number of runners in each age bracket by year"""
    age_distribution = np.zeros(shape=(len(annual_files), NUM_AGE_BRACKETS))
    
    for year in annual_files:
        df = get_runners_data(year)
        for i in range(10, 90, 10):
            age_count = df["age"].where(
                (df["age"].values >= i) & (df["age"].values < i + 10)).count()
            age_distribution[annual_files.index(
                year)][int((i / 10) - 1)] = age_count
    return age_distribution


def plot_annual_age_distribution():
    age_distribution = get_age_distribution()
    years = get_race_years()

    color = cm.viridis(np.linspace(.1, .9, NUM_AGE_BRACKETS))
    df_ages_by_year = pd.DataFrame(age_distribution, index=years)
    df_ages_by_year.plot.bar(legend = True, figsize = (
        18, 6), color = color, rot = 0)
    plt.style.use('seaborn-darkgrid')
    plt.legend(["10-19", "20-29", "30-39", "40-49", "50-59",
                "60-69", "70-79", "80-89"], bbox_to_anchor = (1, 1))
    plt.title("Annual Age Distribution", fontsize = 20)
    plt.xlabel("Race Year", fontsize = 15)
    plt.ylabel("Number of Runners", fontsize = 15)
    plt.show()

plot_annual_age_distribution()


def get_largest_bracket_indices(num_brackets, age_distributions):
    bracket_sizes_across_years = np.sum(age_distributions, axis = 0)
    return np.sort(np.argpartition(bracket_sizes_across_years, -num_brackets)[-num_brackets:])


def plot_largest_age_brackets(num_brackets: int = 3):
    if (num_brackets > NUM_AGE_BRACKETS or num_brackets < 1):
        num_brackets = 3

    age_distributions = get_age_distribution()
    indexed_age_brackets = {"0":"10-20", "1":"20-29", "2":"30-39", "3":"40-49", "4":"50-59",
                "5":"60-69", "6":"70-79", "7":"80-89"}
    indices_of_largest_brackets = get_largest_bracket_indices(num_brackets, age_distributions)
    
    largest_age_brackets = [indexed_age_brackets[str(index)] for index in indices_of_largest_brackets]
    num_runners = [age_distributions[:,index] for index in indices_of_largest_brackets]

    years = get_race_years()

    for i in range(num_brackets):
        plt.plot(years, num_runners[i], marker='o', markersize = 7, color = cm.viridis(.1 + indices_of_largest_brackets[i]*.1))
    plt.gcf().set_size_inches((10, 8)) 
    plt.style.use('seaborn-darkgrid')
    plt.legend(largest_age_brackets, bbox_to_anchor=(1, 1))
    plt.title("Participation in " + str(num_brackets) + " Largest Age Brackets Over " + str(len(years)) + " Years", fontsize = 20)
    plt.xlabel("Race Year", fontsize = 15)
    plt.ylabel("Number of Runners in Age Bracket", fontsize = 15)
    plt.show()

plot_largest_age_brackets(9)
