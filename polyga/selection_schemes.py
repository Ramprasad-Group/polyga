"""Script for polymer different selection schemes"""
from typing import Dict
import pandas as pd
import numpy as np

def elite(population: pd.DataFrame, 
        num_parents_per_nationality: Dict[str, int]) -> pd.DataFrame:
    """Selects parents of next generation based on elitism.
   
    Args:  
        population (pd.DataFrame):  
            Current population dataframe.  
        num_parents_per_nationality (Dict[str, int]):  
            Dictionary indicating how many parents should come from each nation.

    Returns:  
        df (pd.DataFrame):  
            Parents of next generation. 
    """
    df = pd.DataFrame()
    national_origins = np.unique(population['birth_nation'])
    for nation in national_origins:
        tdf = population.loc[population['birth_nation'] == nation]
        tdf = tdf.nlargest(num_parents_per_nationality[nation], 'fitness')
        df = df.append(tdf)

    return df

def random(population: pd.DataFrame, 
        num_parents_per_nationality: Dict[str, int]) -> pd.DataFrame:
    """Selects parents of next generation randomly
   
    Args:  
        population (pd.DataFrame):  
            Current population dataframe.  
        num_parents_per_nationality (Dict[str, int]):  
            Dictionary indicating how many parents should come from each nation.

    Returns:  
        df (pd.DataFrame):  
            Parents of next generation. 
    """
    df = pd.DataFrame()
    national_origins = np.unique(population['birth_nation'])
    for nation in national_origins:
        tdf = population.loc[population['birth_nation'] == nation]
        # TODO see effect of setting random state
        tdf = tdf.sample(n=num_parents_per_nationality[nation], 
                random_state=123)
        df = df.append(tdf)

    return df
