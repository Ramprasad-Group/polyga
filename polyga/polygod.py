"""PolyGod contains PolyPlanet, PolyLand, and PolyNation classes"""
from typing import Dict, Union
import os
import sys
import gc
from time import time
import sqlite3
import math
from multiprocessing import Pool

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from numpy.random import default_rng
from scipy.special import comb

from polyga.models import Polymer
from polyga.selection_schemes import elite

class PolyPlanet:
    """PolyPlanet contains the PolyLands and PolyNations of the world. 

    PolyPlanet keeps track of polymer emigration patterns, dna lists, and 
    some other information.

    Attributes:

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
    """
    def __init__(self, name: str,
                 predict_function: callable,
                 fingerprint_function: callable,
                 models: dict = None,
                 num_cpus: int = 1,
                 random_seed : int = 0,
                 path_to_dna : str = None,
                 save_folder: str = None):
        """Initialize planet
          
        Args:

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
        """
        self.global_cols = ['planetary_id', 'parent_1_id', 
                'parent_2_id', 'is_parent', 'num_chromosomes', 'smiles_string',
                'land', 'nation', 'planet', 'str_chromosome_ids', 'generation',
                'birth_planet', 'birth_land', 'birth_nation', 'chromosome_ids',
                'fitness', 'immigration_loc']
        self.name = name
        self.predict_function = predict_function
        self.fingerprint_function = fingerprint_function
        self.models = models
        self.age = 0
        self.num_cpus = num_cpus
        cores_on_comp = os.cpu_count()
        if self.num_cpus > cores_on_comp:
            self.num_cpus = cores_on_comp
            warning = ("Tried {} cpus, but only {}".format(num_cpus, 
                cores_on_comp) + " exist on this device. Using {}.".format(
                cores_on_comp)
            )
            logging.warning(warning)
        elif self.num_cpus < 1:
            logging.warning('Need at least one core. Setting to one')
        self.num_citizens = 0
        self.num_nations = 0
        self.lands = []
        self.emigration_list = []
        self.random_seed = random_seed
        # set random seed
        if self.random_seed != 0:
            self.rng = default_rng(seed=random_seed)
        else:
            self.rng = default_rng()

        if path_to_dna == None:
            path_to_dna = os.path.join(
                              os.path.dirname(os.path.realpath(__file__)),
                              'default_files',
                              'dna.csv'
                                      )
        self.dna = pd.read_csv(path_to_dna)
        # chromosomes with one connection will not work in polymers, so we
        # drop them.
        self.dna = self.dna[self.dna.num_connections >= 2]
        self.chromosomes = {row['chromosome_id']: row['chromosome'] for
                            index, row in self.dna.iterrows()}
        if save_folder != None:
            self.save_folder = os.path.join(save_folder, self.name)
        else:
            self.save_folder = os.path.join(os.getcwd(), self.name)
        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder)

        self.database = os.path.join(self.save_folder, 
                                     'planetary_database.sqlite')
        self.__initialize_database()
        

    def add(self, land: 'PolyLand'):
        """Add reference to lands on the planet"""
        self.lands.append(land)

    def advance_time(self, take_census: bool = True, narrate: bool = True):
        """Runs through generation of genetic algorithm on all the lands

        First fingerprints, predicts properties of, and scores all polymers.
        Then creates emigration list of emigrating polymers. Then 
        immigrates polymers to new nation. Finally, breeds polymers and saves.

        Args:

            take_census (bool):  
                If true, generation information saved

            narrate (bool):  
                if true narration message occur
        """
        if narrate:
            print("Age of planet {}: {}".format(self.name, self.age))
        self.age += 1
        for land in self.lands:
            land.score_and_emigrate(narrate)
        if len(self.emigration_list) != 0:
            self.immigrate()        
            # Clear emigration list
            self.emigration_list = []
        for land in self.lands:
            land.propagate_nations(take_census, narrate)
        gc.collect()

    def complete_run(self):
        """Close database connection"""
        self.session.close()
        print("Planet {} passes into oblivion...".format(self.name))

    def immigrate(self):
        """Immigrates polymers in emigration list"""
        df = pd.DataFrame()
        for emigration_df in self.emigration_list:
            df = df.append(emigration_df)
        df = df.fillna(0) 
        nation_names = []
        for land in self.lands:
            for nation in land.nations:
                nation_names.append(nation.name)
        immigration_locs = df['immigration_loc'].values
        for i in range(len(immigration_locs)):
            loc = immigration_locs[i]
            birth_nation = df.iloc[i].birth_nation
            if loc == 'random':
                new_loc = birth_nation
                # Don't want to immigrate back home
                while new_loc == birth_nation:
                    new_loc = self.rng.choice(nation_names,
                                              size=1,
                                              replace=False
                                             )
                immigration_locs[i] = new_loc
            elif loc not in nation_names:
                print("Error, {} not a nation. Cannot immigrate there".format(
                       loc))
                sys.exit()
        df['immigration_loc'] = immigration_locs
        for land in self.lands:
            for nation in land.nations:
                name = nation.name
                temp_df = df.loc[df.immigration_loc == name]
                if len(temp_df) != 0:
                    nation.population = nation.population.append(
                                                                  temp_df
                                                                ).fillna(0)

    def random_seed(self):
        """Returns random generator seed or None if seed is 0"""
        if self.random_seed == 0:
            return None
        else:
            return self.random_seed

    def remove(self, land: 'PolyLand'):
        """Remove reference to the land on the planet"""
        if land in self.lands:
            self.lands.remove(land)

    def num_lands(self):
        """Returns number of lands on the planet"""
        return len(self.lands)

    def take_census(self):
        """Saves all population data of nations in folder (planets name)"""
        for land in self.lands:
            land.take_census()

    def uid(self):
        """Returns unique id for a new polymer and increases number of citizens.
          

        Note, uid = 0 means parent of polymer was none
        """
        self.num_citizens += 1
        return self.num_citizens

    def __initialize_database(self):
        """Initialize database."""
        engine = create_engine(f"sqlite:///{self.database}")
        Polymer.__table__.create(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()



class PolyLand:
    """PolyLand contains various PolyNations. 

    It's environment determines how polymers mutate and what features ensure 
    their survival.
    
    Attributes:

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
    """
    def __init__(self, name: str, planet: PolyPlanet, 
                 generative_function: callable,
                 fitness_function: callable,
                 crossover_position: str = 'relative_center',
                 crossover_sigma_offset: float = 0.3,
                 fraction_mutation: float = 0.2,
                 mutation_sigma_offset: float = 0.25,
                 fraction_mutate_additional_block: float = 0.05,
                 generative_function_parameters: dict = {}
                 ):
        self.name = name
        self.age = 0
        self.fitness_function = fitness_function
        self.generative_function = generative_function
        self.generative_function_parameters = generative_function_parameters
        self.planet = planet
        self.planet.add(self)
        self.nations = []
        self.crossover_position = crossover_position
        self.crossover_sigma_offset = crossover_sigma_offset
        self.fraction_mutation = fraction_mutation
        self.mutation_sigma_offset = mutation_sigma_offset
        self.fraction_mutate_additional_block = fraction_mutate_additional_block
        # TODO implement
        self.land_chromosomes = list(self.planet.chromosomes.keys())

    def add(self, nation: 'PolyNation'):
        """Add refence to nations on the land"""
        self.nations.append(nation)
        self.planet.num_nations += 1

    def propagate_nations(self, take_census: bool = True, narrate: bool = True):
        """Generates families and propagates next generation of all nations.

        Args:

            take_census (bool):  
                If true, generation information saved

            narrate (bool):  
                If true narration message occur
        """
        if narrate:
            print("Age of land {} is {}".format(self.name, self.age))
        self.age += 1
        for nation in self.nations:
            nation.propagate_species(take_census, narrate)

    def genetic_information(self):
        """Returns how the environment affects the genes of polymers in this land

        e.g., returns mutation and crossover information

        Returns (tuple):   
            (fraction_mutation, mutation_sigma_offset,
             fraction_mutate_additional_block, crossover_position,
             crossover_sigma_offset)
        """
        return (self.fraction_mutation, self.mutation_sigma_offset,
                self.fraction_mutate_additional_block, self.crossover_position,
                self.crossover_sigma_offset)

    def num_nations(self):
        """Returns number of nations on the land"""
        return len(self.nations)

    def remove(self, nation: 'PolyNation'):
        """Remove reference to the nation on the land if nation exists on land"""
        if nation in self.nations:
            self.nation.remove(nation)
    
    def score_and_emigrate(self, narrate):
        """Assesses fitness scores of polymers and emigrates them.

        Where fingerprinting and property prediction occurs.

        Args:

            narrate (bool):  
                If true narration message occur
        """
        for nation in self.nations:
            nation.score_and_emigrate(narrate)
    
    def take_census(self):
        """Saves all populations data in land"""
        for nation in self.nations:
            nation.take_census()


class PolyNation:
    """PolyNation is where population changes occur. 

    They are influenced by their PolyLand.

    Attributes:

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
            callable representing how polymers in this nation choose
            to mate. See polyga.selection_schemes for more details.
            Default is elite.

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
    """
    def __init__(self, name: str, land: PolyLand, 
                 initial_population_file: str = None,
                 initial_population: pd.DataFrame = None,
                 num_population_initial: int = 180,
                 num_chromosomes_initial: int = 4,
                 num_families: int = 15, 
                 num_parents_per_family: int = 3,
                 num_children_per_family: int = 12,
                 selection_scheme: callable = elite,
                 partner_selection: str = 'diversity',
                 emigration_rate: float  = 0.1,
                 emigration_selection: str = 'best_worst',
                 parent_migrant_percentage: float = 0.1,
                 immigration_pattern: dict = {},
                 random_seed: int = 0):
        """Intialize nation.

        Args:

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

            selection_scheme (callable):  
                callable representing how polymers in this nation choose
                to mate. See polyga.selection_schemes for more details.
                Default is elite.

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
        """
        self.name = name
        self.land = land
        self.selection_scheme = selection_scheme
        self.partner_selection = partner_selection
        self.land.add(self)
        self.random_seed = random_seed
        # set random seed
        if self.random_seed != 0:
            self.rng = default_rng(seed=random_seed)
        else:
            self.rng = default_rng()
        self.num_parents_per_family = num_parents_per_family
        self.num_children_per_family = num_children_per_family
        self.num_families = num_families
        if emigration_rate > 0.5:
            print('Emigration rate was {}, switched to 0.5'.format(
                  emigration_rate))
            emigration_rate = 0.5
        if emigration_rate < 0:
            print('Emigration rate was {}, switched to 0'.format(
                  emigration_rate))
            emigration_rate = 0
        self.emigration_rate = emigration_rate
        self.emigration_selection = emigration_selection
        if parent_migrant_percentage > 1:
            print('migrant parent percentage was {}, switched to 1'.format(
                  parent_migrant_percentage))
            parent_migrant_percentage = 1
        if parent_migrant_percentage < 0:
            print('migrant parent percentage was {}, switched to 0'.format(
                  parent_migrant_percentage))
            parent_migrant_percentage = 0
        self.parent_migrant_percentage = parent_migrant_percentage
        self.immigration_pattern = immigration_pattern
        if len(self.immigration_pattern) != 0:
            tot_percent = 0
            for val in self.immigration_pattern.values():
                tot_percent += val 
            if tot_percent > 1:
                for key in self.immigration_pattern:
                    self.immigration_pattern[key] /= tot_percent
        self.generation = 0
        if initial_population:
            self.population = initial_population
        elif initial_population_file:
            self.population = self.__load_population(initial_population_file)
        else:
            self.population = self.__generate_random_population(
                                                num_population_initial,
                                                num_chromosomes_initial
                                                               ) 

    def family_demographics(self):
        """Returns demographics of family (number of parents and children)"""
        return (self.num_parents_per_family, 
                self.num_children_per_family)

    def print_generation(self):
        print(self.generation)

    def propagate_species(self, take_census: bool = True, narrate: bool = True):
        """Creates families and propagates next generation of polymers.

        Args:  
            take_census (bool):  
                If true, generation information saved

            narrate (bool):  
                If true narration message occur
        """
        if narrate:
            print("{} of {} advances through time".format(self.name,
                                                      self.land.name))
        # Reassess fitness here due to emigration.
        st = time()
        self.population = self.land.fitness_function(self.population.copy(),
                self.__fp_headers)
        if narrate:
            print('The polymers of {} worked for {} polyears.'.format(
               self.name, round((time() - st), 4))) 
        st = time()
        families = self.__selection()
        if narrate:
            print('The polymers of {} married!'.format(self.name)) 
        # Take census here so we know if polymer is selected as parent
        st = time()
        if take_census:
            self.take_census()
        if narrate:
            print('The nation of {} took {} polyyears to finish their census!'.format(
               self.name, round((time() - st), 4))) 
            print('There are {} polymers in the nation'.format(
               len(self.population)))
        st = time()
        children, parents = self.__crossover(families)
        children = [self.__mutate(child) for child in children]
        if narrate:
            print('After {} polyears, they had children.'.format(
                   round((time() - st), 4))) 
        self.population = self.__log_births(children, parents)
        print("Generation {} of {} have all passed away".format(self.generation,
                                                      self.name))
        self.generation += 1

    def score_and_emigrate(self, narrate: bool = True):
        """Assesses fitness of polymers and emigrates them.

        Also fingerprints and runs property prediction.

        Args:
            narrate (bool):
                If true narration message occur
        """
        st = time()
        if self.land.planet.num_cpus == 1:
            self.population, self.__fp_headers = (
                    self.land.planet.fingerprint_function(self.population.copy())
            )
            if narrate:
                print('The polymers of {} took {} polyyears to mature.'.format(
                   self.name, round((time() - st), 4))) 
            st = time()
            self.population = (
                    self.land.planet.predict_function(self.population.copy(),
                        self.__fp_headers, self.land.planet.models)
            )
            if narrate:
                print('The polymers of {} took {} polyyears to graduate college.'.format(
                   self.name, round((time() - st), 4))) 
        elif self.land.planet.num_cpus > 1:
            st = time()
            split_df = np.array_split(self.population.copy(), 
                    self.land.planet.num_cpus)
            # Can't pass method, need to pass function, so we must pass
            # models and appropriate functions as parameters
            iterables = []
            for i in range(self.land.planet.num_cpus):
                iterable = (split_df[i], self.land.planet.fingerprint_function,
                        self.land.planet.predict_function, 
                        self.land.planet.models)
                iterables.append(iterable)
            pool = Pool(self.land.planet.num_cpus)
            return_dfs_and_headers = pool.starmap(parallelize, iterables)
            pool.close()
            pool.join()
            valid_dfs = []
            valid_headers = []
            # Join returned dfs and headers
            for return_df_and_header in return_dfs_and_headers:
                if return_df_and_header[0] is not None:
                    valid_dfs.append(return_df_and_header[0])
                    valid_headers.extend(return_df_and_header[1])

            self.population = pd.concat(valid_dfs).fillna(0)
            self.__fp_headers = list(set(valid_headers))

            if narrate:
                print('The polymers of {} took {} polyyears to grow up.'.format(
                   self.name, round((time() - st), 4))) 
        else:
            logging.critical('num_cpus to use must be >= 1')
            sys.exit()
        st = time()
        self.population = self.land.fitness_function(self.population.copy(),
                self.__fp_headers)
        if narrate:
            print('The polymers of {} worked for {} polyyears.'.format(
               self.name, round((time() - st), 4))) 
        # skip emigration if no other nations exist
        if self.land.planet.num_nations > 1:
            st = time()
            self.__emigrate()
            if narrate:
                print('The polymers of {} emigrated over {} polyyears.'.format(
                   self.name, round((time() - st), 4))) 
        else:
            print("No other nations exist for the polymers of ", end="")
            print("{} to immigrate to".format(self.name))

    def take_census(self):
        """Take census of population (save data)"""
        # Save in folder planet_name/nation_name
        self.population['generation'] = self.generation
        self.population['nation'] = self.name
        self.population['land'] = self.land.name
        self.population['planet'] = self.land.planet.name
        self.population['str_chromosome_ids'] = [str(ids) for ids in 
                                     self.population['chromosome_ids'].values]
        # Drop zero columns
        self.population = self.population.loc[:, (self.population != 0).any(
            axis=0)]
        # Readd zero columns if global ones removed
        for col in self.land.planet.global_cols:
            if col not in self.population.columns:
                self.population[col] = 0
        self.__fp_headers = [col for col in self.population.columns if col in 
                self.__fp_headers]
        # Can't add lists to database and don't want to save fitness or 
        # immigration location
        property_cols = [col for col in self.population.columns if col not 
                in self.__fp_headers and col 
                not in self.land.planet.global_cols]
        
        for index, row in self.population.iterrows():
            fingerprint = row[self.__fp_headers].to_dict()
            properties = row[property_cols].to_dict()
            polymer = Polymer(planetary_id=row['planetary_id'],
                    parent_1_id=row['parent_1_id'], 
                    parent_2_id=row['parent_2_id'], 
                    is_parent=row['is_parent'], 
                    num_chromosomes = row['num_chromosomes'],
                    smiles_string = row['smiles_string'], 
                    birth_land = row['birth_land'], 
                    birth_nation = row['birth_nation'], 
                    birth_planet = row['birth_planet'],
                    str_chromosome_ids = row['str_chromosome_ids'], 
                    generation = row['generation'], 
                    settled_planet = row['planet'], 
                    settled_land = row['land'], 
                    settled_nation = row['nation'], 
                    fingerprint = fingerprint,
                    properties = properties)
            self.land.planet.session.add(polymer)
        self.land.planet.session.commit()

    def __crossover(self, families):
        """Performs crossover on polymers and returns resulting chromosome_id
           lists for mutation

        Polymers will mate until number_children_per_family is met. 
        Mating will occur between parent pairs sequentially [0, 1] -> [0, 2]
        -> [0, 3] -> [1, 2] -> etc... and then cycle back. 
        Half chosen per parent will be random, but if one combination
        already exists, it will be thrown out, unless number of children
        per family > combination(parents, 2)*4. This scheme is not perfect,
        as the first parent will be oversamples, but if diverse choice
        is used, this parent will have the highest fitness score of the
        three.

        Args:  
            families (list):   
                list of lists of polymer family parents
                
        Returns:  
            all_child_chromosome_ids (list):  
                List of lists of child choromosome ids.

            all_parents (list):  
                List of lists of all parent planetary ids in same index order 
                as all_child_chromosome_ids.
        """
        all_child_chromosome_ids = []
        all_parents = []
        for family in families: 
            
            parent_combinations = comb(len(family), 2)
            chromosome_ids_of_children = []
            df_of_parents = (
              self.population.loc[self.population['planetary_id'].isin(family)]
                            )
            chromosome_ids_of_parents = df_of_parents['chromosome_ids'].values
            planetary_ids_of_parents = df_of_parents['planetary_id'].values
            crossover_pos = []
            for chromosome_ids in chromosome_ids_of_parents:
                if self.land.crossover_position == 'relative_center':
                    pos = round(self.rng.normal(
                                            int(len(chromosome_ids)/2),
                                            self.land.crossover_sigma_offset
                                               )
                               )

                elif self.land.crossover_position == 'center':
                    pos = int(len(chromosome_ids)/2) 

                elif self.land.crossover_position == 'random':
                    # Want to segment so each half has at least one chromosome
                    pos = self.rng.integers(1, len(chromosome_ids)-1)
                else:
                    print('Choose a valid crossover position. '
                          + '{} invalid.'.format(
                          self.land.crossover_position))
                    sys.exit()
                # Want to segment so each half has at least one chromosome
                if pos < 1:
                    pos = 1
                if pos >= len(chromosome_ids):
                    pos = len(chromosome_ids)-1
                crossover_pos.append(pos) 
            parent1 = 0
            parent2 = 0
            # Try to find unique children, but if there are five repeats
            # consecutively, just add the repeat
            repeat_children = 0
            while (len(chromosome_ids_of_children) 
                   < self.num_children_per_family):
                parent2 += 1
                if parent2 == len(family):
                    parent1 += 1
                    parent2 = parent1 + 1
                if parent1 == len(family)-1:
                    parent1 = 0
                    parent2 = 1

                # Assume [1, 2, 3, 4] == [3, 4, 1, 2]
                if self.rng.random() < 0.5:
                    child_chromosome_ids = (
                    chromosome_ids_of_parents[parent1][:crossover_pos[parent1]]
                                           )
                else:
                    child_chromosome_ids = (
                    chromosome_ids_of_parents[parent1][crossover_pos[parent1]:]
                                           )
                if self.rng.random() < 0.5:
                    p2_half = (
                    chromosome_ids_of_parents[parent2][:crossover_pos[parent2]]
                              )
                else:
                    p2_half = (
                    chromosome_ids_of_parents[parent2][crossover_pos[parent2]:]
                              )
                child_chromosome_ids.extend(p2_half)
                if (self.num_children_per_family > parent_combinations * 4 or
                   repeat_children > 5): 
                    chromosome_ids_of_children.append(child_chromosome_ids)
                    all_parents.append(
                                        [
                                          planetary_ids_of_parents[parent1],
                                          planetary_ids_of_parents[parent2]
                                        ] 
                                      )
                else:
                    if child_chromosome_ids not in chromosome_ids_of_children:
                        chromosome_ids_of_children.append(child_chromosome_ids)
                        all_parents.append(
                                            [
                                              planetary_ids_of_parents[parent1],
                                              planetary_ids_of_parents[parent2]
                                            ] 
                                          )
                        repeat_children = 0
                    else:
                        repeat_children += 1
            for child_ids in chromosome_ids_of_children:
                all_child_chromosome_ids.append(child_ids)
        return all_child_chromosome_ids, all_parents

    def __emigrate(self):
        """Polymers in nation emigrate according to emigration parameters"""
        if self.emigration_selection == 'random':
            to_emigrate = self.population.sample(frac=self.emigration_rate,
                                                replace=False)
        elif self.emigration_selection == 'elite':
            n = round(len(self.population) * self.emigration_rate) 
            to_emigrate = self.population.nlargest(n, 'fitness')
        elif self.emigration_selection == 'best_worst':
            num_parents = self.num_parents_per_family * self.num_families
            n = round(len(self.population) * self.emigration_rate) 
            parents = self.population.nlargest(num_parents, 'fitness')
            pop_no_parents = self.population[~self.population.isin(parents)
                                            ].dropna()
            to_emigrate = pop_no_parents.nlargest(n, 'fitness')
        self.population = self.population[~self.population.isin(to_emigrate)
                                         ].dropna()
        immigration_loc = ['random']*len(to_emigrate)
        # Randomly choose where each polymer is sent, but number to send to
        # each place is user defined
        if len(self.immigration_pattern) != 0:
            tot_percent = 0
            for val in self.immigration_pattern.values():
                tot_percent += val
            indices = [x for x in range(len(to_emigrate))]
            num_to_change = round(tot_percent * len(to_emigrate))
            indices_to_change = self.rng.choice(indices,
                                                size=num_to_change,
                                                replace=False
                                               )
            index = 0
            for key, val in self.immigration_pattern.items():
                n_to_mutate = round(val * len(to_emigrate))
                for i in range(n_to_mutate):
                    immigration_loc[indices_to_change[index]] = key
                    index += 1
        to_emigrate['immigration_loc'] = immigration_loc
        if len(to_emigrate) != 0:
            self.land.planet.emigration_list.append(to_emigrate)


    def __generate_random_population(self, num_population_initial, 
                                     num_chromosomes_initial):
        """Generates random population of polymers
          
        Args:
            num_population_initial (int):  
                int representing number of polymers to 
                randomly generate

            num_chromosomes_initial (int):   
                int representing number of blocks each 
                randomly generated polymer has
        
        Returns (pd.DataFrame):  
            Pandas dataframe of population
        """
        population = []
        for i in range(num_population_initial):         
            polymer_chromosomes_ids = list(self.rng.choice(
                                           self.land.land_chromosomes,
                                           size=num_chromosomes_initial))
            smiles = self.land.generative_function(polymer_chromosomes_ids, 
                    self.land.planet.chromosomes, self.rng, 
                    **self.land.generative_function_parameters) 
            if smiles == None or smiles == '':
                continue
            else:
                population.append(
                                  {
                               'chromosome_ids': polymer_chromosomes_ids,
                               'num_chromosomes': len(polymer_chromosomes_ids),
                               'planetary_id': self.land.planet.uid(),
                               'parent_1_id': 0,
                               'parent_2_id': 0,
                               'smiles_string': smiles,
                               'birth_land': self.land.name,
                               'birth_nation': self.name,
                               'birth_planet': self.land.planet.name
                                  }
                                 )
        return pd.DataFrame(population)


    
    def __load_population(self, initial_population_file):
        """Loads pandas dataframe from csv file containing initial population"""
        return pd.read_csv(initial_population_file)

    def __log_births(self, children, parents):
        """Logs details of the birth of the new children and returns population

        Args:  
            children (list):  
                list of children chromosome ids

            parents (list):  
                list of pairs parents and their planetary_ids.
        """
        population = []
        for i in range(len(children)):
            child = children[i]
            parent1 = parents[i][0]
            parent2 = parents[i][1]
            smiles = self.land.generative_function(child, 
                        self.land.planet.chromosomes, self.rng,
                        **self.land.generative_function_parameters) 
            if smiles == None or smiles == '':
                continue
            else:
                population.append(
                                  {
                               'chromosome_ids': child,
                               'num_chromosomes': len(child),
                               'planetary_id': self.land.planet.uid(),
                               'parent_1_id': parent1,
                               'parent_2_id': parent2,
                               'smiles_string': smiles,
                               'birth_land': self.land.name,
                               'birth_nation': self.name,
                               'birth_planet': self.land.planet.name
                                  }
                                 )
        return pd.DataFrame(population)


    def __mating(self, df):
        """Returns list of planetary ids of parent groups.

        Polymers that can't find a mate die.
        """
        # Families should be chosen by uid
        families = []
        df = df.sort_values(by='fitness', ascending=False)
        # Set id = planetary_id so we can drop rows by index
        df['id'] = df['planetary_id']
        df = df.set_index('id')
        if self.partner_selection == 'diversity':
            while len(df) > 0: 
                for index, row in df.iterrows():
                    fp1 = row[self.__fp_headers]
                    family = [row['planetary_id']]
                    similarities = {}
                    for index2, row2 in df.iterrows():
                        if index != index2:
                            fp2 = row2[self.__fp_headers]
                            score = self.__tanimoto_similarity(fp1, fp2)
                            # error check
                            if score == -1:
                                continue
                            if score < 0.5: 
                                family.append(row2['planetary_id'])
                                if len(family) == self.num_parents_per_family:
                                    break
                            else:
                                similarities[row2['planetary_id']] = score         
                    if len(family) < self.num_parents_per_family:
                        num_to_add = self.num_parents_per_family - len(family)
                        for i in range(num_to_add):
                            if len(similarities) == 0:
                                break
                            uid = min(similarities, key=similarities.get) 
                            # Don't want to grab a second time
                            similarities.pop(uid, None)
                            family.append(uid) 
                    if len(family) != 1:
                        families.append(family)
                    df = df.drop(index=family)
                    break
                        
        elif self.partner_selection == 'random':
            while len(df) > 0:
                if len(df) < self.num_parents_per_family:
                    family = df.planetary_id.values
                else:
                    family = df.sample(n=self.num_parents_per_family)[
                                'planetary_id'].values
                if len(family) != 1:
                    families.append(family)
                df = df.drop(index=family)
                                            
        else:
            print("Please choose a valid selection scheme. {} invalid.".format(
                    self.partner_selection))
            sys.exit()
            
        return families


    def __mutate(self, chromosome_ids):
        """Mutates some chromosomes in the list of chromosome ids

        Args:  
            chromosome_ids (list): 
                list of chromosomes

        Returns:  
            chromosome list of chromosomes with some mutations
        """
        num_to_mutate = round(self.rng.normal(
                             len(chromosome_ids) * self.land.fraction_mutation,
                             self.land.mutation_sigma_offset
                                                         )
                             )
        if num_to_mutate > len(chromosome_ids):
            num_to_mutate = len(chromosome_ids)
        # Avoid error from negative numbers.
        if num_to_mutate > 0:
            indices = [x for x in range(len(chromosome_ids))]
            indices_to_mutate = list(self.rng.choice(indices,
                                                     size=num_to_mutate,
                                                     replace=False
                                                    )
                                    )
            mutations = list(self.rng.choice(
                                         self.land.land_chromosomes,
                                         size=num_to_mutate
                                            )
                            )
            for i in range(num_to_mutate):
                chromosome_ids[indices_to_mutate[i]] = mutations[i]
        if self.rng.random() < self.land.fraction_mutate_additional_block: 
            mutation = self.rng.choice(
                                       self.land.land_chromosomes,
                                       size=1
                                      )
            chromosome_ids.append(mutation[0])
        return chromosome_ids


    def __selection(self):
        """Returns families based on selection scheme and partner scheme.

        If num_families*num_parents_per_family more than max available, all
        polymers will be mated.
        """
        num_parents = self.num_families * self.num_parents_per_family
        national_origins = np.unique(self.population['birth_nation'])
        num_parents_per_nationality = {}
        # Will subtract number from each other nation
        num_migrant_parents = round(num_parents
                                   * self.parent_migrant_percentage)
        num_parents_per_nationality[self.name] = (num_parents  
                                                  - num_migrant_parents)
        # Don't try to find migrants if none exist or if none mandatory.
        if (len(national_origins) != 1 
            or self.parent_migrant_percentage == 0):
            # Count number of migrants per foreign nation
            num_migrants_per_nation = {}
            for nation in national_origins:
                if nation != self.name:
                    tdf = self.population.loc[self.population[
                                                      'birth_nation'
                                                              ] == nation]
                    num_migrants_per_nation[nation] = len(tdf)
                    num_parents_per_nationality[nation] = 0
            # Evenly distribute parents per each nation until 
            # num_migrant_parents met or no more migrants exist.
            tot_num_migrant_parents = 0
            while tot_num_migrant_parents != num_migrant_parents:
                no_more_migrants = True
                for nation in num_migrants_per_nation:
                    if num_migrants_per_nation[nation] > 0:
                        num_migrants_per_nation[nation] -= 1
                        num_parents_per_nationality[nation] += 1 
                        tot_num_migrant_parents += 1
                        no_more_migrants = False
                    if tot_num_migrant_parents == num_migrant_parents:
                        break
                if no_more_migrants:
                    break
        if (num_parents > len(self.population)):
            df = self.population.copy()
        else: 
            df = self.selection_scheme(self.population.copy(), 
                    num_parents_per_nationality)

        families = self.__mating(df)
        # Save who is parent
        is_parent = []
        all_parent_planetary_ids = [x for l in families for x in l] 
        for index, row in self.population.iterrows():
            if row['planetary_id'] in all_parent_planetary_ids:
                is_parent.append(True)
            else:
                is_parent.append(False)
        self.population['is_parent'] = is_parent
        return families
            


    def __tanimoto_similarity(self, x, y):
        """Returns tanimoto similarity score of polymers.

        Returns -1 if division by zero occurs.
        """
        numerator = np.dot(x,y)
        denominator = np.dot(x,x) + np.dot(y,y) - np.dot(x,y)
        if denominator == 0:
            return -1
        tanimoto_similarity=np.dot(x,y)/(np.dot(x,x)+np.dot(y,y)-np.dot(x,y))
        return tanimoto_similarity

def parallelize(df, fingerprint_function, predict_function, models):
    """Parallelize the running of fingerprinting and property prediction.

    Args:
        df (pd.DataFrame):  
            Polymers to fingerprint and predict on

    Returns:  
        dataframe with all generated polymers
    """
    fingerprint_df, fp_headers = fingerprint_function(df)

    # If all polymers dropped, we just want to return None
    if len(fingerprint_df) == 0:
        return [None, None]

    prediction_df = predict_function(fingerprint_df, fp_headers, models)

    return [prediction_df, fp_headers]
