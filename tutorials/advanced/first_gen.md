# Advanced tutorials
## Navigation
- [Front Page](../../README.md)
- Using a custom first generation

## Custom First Generation
When you use polyga, the default behavior is for the app to randomly generate
the first generation of polymers. However, some users may want to manually
select the first generation. To do this, there are two methods: loading a 
file or loading a dataframe.

## Loading a file
First, let's set up a general planet and land


```Python
import os
import pickle

import pandas as pd

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

planet = pg.PolyPlanet('Planet_Funny', 
        predict_function=silly_utils.silly_property_prediction,
        fingerprint_function=silly_utils.silly_fingerprint,
        models=models
        )

land = pg.PolyLand('Funnyland', planet, 
        generative_function=utils.chromosome_ids_to_smiles,
        fitness_function=silly_utils.make_funniest_polymer
        )
```

Now, maybe we ran a previous run and found several promising polymers that
were super cool and smart, but not very funny. We want to run again with these
cool and smart polymers, but bias them towards being funny this time around.
For that reason, we've used a new fitness function called "make\_funniest\_polymer.

We've saved these cool and smart polymers in a folder in our local directory 
called "cool\_smart.csv". 
```Python
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
```

They must be saved in csv format.

Now pass them to a new nation and run.

```Python
nation = pg.PolyNation('FunnyPoly', land,
                       selection_scheme=selection_schemes.elite,
                       partner_selection='diversity', 
                       num_population_initial=180,
                       initial_population_file='cool_smart.csv',
                       )

for i in range(10):
    planet.advance_time()

planet.complete_run()
```

We could also have loaded the dataframe first and passed that.

```Python
df = pd.read_csv('cool_smart.csv')
nation = pg.PolyNation('FunnyPoly', land,
                       selection_scheme=selection_schemes.elite,
                       partner_selection='diversity', 
                       num_population_initial=180,
                       initial_population=df
                       )

for i in range(10):
    planet.advance_time()

planet.complete_run()
```

We just use initial\_population instead of initial\_population\_file.

These dataframes and files must contain the following columns in order 
to load properly: 
 'chromosome\_ids',
 'num\_chromosomes',
 'parent\_1\_id',
 'parent\_2\_id',
 'smiles\_string',
 'birth\_land',
 'birth\_nation',
 'birth\_planet'.

You can add fillers for these columns, but they must be in the file or
dataframe. Chromosome\_ids, smiles\_string and num\_chromosomes must be 
correct and not fillers though. The full code is below.

```Python
import os
import pickle

import pandas as pd

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

planet = pg.PolyPlanet('Planet_Funny', 
        predict_function=silly_utils.silly_property_prediction,
        fingerprint_function=silly_utils.silly_fingerprint,
        models=models
        )

land = pg.PolyLand('Funnyland', planet, 
        generative_function=utils.chromosome_ids_to_smiles,
        fitness_function=silly_utils.make_funniest_polymer
        )
        
nation = pg.PolyNation('FunnyPoly', land,
                       selection_scheme=selection_schemes.elite,
                       partner_selection='diversity', 
                       num_population_initial=180,
                       initial_population_file='cool_smart.csv',
                       )

for i in range(10):
    planet.advance_time()

planet.complete_run()
```

