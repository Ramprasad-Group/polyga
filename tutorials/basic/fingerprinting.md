# Basic tutorials
## Navigation
- [Front Page](../../README.md)
- [Running polyga](basic.md)
- [Analyzing polyga run](analyzing.md) 
- [Prediction of properties](predict.md)
- Fingerprinting function
- [Creating fitness functions](fitness.md)
- [(OPTIONAL) tutorial background](background.md)

## Fingerprinting functions
Fingerprints are lists of numbers that can uniquely identify an object. For 
instance, most humans could be quantified as having two legs, two arms, one
head, two eyes, etc... which might be useful in helping a model distinguish
between a human from a spider. Similarily, we can do the same thing for 
polymers.

Once again, open 'silly\_utils.py' in the 'examples' folder (see
[Running polyga](basic.md) for information on the folder setup), and see the
following code:
```Python
import pickle
import os
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
    fp_headers = [col for col in fp_df.columns if 'fp_' in col]
    return fp_df, fp_headers
```

The first thing to note it that polyga will always pass a dataframe to your
fingerprinting function with the smiles string of the polymer in it.
```Python
def silly_fingerprint(df):
    """Morgan fingerprint with count of chars in smiles_string.
        
    I wouldn't use this for actual research.

    Args:
        df (pd.DataFrame):
            dataframe of polyga population

    Returns:
        same dataframe with fingerprints attached
    """
```

For our case here, we want to save all the data in a dictionary of lists
(including old data). We start going through each row of the dataframe, 
finding the smiles\_string of the polymer, and converting it to and rdkit
molecule.
```Python
    fp_dict = defaultdict(list)
    columns = df.columns
    for index, row in df.iterrows():
        try:
            smiles = row['smiles_string']
            # These are used for ladder polymers, so we have to remove them
            # or we get a parsing error
            smiles = smiles.replace('e','*').replace('t','*').replace('d','*').replace('g','*')
            m = Chem.MolFromSmiles(smiles)
```

Now we take that molecule and run an rdkit fingerprinting scheme called the 
Morgan fingerprint. This will create 2048 columns with a 1 or 0 depending
on the structure of the polymer. Then we add an additional fingerprint based
on the number of characters in the smiles string.
```Python
            # Make radius 5 so we have unique fingerprints
            fp = AllChem.GetMorganFingerprintAsBitVect(m, 5, nBits=2048)
            arr = np.zeros((0,), dtype=np.int8)
            DataStructs.ConvertToNumpyArray(fp,arr)
            # Add fake fingerprint to differentiate repeats
            fp_dict['fp_' + 'num_str_atoms'].append(len(smiles))
```
This is why we call it a silly\_fingerprint. For one, bit based morgan fps
tend to create repeat vectors, meaning each polymer won't be distinct (which
is generally a requirement for a strong fingerprint). Secondly,
there is little physical meaning to the number of chars in the smiles name, 
meaning it does not accurately represent each polymer. As such, I would be 
shocked if this fingerprint scheme was ever useful. With that being said, it
was easy to make for this example, hence why I used it.

Finaally, we save all of the data for this row in the dictionary lists, turn
the dictionary into a pandas dataframe, and return the dataframe and list of
headers.
```Python
            for i in range(len(arr)):
                fp_dict['fp_' + str(i)].append(arr[i])
            for col in columns:
                fp_dict[col].append(row[col])
        except Exception as e:
            # Skip failed fingerprinting
            continue
    
    fp_df = pd.DataFrame.from_dict(fp_dict)
    fp_headers = [col for col in fp_df.columns if 'fp_' in col]
    return fp_df, fp_headers
```

To summarize steps one needs to take to create a fingerprinting function:
1. We created a function that takes in the polyga child dataframe
2. We looked at each smiles and created a unique rdkit fingerprint
3. We saved the original columns in the dataframe and the new fingerprints
4. We returned this new dataframe **and the fingerprint headers**

Each of this steps must be taken when creating a fingerprinting function. Let's
move on to the final section of the basic tutorial, [creating fitness 
functions](fitness.md).
