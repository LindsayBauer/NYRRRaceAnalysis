from os import path
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd

annual_files = [str(year) + ".json" for year in range(2010,2020)]

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

def get_num_countries():
    """Return number of countries represented by year"""
    num_countries = np.zeros(shape=(len(annual_files), 1))
    
    for year in annual_files:
        df = get_runners_data(year)
        country_count = df['countryCode'].value_counts()
        num_countries[annual_files.index(
                year)] = len(country_count.index)
    return num_countries


def plot_num_countries():
    num_countries = get_num_countries()
    years = get_race_years()

    plt.plot(years, num_countries, marker='o', markersize = 7, color = cm.viridis(.2))
    plt.gcf().set_size_inches((10, 8)) 
    plt.style.use('seaborn-darkgrid')
    plt.title("Number of Countries Represented by Year", fontsize = 20, fontweight = 10)
    plt.xlabel("Race Year", fontsize = 15)
    plt.ylabel("Number of Countries", fontsize = 15)
    plt.show()

plot_num_countries()