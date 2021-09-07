import os
import sqlite3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import polyga.analysis as pga
save_loc = 'Planet_Silly'
df, fp_df = pga.load_planet(save_loc)

for col in df.columns:
    print(col)


def plot_average_lengths(df):
    """Plots average lengths of polymers vs generation for all settled_nations"""
    gens = max(df.generation) + 1
    x = np.linspace(0, gens, gens)
    settled_nations = np.unique(df.settled_nation.values)
    legend = []
    for settled_nation in settled_nations:
        tdf = df.loc[df['settled_nation'] == settled_nation]
        means = []
        for gen in range(gens):
            tdf_ = tdf.loc[tdf['generation'] == gen]
            mean = tdf_.num_chromosomes.mean()
            means.append(mean)
        plt.plot(x, means)
        legend.append(settled_nation)
    plt.ylabel('Number of Blocks')
    plt.xlabel('Generation')
    plt.legend(legend, title='avg_num_blocks_per_polymer')
    plt.savefig(save_loc + '/length_avg.png')
    plt.clf()

def plot_property_averages(df):
    """Plots property averages for all settled_nations and displays them separately."""
    properties = ['Polymer_Coolness', 'Polymer_Funnyness','Polymer_Intelligence']
    settled_nations = np.unique(df.settled_nation.values)
    for settled_nation in settled_nations:
        means = []
        maxes = []
        mins = []
        stds = []
        tdf = df.loc[df.settled_nation == settled_nation]
        for prop in properties:
            mean = []
            std = []
            max_ = []
            min_ = []
            for i in range(max(tdf.generation) + 1):
                tdf_ = tdf.loc[tdf['generation'] == i]
                mean.append(tdf_[prop].mean())
                std.append(tdf_[prop].std())
                max_.append(max(tdf_[prop]))
                min_.append(min(tdf_[prop]))
            means.append(mean)
            stds.append(std)
            maxes.append(max_)
            mins.append(min_)

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=[16,9])
        x = np.linspace(0, max(tdf.generation), max(tdf.generation)+1)
        x = [val + 1 for val in x]
        row = 0
        col = 0
        curr = 0
        for prop in properties:
            max_ = maxes[curr]
            min_ = mins[curr]
            mean = means[curr]
            std = stds[curr]
            upper = [mean[i] + std[i] for i in range(len(mean))]
            lower = [mean[i] - std[i] for i in range(len(mean))]
            axes[row][col].fill_between(x, min_, max_, alpha=0.5, 
                color='darkblue'
            )
            axes[row][col].fill_between(x, lower, upper, alpha=0.5, 
                color='lightblue'
            )
            axes[row][col].plot(x, means[curr], lw=2, c='darkred')
            axes[row][col].set_ylabel(prop)
            axes[row][col].set_xlim([1,max(tdf.generation)+1])
            axes[row][col].set_xscale("log")
            curr += 1
            col += 1
            if col > 1:
                col = 0
                row += 1
        fig.delaxes(axes[1][1])
        fig.suptitle(settled_nation)
        plt.savefig(save_loc + '/' + settled_nation + '_property_avgs.png')
        plt.clf()

plot_property_averages(df)
plot_average_lengths(df)
