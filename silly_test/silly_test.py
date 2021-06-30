from polyga import polygod as pg
from polyga import utils 

from examples import silly_utils

planet = pg.PolyPlanet('Planet_Silly', 
        predict_function=silly_utils.silly_property_prediction,
        fingerprint_function=silly_utils.silly_fingerprint
        )

land = pg.PolyLand('Awesomeland', planet, 
        generative_function=utils.chromosome_ids_to_smiles,
        fitness_function=silly_utils.make_coolest_funniest_smartest_polymer
        )
nation = pg.PolyNation('UnitedPolymersOfCool', land, selection_scheme='elite', 
                       partner_selection='diversity', 
                       num_population_initial=180,
                       )

for i in range(5):
    planet.advance_time()

planet.complete_run()
