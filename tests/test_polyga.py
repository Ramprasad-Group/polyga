import pytest
import shutil
import os
import json
import pickle
import sqlite3
from collections import defaultdict

import pandas as pd

from polyga import polygod as pg
from polyga import utils, selection_schemes
def nothing():
    print("test")

def fingerprint(df):
    fp_dict = defaultdict(list)
    columns = df.columns
    for index, row in df.iterrows():
        fp_dict['fp_1'].append(index)
        fp_dict['fp_2'].append(len(df)-index)
        fp_dict['fp_3'].append((len(df)-index)/2)
        fp_dict['fp_4'].append(index % 2)
        for col in columns:
            fp_dict[col].append(row[col])
    fp_df = pd.DataFrame.from_dict(fp_dict)
    fp_headers = [col for col in fp_df.columns if 'fp_' in col]
    return fp_df, fp_headers

def predict(df, fp_headers, models):
    df['prop_1'] = [index % 3 for index in df.index]
    df['prop_2'] = [index * 2 for index in df.index]
    df['fp_5'] = 0
    return df

def fitness(df, fp_headers):
    df['fitness'] = 1
    return df


def test_initialize():
    planet = pg.PolyPlanet('Planet_Silly', 
            predict_function=nothing,
            fingerprint_function=nothing,
            )

    land = pg.PolyLand('Awesomeland', planet, 
            generative_function=utils.chromosome_ids_to_smiles,
            fitness_function=nothing
            )

    nation = pg.PolyNation('UnitedPolymersOfCool', land, 
            selection_scheme=selection_schemes.elite, 
                           partner_selection='diversity', 
                           num_population_initial=180,
                           )
    planet.complete_run()
    shutil.rmtree('Planet_Silly')

def test_adding_polymers():
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
    planet.advance_time()
    planet.complete_run()
    save_loc = 'Planet_Silly'
    conn = sqlite3.connect(os.path.join(save_loc, 
        'planetary_database.sqlite')
    )
    query = "SELECT * FROM polymer"
    df = pd.read_sql(query, conn)
    fp_headers = ['fp_1', 'fp_2', 'fp_3', 'fp_4']
    prop_headers = ['prop_1', 'prop_2']
    for index, row in df.iterrows():
        fp = json.loads(row['fingerprint'])
        properties = json.loads(row['properties'])
        assert list(fp.keys()) == fp_headers
        assert list(properties.keys()) == prop_headers
    shutil.rmtree('Planet_Silly')

def test_delete():
    try:
        shutil.rmtree('Planet_Silly')
    except:
        pass
    
