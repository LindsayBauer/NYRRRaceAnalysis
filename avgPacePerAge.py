from os import path
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd

annual_files = [str(year) + ".json" for year in range(2010,2020)]

def pace_string_to_seconds(time):
    """Convert a "minutes:seconds" string to seconds"""
    m, s = [int(i) for i in time.split(':')]
    return (60 * m + s)


def get_runners_data(year):
    getData = pd.read_json(path.join(Path.cwd(), 'Data', year),
                               orient='columns')['response']
    return pd.DataFrame.from_records(getData['items'])


def get_sum_of_paces_by_age():
    """Return sum of pace times in seconds for all runners of same age"""
    sum_of_paces_by_age = np.zeros(shape=(100,2))
    
    for year in annual_files:
        df = get_runners_data(year)    
        for i in range(df["age"].min(), df["age"].max()+1):
            paces_by_age = df["pace"].where(df["age"].values == i)
            paces_by_age = paces_by_age[~pd.isnull(paces_by_age)]
            if len(paces_by_age) != 0:
                pace_seconds = 0
                for entry in paces_by_age:
                    pace_seconds += pace_string_to_seconds(entry)
                sum_of_paces_by_age[i][0] += pace_seconds
                sum_of_paces_by_age[i][1] += len(paces_by_age) # Number of runners with age i
    return sum_of_paces_by_age


def get_average_pace_per_age():
    """Return avg pace in minutes per runner age across all race years"""
    sum_of_paces_by_age = get_sum_of_paces_by_age()
    
    avg_pace_per_age = []
    for j in range(len(sum_of_paces_by_age)):
        # Only consider age groups with at least 100 runners 
        if sum_of_paces_by_age[j][1] >= 100:
            avg_pace_per_age.append([round((sum_of_paces_by_age[j][0] / sum_of_paces_by_age[j][1])/60, 2),j])
    return avg_pace_per_age

def get_fastest_age():
    print("The fastest age is: " + str(min(get_average_pace_per_age())[1])) 

def plot_avg_pace_per_age():    
    data = np.asarray(get_average_pace_per_age(), dtype=np.float32)
    paces_data = data[:,0]
    age_data = data[:,1]

    plt.scatter(age_data, paces_data, color = cm.inferno_r(.6), s = 50)
    plt.xticks(np.arange(min(age_data) - min(age_data) % 5, max(age_data) + 5 - max(age_data) % 5, 5.0))
    m, b = np.polyfit(age_data, paces_data, 1)
    plt.plot(age_data, m*age_data + b, color = cm.inferno_r(.8))
    plt.style.use('seaborn-darkgrid')
    plt.gcf().set_size_inches((14, 10))   
    plt.title("Average Pace Per Age", fontsize = 20)
    plt.xlabel("Runners Age in Years", fontsize = 15)
    plt.ylabel("Pace (Minutes per Mile)", fontsize = 15)
    plt.show()

plot_avg_pace_per_age()
get_fastest_age()