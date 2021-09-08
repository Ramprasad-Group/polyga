import os
import pickle

from polyga import polygod as pg
from polyga import utils, selection_schemes

from examples import silly_utils

# Load models for property predictions
model_folder = 'examples'
properties = {
          'Polymer_Coolness': 'Polymer_Coolness_random-forest.pkl',
          'Polymer_Intelligence': 'Polymer_Intelligence_random-forest.pkl',
          'Polymer_Funnyness': 'Polymer_Funnyness_random-forest.pkl'
         }
models = {}

for prop in properties:
    model_file = open(os.path.join(model_folder, properties[prop]), 'rb')
    models[prop] = pickle.load(model_file)
    model_file.close()

planet = pg.PolyPlanet('Planet_Silly', 
        predict_function=silly_utils.silly_property_prediction,
        fingerprint_function=silly_utils.silly_fingerprint,
        models=models
        )

land = pg.PolyLand('Awesomeland', planet, 
        generative_function=utils.chromosome_ids_to_smiles,
        fitness_function=silly_utils.make_coolest_funniest_smartest_polymer
        )

nation = pg.PolyNation('UnitedPolymersOfCool', land,
                       selection_scheme=selection_schemes.elite,
                       partner_selection='diversity', 
                       num_population_initial=180,
                       )

for i in range(10):
    planet.advance_time()

planet.complete_run()
