import pytest
import shutil
import os
import pickle

from polyga import polygod as pg
from polyga import utils 

def nothing():
    print(test) 

def test_initialize():
    planet = pg.PolyPlanet('Planet_Silly', 
            predict_function=nothing,
            fingerprint_function=nothing,
            )

    land = pg.PolyLand('Awesomeland', planet, 
            generative_function=utils.chromosome_ids_to_smiles,
            fitness_function=nothing
            )

    nation = pg.PolyNation('UnitedPolymersOfCool', land, selection_scheme='elite', 
                           partner_selection='diversity', 
                           num_population_initial=180,
                           )
    planet.complete_run()
    shutil.rmtree('Planet_Silly')


