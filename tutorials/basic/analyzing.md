# Basic tutorials
## Navigation
- [Front Page](../../README.md)
- [Running polyga](basic.md)
- [Analyzing polyga run](analyzing.md) 
- [Prediction of properties](predict.md)
- [Fingerprinting function](fingerprinting.md)
- [Creating fitness functions](fitness.md)
- [(OPTIONAL) tutorial background](background.md)

## Analyzing polyga run
After running polyga, we want to analyze the polymers (or other materials)
we have created. To start, let's run the 'analyze\_silly\_test.py' script in 
the silly\_test folder by running the command  
`python analyze_silly_test.py`  
in the terminal
(to see how your directory should look, see the [previous tutorial](basic.md)).

First, the follwing data should print to the terminal.

```
['fingerprints_T1', 'fingerprints_T2']  
planetary_id  
parent_1_id  
parent_2_id  
is_parent  
num_chromosomes  
smiles_string  
birth_land  
birth_nation  
birth_planet  
str_chromosome_ids  
land  
generation    
nation  
planet  
Polymer_Coolness  
Polymer_Intelligence  
Polymer_Funnyness  
```

If we open the Silly\_Test folder we should see some images as well. The first
one should look something like this, although, GAs are heuristic models so
your results may vary.  
![properties image](../../imgs/UnitedPolymersOfCool_property_avgs.png)

In this image, the darkred line is the average property value per polymer at
each generation, the light blue is the average +/- the standard deviation, and
the dark blue is the min to max property value of polymers in each generation.
The generations are plotted on a log scale and we see that average values
increase per generation.

This indicates that, like in real life, each generation of polymers is getting 
progressively cooler, funnier, and smarter. However, the next image will offset
this excitement.

![pol length img](../../imgs/length_avg.png)

Here we see the polymers are getting longer as time goes by. If we actually 
wanted to synthesize these polymers, this increase in length would make that 
much more challenging. To understand why this is occuring, we'll have
to examine our random forest models and fingerprints in a bit, but first, let's
go over the code that facilitated this analysis.

```Python
import os
import sqlite3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    plt.ylabel('Number of Blocks')
    plt.xlabel('Generation')
    plt.legend(legend, title='avg_num_blocks_per_polymer')
    plt.savefig(save_loc + '/length_avg.png')
    plt.clf()

def plot_property_averages(df):
    """Plots property averages for all nations and displays them separately."""
    properties = ['Polymer_Coolness', 'Polymer_Funnyness','Polymer_Intelligence']
    nations = np.unique(df.nation.values)
    for nation in nations:
        means = []
        maxes = []
        mins = []
        stds = []
        tdf = df.loc[df.nation == nation]
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
        fig.suptitle(nation)
        plt.savefig(save_loc + '/' + nation + '_property_avgs.png')
        plt.clf()

plot_property_averages(df)
plot_average_lengths(df)
```

I won't go into as much detail since a lot of the material is related to 
plotting with matplotlib, but I will discuss a few key points.

First, this section:
```Python
save_loc = 'Planet_Silly'
conn = sqlite3.connect(os.path.join(save_loc, 
    'planetary_database.sqlite')
)
query = "SELECT * FROM occupants"
df = pd.read_sql(query, conn)
```

The first thing we're doing is opening our database and extracting our polymers.
They are located in the 'occupants' table.
```Python
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
fingerprint_tables = []
for i in range(len(tables)):
    # Ignore occupants table
    if i != 0:
        table = tables[i][0]
        fingerprint_tables.append(table)
conn.close()

print(fingerprint_tables)
```

Next, we are looking at all of the tables in the database. The first one is
the occupants one, which we choose to ignore. All subsequent ones are 
fingerprint tables. The reason why we have multiple is because sqlite only
allows 2000 columns per table. In this example, we have 
``` 
['fingerprints_T1', 'fingerprints_T2']  
```
because there are over 2000 fingerprints (which we'll go over in the 
fingerprint tutorial).

We don't open these tables in this code, but if we had wanted to we could use
something like the following code:
```Python
dfs = []
for table in fingerprint_tables:
    query = "SELECT * FROM " + table
    fp_df = pd.read_sql(query, conn)
    dfs.append(fp_df.copy())
```

After looking at the fingerprinting tables, we run this:
```Python
for col in df.columns:
    print(col)
```

Which printed that list to the terminal previously. These are the column
headers that will be generated each time the GA runs, with the exception of the
property columns. These will depend on the properties you are using.

The rest of the code should be relatively self explanatory, so I'll leave
that for you to read. There are a lot of analyses you could run on your results
including uniform manifold approximation and projection maps, an analysis of
chemical composition vs generation, frequency of blocks, etc... 
so I did not include all possible analyses here.

For now, let's go more in depth into 
[how we predicted the polymer properties](predict.md).
