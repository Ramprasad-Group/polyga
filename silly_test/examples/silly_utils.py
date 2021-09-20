from collections import defaultdict

import pandas as pd
import numpy as np
from rdkit.Chem import AllChem, DataStructs
from rdkit import Chem, RDLogger
# Turn off rdkit warnings
RDLogger.DisableLog('rdApp.*')
from sklearn.preprocessing import MinMaxScaler

def silly_fingerprint(df):
    """Morgan fingerprint with count of chars in smiles_string.
        
    I wouldn't use this for actual research.

    Args:
        df (pd.DataFrame):
            dataframe of polyga population

    Returns:
        same dataframe with fingerprints attached
    """
    fp_dict = defaultdict(list)
    columns = df.columns
    for index, row in df.iterrows():
        try:
            smiles = row['smiles_string']
            # These are used for ladder polymers, so we have to remove them
            # or we get a parsing error
            smiles = smiles.replace('e','*').replace('t','*').replace('d','*').replace('g','*')
            m = Chem.MolFromSmiles(smiles)
            # Make radius 5 so we have unique fingerprints
            fp = AllChem.GetMorganFingerprintAsBitVect(m, 5, nBits=2048)
            arr = np.zeros((0,), dtype=np.int8)
            DataStructs.ConvertToNumpyArray(fp,arr)
            # Add fake fingerprint to differentiate repeats
            fp_dict['fp_' + 'num_str_atoms'].append(len(smiles))
            for i in range(len(arr)):
                fp_dict['fp_' + str(i)].append(arr[i])
            for col in columns:
                fp_dict[col].append(row[col])
        except Exception as e:
            # Skip failed fingerprinting
            continue
    
    fp_df = pd.DataFrame.from_dict(fp_dict)
    keys = [key for key in fp_dict.keys()]
    for key in keys:
        del fp_dict[key]
    del keys
    del fp_dict

    fp_headers = [col for col in fp_df.columns if 'fp_' in col]
    return fp_df, fp_headers

def silly_property_prediction(df, fp_headers, models):
    """Predict silly properties of polymers

    Args:
        df (pd.DataFrame):
            dataframe of fingerprinted polymers
        fp_headers (list):
            list of fingerprint headers
        models (dict):
            Key is parameter name, value is the model

    Returns:
        same dataframe with predictions attached
    """
    prop_values = defaultdict(list)
    for model in models:
        prop_values[model] = (
                models[model].predict(df[fp_headers].values).reshape(-1)
                )
    
    keys = [key for key in prop_values.keys()]
    for key in keys:
        df[key] = prop_values[key].copy()
        del prop_values[key]
    del keys
    del prop_values 

    return df
    

def make_coolest_funniest_smartest_polymer(df, fp_headers):
    """Make the coolest fricken polymer around

    Args:
        df (pd.DataFrame):
            dataframe of population with properties predicted 

    Returns:
        Same dataframe with fitness function attached 
    """
    # Same names as returned property
    properties = [
                  'Polymer_Coolness',
                  'Polymer_Intelligence',
                  'Polymer_Funnyness'
                  ]

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
    return df

def make_funniest_polymer(df, fp_headers):
    """Score by funnyness only"""
    # Same names as returned property
    properties = [
                  'Polymer_Funnyness'
                  ]

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
    return df
