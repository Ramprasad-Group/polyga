import os
import sys
import sqlite3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

save_loc = 'Planet_Silly'
conn = sqlite3.connect(os.path.join(save_loc, 
    'planetary_database.sqlite')
)
query = "SELECT * FROM occupants"
df = pd.read_sql(query, conn)

cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
fingerprint_tables = []
for i in range(len(tables)):
    if i != 0:
        table = tables[i][0]
        fingerprint_tables.append(table)
conn.close()

print(fingerprint_tables)

for col in df.columns:
    print(col)

def plot_average_lengths(df):
    """Plots average lengths of polymers vs generation for all nations"""
    gens = max(df.generation) + 1
    x = np.linspace(0, gens, gens)
    nations = np.unique(df.nation.values)
    legend = []
    for nation in nations:
        tdf = df.loc[df['nation'] == nation]
        means = []
        for gen in range(gens):
            tdf_ = tdf.loc[tdf['generation'] == gen]
            mean = tdf_.num_chromosomes.mean()
            means.append(mean)
        plt.plot(x, means)
        legend.append(nation)
    plt.legend(legend)
    plt.savefig(save_loc + '/length_avg.png')
    plt.clf()

def plot_property_averages(df):
    """Plots property averages for all nations and displays them separately."""
    properties = ['Polymer_Coolness', 'Polymer_Funnyness','Polymer_Intelligence']
    nations = np.unique(df.nation.values)
    for nation in nations:
        vals = []
        tdf = df.loc[df.nation == nation]
        for prop in properties:
            val = []
            for i in range(max(tdf.generation) + 1):
                tdf_ = tdf.loc[tdf['generation'] == i]
                val.append(tdf_[prop].mean())
            vals.append(val)

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=[16,9])
        x = np.linspace(0, max(tdf.generation), max(tdf.generation)+1)
        x = [val + 1 for val in x]
        row = 0
        col = 0
        curr = 0
        for prop in properties:
            axes[row][col].plot(x, vals[curr], lw=2, c='darkred')
            axes[row][col].set_ylabel(prop)
            axes[row][col].set_xlim([1,max(tdf.generation)+1])
            axes[row][col].set_xscale("log")
            curr += 1
            col += 1
            if col > 1:
                col = 0
                row += 1
        fig.delaxes(axes[1][1])
        fig.suptitle(nation)
        plt.savefig(save_loc + '/' + nation + '_property_avgs.png')
        plt.clf()

plot_property_averages(df)
plot_average_lengths(df)
