from os import path
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd

annual_files = [str(year) + ".json" for year in range(2010,2020)]

def get_runners_data(year):
    getData = pd.read_json(path.join(Path.cwd(), 'Data', year),
                               orient='columns')['response']
    return pd.DataFrame.from_records(getData['items'])

def get_avg_races_run():
    """Return dictionary. Keys are finishing place brackets and values are the average number of
    races run prior by runners that placed in that bracket"""
    prior_races_by_bracket = {}
    for year in annual_files:
        df = get_runners_data(year)

        bracket_size = 1000
        for i in range(0, df["overallPlace"].max() + 1, bracket_size):
            average_races = df["racesCount"].where(
                (df["overallPlace"].values > i) & (df["overallPlace"].values <= i + bracket_size)).mean()
            try:
                prior_races_by_bracket[i + bracket_size].add(average_races)
            except KeyError:
                prior_races_by_bracket[i + bracket_size] = {average_races}

    for key in prior_races_by_bracket:
        prior_races_by_bracket[key] = round(sum(prior_races_by_bracket[key]) / 
            float(len(prior_races_by_bracket[key])), 2)
    return prior_races_by_bracket

get_avg_races_run()
    

def plot_avg_races_run():
    prior_races_by_bracket = get_avg_races_run()
    brackets, avg_num_races = zip(*prior_races_by_bracket.items())
    data_to_plot = [{brackets[i]: avg_num_races[i]} for i in range(len(brackets))]

    df_num_races = pd.DataFrame(data_to_plot, index = brackets)
    color = cm.inferno_r(np.linspace(.4, .8, len(brackets)))
    plt.style.use('seaborn-darkgrid')
    df_num_races.plot.bar(stacked = True, color = color, rot = 0, figsize = (12,4), legend = False)
    plt.title("Average Number of Races Run per Placement Bracket", fontsize = 20)
    plt.xlabel("Finishing Bracket in Race", fontsize = 15)
    plt.ylabel("Average Number of Races Run Prior", fontsize = 15)
    plt.show()

plot_avg_races_run() 