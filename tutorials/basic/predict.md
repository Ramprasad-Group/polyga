# Basic tutorials
## Navigation
- [Front Page](../../README.md)
- [Running polyga](basic.md)
- [Analyzing polyga run](analyzing.md) 
- [Prediction of properties](predict.md)
- [Fingerprinting function](fingerprinting.md)
- [Creating fitness functions](fitness.md)
- [(OPTIONAL) tutorial background](background.md)

## Prediction of properties
In this example, we are predicting some properties I made up. Granted, some
polymers are less cool than others (all plastics are trash for instance), but
that property isn't quantifiable.

I explain how I made the three models for this tutorial in the 
[tutorial background](background.md) which is optional reading (I mean, all of
this is optional, but the background is not relevant to understanding polyga), 
but I want to delve into how polyga interacts with these models further.

To understand, open 'silly\_utils.py' in the 'examples' folder (see
[Running polyga](basic.md) for information on the folder setup). In this file
is the following function:
```Python
def silly_property_prediction(df, fp_headers):
    """Predict silly properties of polymers

    Args:
        df (pd.DataFrame):
            dataframe of fingerprinted polymers
        fp_headers (list):
            list of fingerprint headers

    Returns:
        same dataframe with predictions attached
    """
    model_folder = os.path.dirname(os.path.realpath(__file__))
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

    prop_values = defaultdict(list)
    for model in models:
        prop_values[model] = (
                models[model].predict(df[fp_headers].values).reshape(-1)
                )
    
    for key in prop_values.keys():
        df[key] = prop_values[key]
    
    return df
```

This is a custom function I wrote to predict the properties, and would require
the following dependencies
```Python
import pickle
import os
from collections import defaultdict
import pandas as pd
```

To start, the function loads the models which I know are located in the same 
folder the silly\_utils.py script is located in:
```Python
    model_folder = os.path.dirname(os.path.realpath(__file__))
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
The first line here loads the path to silly\_utils.py and, by extension, all
my models. Next, I load my models (I saved them as .pkl files) and save them
in a dictionary with the property name as the key and the model as the value.

```Python
    prop_values = defaultdict(list)
    for model in models:
        prop_values[model] = (
                models[model].predict(df[fp_headers].values).reshape(-1)
                )
```

Now, I create a dictionary of lists and predict all the properties for each
polymer. One *CRITICAL* thing to note is polyga will always pass a hard copy of
the child dataframe as the first parameter and fingerprint headers to the 
prediction function as the second.

```Python
    for key in prop_values.keys():
        df[key] = prop_values[key]
    
    return df
```
Finally, we save all the property values to the original dataframe and
return it back to polyga.

To summarize:
1. We defined a function where the first parameter was the child dataframe and
the second were the fingerprint headers in the dataframe
2. We opened our models, manually knowing where they were located in our
harddrive
3. We predicted the properties for each polymer and saved them in the original
dataframe
4. We *PASSED BACK* the original datafame + those properties added. It is 
critical you do this.

If you had your own models, you would write the code to import them and
make predictions yourself. What we'll do next is [go into how we created these
fingerprints](fingerprinting.md).
