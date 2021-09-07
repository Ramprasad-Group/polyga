from collections import defaultdict
import json
import os
import sqlite3

import pandas as pd

def str_to_list(string):
    """remove [] and whitespace, then create list of integers to return"""
    string = string[1:-1].replace(' ', '').split(',')
    return [int(str_id) for str_id in string]

def load_planet(planet: str) -> (pd.DataFrame, pd.DataFrame):
    """Loads planetary database and returns pandas dataframe

    Converts properties json string to columns of property values and 
    converts fingerprint column to a separate dataframe indexed by the 
    planetary_id.

    Args:  
        planet(str):  
            Planet name (full or relative path of it).

    Returns:  
        df (pd.DataFrame):  
            Dataframe of polymers and their properties.  
        fp_df (pd.DataFrame):  
            Dataframe of polymer fingerprints, indexed by planetary_id.
    """
    conn = sqlite3.connect(os.path.join(planet, 
        'planetary_database.sqlite')
    )
    query = "SELECT * FROM polymer"
    df = pd.read_sql(query, conn)
    cols = df.columns
    df_dict = defaultdict(list)
    fp_list = []
    for index, row in df.iterrows():
        for col in cols:
            if col == 'properties':
                props = json.loads(row[col])
                for key, value in props.items():
                    df_dict[key].append(value)
            elif col == 'fingerprint':
                fp = json.loads(row[col])
                fp['planetary_id'] = row['planetary_id']
                fp_list.append(fp.copy())
            elif col == 'str_chromosome_ids':
                df_dict['chromosome_ids'].append(str_to_list(row[col]))
            else:
                df_dict[col].append(row[col])
    df = pd.DataFrame.from_dict(df_dict)
    fp_df = pd.DataFrame(fp_list)
    fp_df = fp_df.set_index(keys=['planetary_id'])
    return df, fp_df

