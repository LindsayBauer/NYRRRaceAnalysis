from os import path
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

annual_files = [str(year) + ".json" for year in range(2010,2020)]

def get_data_all_years():
    frames = []
    for year in annual_files:
        getData = pd.read_json(path.join(Path.cwd(), 'Data', year),
                               orient='columns')['response']
        df = pd.DataFrame.from_records(getData['items'])
        frames.append(df)
    return pd.concat(frames)


def get_top_first_names():
    """Return dictionary of the 50 most common first names of the top 500 finishers across all years.
    Keys are the names and values are the proportion of top finishers with that name""" 
    name_proportions = {}
    combined_data = get_data_all_years()
    top_names = pd.DataFrame(combined_data['firstName'].where(
            (combined_data["overallPlace"].values <= 500)).value_counts())
    for row in top_names.head(50).itertuples():
        name_proportions[row[0]] = round(row[1] / len(top_names.index), 10)
    return name_proportions


def plot_top_first_names():
    name_proportions = get_top_first_names()
    wc = WordCloud(background_color = "white", relative_scaling = 0.5).generate_from_frequencies(name_proportions)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()

plot_top_first_names()


def get_most_common_first_names():
    """Return dictionary of the 50 most common first names of runners across all years
    Keys are the names and values are the proportion of runners with that name"""
    name_proportions = {}
    combined_data = get_data_all_years()
    num_entries = len(combined_data.index)
    common_names = pd.DataFrame(combined_data['firstName'].value_counts().head(50))
    for row in common_names.itertuples():
        name_proportions[row[0]] = round(row[1] / num_entries, 10)
    return name_proportions


def plot_most_common_first_names():
    name_proportions = get_most_common_first_names()
    wc_new = WordCloud(background_color = "white", relative_scaling = 0.5).generate_from_frequencies(name_proportions)
    plt.imshow(wc_new, interpolation='bilinear')
    plt.axis("off")
    plt.show()

plot_most_common_first_names()


def get_difference_of_name_groups():
    uncommon_top_finisher_names = get_top_first_names().keys() - get_most_common_first_names()
    common_not_top_finisher_names = get_most_common_first_names().keys() - get_top_first_names()
    print("Uncommon top finisher names: " + ', '.join([name for name in uncommon_top_finisher_names]))
    print("Common names that aren't top finishers: " + ', '.join([name for name in common_not_top_finisher_names]))
    
get_difference_of_name_groups()