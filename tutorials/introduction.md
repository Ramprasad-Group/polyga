Hello! In this introduction, you'll learn how to import polyga and run some
experiments to find new polymers.

I assume you have already read the
[README](../README.md) intro, but if
not, just ensure you have all the required dependencies.

To start, import the package and some other necessary dependencies.
```Python
from polyga import polygod
import pandas as pd
import numpy as np
from sklearn import preprocessing
```

polyga requires the user to define the fitness function that will guide polymer
evolution. Thus, create a function that will accept a pandas dataframe as input,
then define how you want to evolve your polymers.
```Python
def fitness_function(df):
    """Encourage the evolution of polymers with glass transition temperatures of
       500 K. 

       All fitness functions must returns list with order unaltered
    """
    tgs = df.exp_Tg.values
    # Those with values closest to 500 will have highest fitness score
    tgs = [500 - abs(tg-500) for tg in tgs]
    tgs = np.array(tgs)
    # Reshape for processing
    tgs = np.reshape(tgs,(len(tgs),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    tgs = scaler.fit_transform(tgs)
    return tgs
```
In this example, I want polymers with a glass transition temperature (Tg) as 
close to 500 K as possible. Remember, you must return a list or 1-d
numpy array and the order of polymers must not be altered.

After defining the fitness function, we can create the planet, lands, and 
nations. Each land must have a fitness function passed to it. Each planet,
land and nation must have a name. The lands must have the planet passed
to them as well, and the nations must have a land passed to them.
```Python
planet = PG.PolyPlanet('PolyLand')
# Must pass a fitness function the all land, but they can be different
land = PG.PolyLand('HighTg', planet, fitness_function=fitness_function)
nation = PG.PolyNation('Polypeptland', land) 
```

Advancing time on the planet will cause the polymers of each nation to evolve
according to the fitness function of the land they reside on. Each nation
and land has a variety of parameters that can be passed to it to influence
this evolution. These parameters can be seen in the docs folder on github.
```Python
# Run for 15 generations
for i in range(15):
    planet.advance_time()
```

You may be wondering how we are able to determine the exp_Tg for the polymers.
polyga requires you to have your own models available that can predict
polymer properties. script.py is the current script we're writing.
Within the models folder are two folders called "exp_Tg" and "exp_Eg".
Within these folders are PolymerGenome trained models that can predict
glass transition temperature and bandgap respectively. 
```
.  
+-- script.py  
+-- models  
|   +-- exp_Tg  
|       +-- model.pkl  
|   +-- exp_Eg  
|       +-- model.pkl  
```
We'll know which properties are accessible in the fitness function based on 
the name of the folder you add to your models folder. For instance, if the
exp_Tg folder was renamed to "experimental_Tg", we would access the predicted
values as
```Python
    tgs = df.experimental_Tg.values
```
instead of
```Python
    tgs = df.exp_Tg.values
```

Similarily, if we wanted to try and create polymers with bandgaps of 9, we could
pass this fitness function to a land instead.

```Python
def fitness_function(df):
    """Encourage the evolution of polymers with bandgaps of
       9 eV. 

       All fitness functions must returns list with order unaltered
    """
    egs = df.exp_Eg.values
    # Those with values closest to 9 will have highest fitness score
    egs = [9 - abs(eg-9) for eg in egs]
    egs = np.array(egs)
    # Reshape for processing
    egs = np.reshape(egs,(len(egs),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    egs = scaler.fit_transform(egs)
    return egs
```

Once you feel the children have evolved for long enough, we can complete the
run.
```Python
planet.complete_run()
```
This is important to have, as it will close the connection to the sqlite
database.

The full script is below. After, check out the section on
[accessing old runs](accessing_old_runs.md) to learn how to extract
data from your polymers.


```Python
from polyga import polygod
import pandas as pd
import numpy as np
from sklearn import preprocessing

def fitness_function(df):
    """Encourage the evolution of polymers with glass transition temperatures of
       500 K. 

       All fitness functions must returns list with order unaltered
    """
    tgs = df.exp_Tg.values
    # Those with values closest to 500 will have highest fitness score
    tgs = [500 - abs(tg-500) for tg in tgs]
    tgs = np.array(tgs)
    # Reshape for processing
    tgs = np.reshape(tgs,(len(tgs),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    tgs = scaler.fit_transform(tgs)
    return tgs

planet = PG.PolyPlanet('PolyLand')
# Must pass a fitness function the all land, but they can be different
land = PG.PolyLand('HighTg', planet, fitness_function=fitness_function)
nation = PG.PolyNation('Polypeptland', land) 

# Run for 15 generations
for i in range(15):
    planet.advance_time()

planet.complete_run()
```
