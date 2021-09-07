<a name="polygod"></a>

# polygod

PolyGod contains PolyPlanet, PolyLand, and PolyNation classes

<a name="polygod.PolyPlanet"></a>

## PolyPlanet Objects

```python
class PolyPlanet()
```

PolyPlanet contains the PolyLands and PolyNations of the world.

PolyPlanet keeps track of polymer emigration patterns, dna lists, and
some other information.

**Attributes**:

  
  num_citizens (int):
  Number of citizens ever existing on planet.
  name (str):
  name of the planet/folder where data is saved.
  
  lands (list):
  list of all lands on the planet
  
  dna (pd.DataFrame):
  pandas dataframe containing chromosomes,
  their frequency in nature, and the chromosome ids.
  
  chromosomes (dict):
  dictionary of chromosome ids and their
  chromosome polymers can use.
  
  random_seed (int):
  Random seed to use for planet. If 0, no
  random seed is used.
  
  save_folder (str):
  Path to save planet/nations in.
  Default is None, which
  means save in current folder.
  
  planetary_database (str):
  Path to database of all polymers and their predicted
  properties.
  
  emigration_list (list):
  Stores emigration information for a generation.
  
  num_nations (int):
  Number of nations on the planet.
  
  predict_function (callable):
  Function to predict properties of polymers. Passed dataframe of
  polymers, should return same dataframe with propery predictions
  attached.
  
  fingerprint_function (callable):
  Function to fingerprint polymers. Passed population dataframe. Must
  return dataframe with fingerprints attached.
  
  models (dict):
  Models dict with key as parameter name, value as model used in
  predict function. Default None, in case no model used.
  
  num_cpus (int):
  Number of cpus to use when fingerprinting and predicting
  properties. If number on computer exceeded, number set to
  number on computer. Default is one.

<a name="polygod.PolyPlanet.__init__"></a>

#### \_\_init\_\_

```python
 | __init__(name: str, predict_function: callable, fingerprint_function: callable, models: dict = None, num_cpus: int = 1, random_seed: int = 0, path_to_dna: str = None, save_folder: str = None)
```

Initialize planet

**Arguments**:

  
  name (str):
  Name of the planet/folder where data is saved.
  
  predict_function (callable):
  Function to predict properties of polymers. Passed dataframe of
  polymers, should return same dataframe with propery predictions
  attached.
  
  fingerprint_function (callable):
  Function to fingerprint polymers. Passed population dataframe.
  Must return dataframe with fingerprints attached and a list
  of fingerprint column headers.
  
  random_seed (int):
  Random seed to use for planet. If 0, no
  random seed is used.
  
  path_to_dna (str):
  Full path to block list used to create
  polymers. Default is original PolyGA block list.
  
  save_folder (str):
  Path to save planet/nations in.
  Default is None, which
  means save in current folder.
  
  models (dict):
  Models dict with key as parameter name, value as model used in
  predict function. Default None, in case no model used.
  
  num_cpus (int):
  Number of cpus to use when fingerprinting and predicting
  properties. If number on computer exceeded, number set to
  number on computer. Default is one.

<a name="polygod.PolyPlanet.add"></a>

#### add

```python
 | add(land: 'PolyLand')
```

Add reference to lands on the planet

<a name="polygod.PolyPlanet.advance_time"></a>

#### advance\_time

```python
 | advance_time(take_census: bool = True, narrate: bool = True)
```

Runs through generation of genetic algorithm on all the lands

First fingerprints, predicts properties of, and scores all polymers.
Then creates emigration list of emigrating polymers. Then
immigrates polymers to new nation. Finally, breeds polymers and saves.

**Arguments**:

  
  take_census (bool):
  If true, generation information saved
  
  narrate (bool):
  if true narration message occur

<a name="polygod.PolyPlanet.complete_run"></a>

#### complete\_run

```python
 | complete_run()
```

Close database connection

<a name="polygod.PolyPlanet.immigrate"></a>

#### immigrate

```python
 | immigrate()
```

Immigrates polymers in emigration list

<a name="polygod.PolyPlanet.random_seed"></a>

#### random\_seed

```python
 | random_seed()
```

Returns random generator seed or None if seed is 0

<a name="polygod.PolyPlanet.remove"></a>

#### remove

```python
 | remove(land: 'PolyLand')
```

Remove reference to the land on the planet

<a name="polygod.PolyPlanet.num_lands"></a>

#### num\_lands

```python
 | num_lands()
```

Returns number of lands on the planet

<a name="polygod.PolyPlanet.take_census"></a>

#### take\_census

```python
 | take_census()
```

Saves all population data of nations in folder (planets name)

<a name="polygod.PolyPlanet.uid"></a>

#### uid

```python
 | uid()
```

Returns unique id for a new polymer and increases number of citizens.


Note, uid = 0 means parent of polymer was none

<a name="polygod.PolyLand"></a>

## PolyLand Objects

```python
class PolyLand()
```

PolyLand contains various PolyNations.

It's environment determines how polymers mutate and what features ensure
their survival.

**Attributes**:

  
  name (str):
  Name of the land.
  
  planet (PolyPlanet):
  PolyPlanet land is located on.
  
  nations (list):
  All nations on the land.
  
  crossover_position (str):
  str representing crossover cutting position.
  'relative_center' = center with Gaussian distribution,
  'center'=exact center, 'random'=random position.
  Default is 'relative_center'
  
  crossover_sigma_offset (float):
  float representing standard deviation of cut
  from center position for crossover (unit: block).
  Only applies for 'relative_center'.
  Default 0.1 blocks.
  
  fraction_mutation (float):
  Number representing chance of mutation.
  Ex, 0.1 = 10% (in average of Gaussian distribution)
  of genomes in a monomer can be mutated.
  Default is 0.1.
  
  mutation_sigma_offset (float):
  Float representing standard deviation of
  number of blocks to be mutated (unit: %/100).
  Default is 0.25 (=25%).
  
  fraction_mutate_additional_block (float):
  float indicating percent of polymers to append
  randomly chosen block to (0.1 = 10%). Default 0.05
  
  land_chromosomes (list):
  Chromosome ids land can use.
  
  generative_function (callable):
  Function to put together chromosomes into polymer. Passed
  list of chromosomes and dna, returns smiles of polymer
  
  generative_function_parameters (Dict):
  Extra parameters for generative function in dict format.
  Default an empty Dict
  
  fitness_function (callable):
  Function to assess fitness of polymers by. Passed population
  dataframe. Must return
  a list or 1d np.array thats order is in the same
  order as the population dataframe.

<a name="polygod.PolyLand.add"></a>

#### add

```python
 | add(nation: 'PolyNation')
```

Add refence to nations on the land

<a name="polygod.PolyLand.propagate_nations"></a>

#### propagate\_nations

```python
 | propagate_nations(take_census: bool = True, narrate: bool = True)
```

Generates families and propagates next generation of all nations.

**Arguments**:

  
  take_census (bool):
  If true, generation information saved
  
  narrate (bool):
  If true narration message occur

<a name="polygod.PolyLand.genetic_information"></a>

#### genetic\_information

```python
 | genetic_information()
```

Returns how the environment affects the genes of polymers in this land

e.g., returns mutation and crossover information

Returns (tuple):   
    (fraction_mutation, mutation_sigma_offset,
     fraction_mutate_additional_block, crossover_position,
     crossover_sigma_offset)

<a name="polygod.PolyLand.num_nations"></a>

#### num\_nations

```python
 | num_nations()
```

Returns number of nations on the land

<a name="polygod.PolyLand.remove"></a>

#### remove

```python
 | remove(nation: 'PolyNation')
```

Remove reference to the nation on the land if nation exists on land

<a name="polygod.PolyLand.score_and_emigrate"></a>

#### score\_and\_emigrate

```python
 | score_and_emigrate(narrate)
```

Assesses fitness scores of polymers and emigrates them.

Where fingerprinting and property prediction occurs.

**Arguments**:

  
  narrate (bool):
  If true narration message occur

<a name="polygod.PolyLand.take_census"></a>

#### take\_census

```python
 | take_census()
```

Saves all populations data in land

<a name="polygod.PolyNation"></a>

## PolyNation Objects

```python
class PolyNation()
```

PolyNation is where population changes occur.

They are influenced by their PolyLand.

**Attributes**:

  
  name (str):
  name of the nation
  
  land (PolyLand):
  PolyLand Nation is located on
  
  initial_population_file (str):
  Optional. Full path to file containing initial population. If
  initial_population and initial_population_file None, random initial
  population is used. If both passed,
  initial_population takes preference. Default None.
  
  initial_population (pandas.DataFrame):
  Pandas dataframe containing initial population. If
  initial_population and initial_population_file None, random initial
  population is used. If both passed,
  initial_population takes preference. Default None.
  
  num_families (int):
  Number of families that will propagate. Default 45
  
  num_parents_per_family (int):
  Each pair of parents will mate. Default 2.
  
  num_children_per_family (int):
  Number of children per pair of parents. Default is 4.
  
  generation (int):
  Current generation of polymers in this nation.
  
  selection_scheme (str):
  str representing how polymers in this nation choose
  to mate. 'elite' means only the highest scoring
  polymers mate. 'random' means random polymers are
  chosen. Default 'elite'
  
  partner_selection (str):
  str representing how parents choose their mate.
  'diversity' means highest scoring parents choose
  partner based on least similar tanimoto similarity
  score. 'random' means partner chosen randomly.
  Default 'diversity'.
  
  emigration_rate (float):
  Value between 0 and 0.5 representing the % of polymers that will
  emigrate to a new nation. Values greater than
  0.5 reduced to 0.5. Values less than 0 increased to 0.
  Default is 0.1 (10%).
  
  emigration_selection (str):
  Method of selecting which polymers will emigrate. "random" means
  random selection. "elite" means highest scoring in current
  nation will emigrate. "best_worst" means the highest scoring
  polymers that wouldn't be selected as parents emigrate.
  Default is "best_worst"
  
  parent_migrant_percentage (float):
  Percentage of parents that will automatically be migrants, even
  if their fitness score is low. For example, if .1, 10% of parents
  will be migrants, if available. Parents will be taken equally from
  **from each nation** until max added. Default is 0.1
  
  immigration_pattern (dict):
  keys of dict are strings representing the country polymers will
  immigrate too, values are floats representing the percentage of
  polymers that will emigrate. i.e., if 10% are migrating total,
  with 50% to nation_a, 50% nation_b, the dict would be
  ``immigration_pattern = {'nation_a': 50%, 'nation_b': 50%}``
  If no dict provided, polymers emigrate randomly. If percentages
  sum to greater than 1, percentages normalized. If percentages
  summed to less than one, remaining polymers sent to random
  locations. If location indicated that doesn't exist, error
  is thrown.
  
  random_seed (int):
  Random seed to use for nation. If 0, no
  random seed is used.

<a name="polygod.PolyNation.__init__"></a>

#### \_\_init\_\_

```python
 | __init__(name: str, land: PolyLand, initial_population_file: str = None, initial_population: pd.DataFrame = None, num_population_initial: int = 180, num_chromosomes_initial: int = 4, num_families: int = 15, num_parents_per_family: int = 3, num_children_per_family: int = 12, selection_scheme: str = 'elite', partner_selection: str = 'diversity', emigration_rate: float = 0.1, emigration_selection: str = 'best_worst', parent_migrant_percentage: float = 0.1, immigration_pattern: dict = {}, random_seed: int = 0)
```

Intialize nation.

**Arguments**:

  
  name (str):
  name of the nation
  
  land (PolyLand):
  PolyLand Nation is located on
  
  initial_population_file (str):
  Optional. Full path to file containing initial population. If
  initial_population and initial_population_file None, random
  initial population is used. If both passed,
  initial_population takes preference. Default None.
  
  initial_population (pandas.DataFrame):
  Pandas dataframe containing initial population. If
  initial_population and initial_population_file None, random
  initial population is used. If both passed,
  initial_population takes preference. Default None.
  
  num_population_initial (int):
  Number of polymers to randomly generate for the initial pop.
  
  num_families (int):
  Number of families that will propagate. Default 45
  
  num_parents_per_family (int):
  Each pair of parents will mate. Default 2.
  
  num_children_per_family (int):
  Number of children per pair of parents. Default is 4.
  
  selection_scheme (str):
  str representing how polymers in this nation choose
  to mate. 'elite' means only the highest scoring
  polymers mate. 'random' means random polymers are
  chosen. Default 'elite'
  
  partner_selection (str):
  str representing how parents choose their mate.
  'diversity' means highest scoring parents choose
  partner based on least similar tanimoto similarity
  score. 'random' means partner chosen randomly.
  Default 'diversity'.
  
  emigration_rate (float):
  Value between 0 and 0.5 representing the % of polymers that will
  emigrate to a new nation. Values greater than
  0.5 reduced to 0.5. Values less than 0 increased to 0. Polymers
  who emigrate are chosen via emigration_selection.
  Default is 0.1 (10%).
  
  emigration_selection (str):
  Method of selecting which polymers will emigrate. "random" means
  random selection. "elite" means highest scoring in current
  nation will emigrate. "best_worst" means the highest scoring
  polymers that wouldn't be selected as parents emigrate.
  Default is "best_worst"
  
  parent_migrant_percentage (float):
  Percentage of parents that will automatically be migrants, even
  if their fitness score is low. For example, if .1, 10% of parents
  will be migrants, if available. Parents will be taken equally from
  **from each nation** until max added. Default is 0.1
  
  immigration_pattern (dict):
  keys of dict are strings representing the country polymers will
  immigrate too, values are floats representing the percentage of
  polymers that will emigrate. i.e., if 10% are migrating total,
  with 50% to nation_a, 50% nation_b, the dict would be
  ``immigration_pattern = {'nation_a': 50%, 'nation_b': 50%}``
  If no dict provided, polymers emigrate randomly. If percentages
  sum to greater than 1, percentages normalized. If percentages
  summed to less than one, remaining polymers sent to random
  locations. If location indicated that doesn't exist, error
  is thrown.

<a name="polygod.PolyNation.family_demographics"></a>

#### family\_demographics

```python
 | family_demographics()
```

Returns demographics of family (number of parents and children)

<a name="polygod.PolyNation.propagate_species"></a>

#### propagate\_species

```python
 | propagate_species(take_census: bool = True, narrate: bool = True)
```

Creates families and propagates next generation of polymers.

**Arguments**:

  take_census (bool):
  If true, generation information saved
  
  narrate (bool):
  If true narration message occur

<a name="polygod.PolyNation.score_and_emigrate"></a>

#### score\_and\_emigrate

```python
 | score_and_emigrate(narrate: bool = True)
```

Assesses fitness of polymers and emigrates them.

Also fingerprints and runs property prediction.

**Arguments**:

  narrate (bool):
  If true narration message occur

<a name="polygod.PolyNation.take_census"></a>

#### take\_census

```python
 | take_census()
```

Take census of population (save data)

<a name="polygod.parallelize"></a>

#### parallelize

```python
parallelize(df, fingerprint_function, predict_function, models)
```

Parallelize the running of fingerprinting and property prediction.

**Arguments**:

  df (pd.DataFrame):
  Polymers to fingerprint and predict on
  

**Returns**:

  dataframe with all generated polymers

