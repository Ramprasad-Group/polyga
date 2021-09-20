import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import polyga.analysis as pga
save_loc = 'Planet_Silly'
df, fp_df = pga.load_planet(save_loc)

def find_smart_and_cool(df):
    """Finds smart and cool polymers and saves them to file."""
    properties = ['Polymer_Coolness', 'Polymer_Intelligence']
    df = df.copy()
    fitness = []
    scaled_dict = {}
    for prop in properties:
        vals = np.array(df[prop].values)
        vals = np.reshape(vals, (len(vals), -1))
        scaler = MinMaxScaler()
        scaled_vals = scaler.fit_transform(vals)
        scaled_dict[prop] = scaled_vals

    for i in range(len(df)):
        fit = 0
        for prop in properties:
            fit += 1/3 * scaled_dict[prop][i][0]
        fitness.append(fit)

    df['fitness'] = fitness
    sdf = df.nlargest(180, 'fitness')
    sdf.to_csv('cool_smart.csv', index=False) 

find_smart_and_cool(df)
