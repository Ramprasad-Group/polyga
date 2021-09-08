# Basic tutorials
## Navigation
- [Front Page](../../README.md)
- Running polyga
- [Analyzing polyga run](analyzing.md) 
- [Prediction of properties](predict.md)
- [Fingerprinting function](fingerprinting.md)
- [Creating fitness functions](fitness.md)
- [(OPTIONAL) tutorial background](background.md)

## Running polyga
In this tutorial we will learn how to run polyga. 
After running the [pip install](../../README.md/#pip-install) instructions
for polyga, download the zip folder for polyga by clicking the green "code" 
button and move the silly\_test folder to your working directory after 
downloading.

For background on why I named them planets, lands, and nations, see
[the background](../../background/ga.md)

You working directory should look something like this

```
.
+--My_directory/  
|  +--silly_test/  
|    +--silly_test.py
|    +--analyze_silly_test.py
|    +--additional_requirements.txt  
|    +--examples/  
|      +--Polymer_Coolness_random-forest.pkl  
|      +--Polymer_Funnyness_random-forest.pkl  
|      +--Polymer_Funnyness_random-forest.pkl  
|      +--silly_utils.py
```

Pip install the dependencies in additional\_requirements.txt, as these
are required to open the random-forest example models I have created.

After, cd into the silly\_test folder and run `python silly_test.py`.
It should run ten generations of polyga.

If you open silly\_test.py you'll see the following code:
```Python
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
```

To start, we import os, pickle, polyga and it's utility functions 
(polyga.utils), then import some special functions I wrote for this example.
```Python
import os
import pickle

from polyga import polygod as pg
from polyga import utils 

from examples import silly_utils
```

Then, we load the models we want to predict for our polymers. These will 
eventually be passed to our predict function. We load them here so
we don't have to reload them over and over again.

```Python
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
```

Next, we create the planet our lands and nations will reside on.
```Python
planet = pg.PolyPlanet('Planet_Silly', 
        predict_function=silly_utils.silly_property_prediction,
        fingerprint_function=silly_utils.silly_fingerprint,
        models=models
        )
```

We first name our planet 'Planet\_Silly' because, as you'll see in the future,
the data we generate is nonesense. Next, we specify the function we'll use
to predict polymer properties, and the function we'll use to generate polymer
fingerprints (we'll looking into these more closely in a later tutorial). 
Finally, we pass the models we previously loaded. Note that you don't have
to pass any if you don't use any models.

Now that our planet is set up, we add a land:
```Python
land = pg.PolyLand('Awesomeland', planet, 
        generative_function=utils.chromosome_ids_to_smiles,
        fitness_function=silly_utils.make_coolest_funniest_smartest_polymer
        )
```

We can add as many lands as we want, but in this example, we'll only make one.
We create a name for this land, 'Awesomeland', and associate it with the planet
we just created. Here we also define the generative function that will
create our polymers, and the fitness function that will rank them. Once again,
we'll expand upon these in a later tutorial.

Next we create a nation on our land:
```Python
nation = pg.PolyNation('UnitedPolymersOfCool', land,
                       selection_scheme=selection_schemes.elite,
                       partner_selection='diversity', 
                       num_population_initial=180,
                       )
```

Like our planet and land, we name our nation. Then we associate it with the
land (and by extension, the planet). We choose an elite selection scheme and
diversity partner selection for this nation. The selection scheme determines
how polymers for each generation will be chosen (elite meaning only the highest
scoring polymers will breed), while partner selection
indicates how a polymer will choose who it mates with. 'diversity' means it
will mate with the selected polymers that are least similar to it according to
its tanimoto similarity score.
Other options are available for these parameters and listed in the 
[docs](../../docs).

An arbitrary number of nations and lands can be created on each planet. When we
explore migration, we will see why this can be useful.

Finally, we run polyga:
```Python
for i in range(10):
    planet.advance_time()

planet.complete_run()
```

Each time we call planet.advance\_time(), a new generation is created and an
old one dies. After we're finished, we run planet.complete\_run() to close
our planet's sqlite database connection.

After the example runs you should see a new folder in silly\_test
```
.
+--My_directory/  
|  +--silly_test/  
|    +--silly_test.py
|    +--analyze_silly_test.py
|    +--additional_requirements.txt  
|    +--examples/  
|      +--Polymer_Coolness_random-forest.pkl  
|      +--Polymer_Funnyness_random-forest.pkl  
|      +--Polymer_Funnyness_random-forest.pkl  
|      +--silly_utils.py
|    +--Planet_Silly/
|      +--planetary_database.sqlite
```
Our planet has been created along with an sqlite database to save each 
generation of our planet.

Next, [let's analyze the polymers created by this run of polyga](analyzing.md).
