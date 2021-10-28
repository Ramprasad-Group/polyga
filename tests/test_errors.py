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

def test_error_on_selection_scheme():
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
            # Error here
            partner_selection='diversite', 
            num_population_initial=180,
            )
    with pytest.raises(ValueError) as e_info:
        planet.advance_time()
    planet.complete_run()
    shutil.rmtree('Planet_Silly')

def test_crossover():
    planet = pg.PolyPlanet('Planet_Silly', 
            predict_function=predict,
            fingerprint_function=fingerprint,
            )

    land = pg.PolyLand('Awesomeland', planet, 
            generative_function=utils.chromosome_ids_to_smiles,
            fitness_function=fitness,
            # error here
            crossover_position='wrong'
            )

    nation = pg.PolyNation('UnitedPolymersOfCool', land,
            selection_scheme=selection_schemes.elite, 
            num_population_initial=180,
            )
    with pytest.raises(ValueError) as e_info:
        planet.advance_time()
    planet.complete_run()
    shutil.rmtree('Planet_Silly')

def test_num_cpus():
    planet = pg.PolyPlanet('Planet_Silly', 
            predict_function=predict,
            fingerprint_function=fingerprint,
            )

    land = pg.PolyLand('Awesomeland', planet, 
            generative_function=utils.chromosome_ids_to_smiles,
            fitness_function=fitness,
            )

    nation = pg.PolyNation('UnitedPolymersOfCool', land,
            selection_scheme=selection_schemes.elite, 
            num_population_initial=180,
            immigration_pattern={'wrong': .5}
            )

    nation = pg.PolyNation('UnitedPolymersOfCool2', land,
            selection_scheme=selection_schemes.elite, 
            num_population_initial=180,
            immigration_pattern={'wrong': .5}
            )
    with pytest.raises(ValueError) as e_info:
        planet.advance_time()
        planet.advance_time()
    planet.complete_run()
    shutil.rmtree('Planet_Silly')

