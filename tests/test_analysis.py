import pytest
import shutil
import os
import json
import pickle
import sqlite3
from collections import defaultdict
import random

import pandas as pd

from polyga import polygod as pg
from polyga import utils, selection_schemes
from polyga import analysis as pga
def nothing():
    print("test")

def fingerprint(df):
    fp_dict = defaultdict(list)
    columns = df.columns
    rand = random.random()
    for index, row in df.iterrows():
        fp_dict['fp_1'].append(index)
        fp_dict['fp_2'].append(len(df)-index)
        fp_dict['fp_3'].append((len(df)-index)/2)
        # Sometimes have variable length of pols
        if rand < 0.5:
            fp_dict['fp_4'].append(index % 2)
        for col in columns:
            fp_dict[col].append(row[col])
    fp_df = pd.DataFrame.from_dict(fp_dict)
    fp_headers = [col for col in fp_df.columns if 'fp_' in col]
    return fp_df, fp_headers

def predict(df, fp_headers, models):
    df['prop_1'] = [index % 3 for index in df.index]
    df['prop_2'] = [index * 2 for index in df.index]
    return df

def fitness(df, fp_headers):
    df['fitness'] = 1
    return df


def test_load_planet():
    planet = pg.PolyPlanet('Planet_Silly', 
            predict_function=predict,
            fingerprint_function=fingerprint,
            )

    land = pg.PolyLand('Awesomeland', planet, 
            generative_function=utils.chromosome_ids_to_smiles,
            fitness_function=fitness
            )

    nation = pg.PolyNation('UnitedPolymersOfCool', land, 
            selection_scheme=selection_schemes.elite, 
                           partner_selection='diversity', 
                           num_population_initial=180,
                           )
    for i in range(5):
        planet.advance_time()
    planet.complete_run()
    save_loc = 'Planet_Silly'
    df, fp_df = pga.load_planet(save_loc)
    for prop in ['prop_1', 'prop_2']:
        assert prop in df.columns
    for col in fp_df.columns:
        assert col not in df.columns
    assert len(fp_df.columns) >= 3
    assert 'chromosome_ids' in df.columns
    assert isinstance(df.chromosome_ids.to_list()[0], list)

    shutil.rmtree('Planet_Silly')

def test_delete():
    try:
        shutil.rmtree('Planet_Silly')
    except:
        pass
    

test_load_planet()
