# Basic tutorials
## Navigation
- [Front Page](../../README.md)
- [Running polyga](basic.md)
- [Analyzing polyga run](analyzing.md) 
- Prediction of properties
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
    
    for key in prop_values.keys():
        df[key] = prop_values[key]
    
    return df
```

This is a custom function I wrote to predict the properties, and would require
the following dependencies
```Python
from collections import defaultdict
import pandas as pd
```

Previously, we loaded the models which were located in the same 
folder the silly\_utils.py script is located in:
```Python
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
I loaded my models (I saved them as .pkl files) and save them
in a dictionary with the property name as the key and the model as the value.
This made it easy to access, but technically one could load the models in 
any way. Additionally, you could not pass any models, but you must have a model
parameter in the predict function, even if you don't use it.

Now, I create a dictionary of lists and predict all the properties for each
polymer. One **CRITICAL** thing to note is polyga will always pass a hard copy of
the child dataframe as the first parameter, fingerprint headers to the 
prediction function as the second, and models as the third (even if None):

```Python
    prop_values = defaultdict(list)
    for model in models:
        prop_values[model] = (
                models[model].predict(df[fp_headers].values).reshape(-1)
                )
```

```Python
def silly_property_prediction(df, fp_headers, models):
```
Hence, these three parameters in the created function.

Finally, we save all the property values to the original dataframe and
return it back to polyga.

```Python
    for key in prop_values.keys():
        df[key] = prop_values[key]
    
    return df
```

To summarize steps one would need to take to predict properties:
1. We defined a function where the first parameter was the child dataframe,
the second were the fingerprint headers in the dataframe, and the third was 
the dictionary of models
2. We opened our models, manually knowing where they were located in our
harddrive
3. We predicted the properties for each polymer and saved them in the original
dataframe
4. We **PASSED BACK** the original datafame + those properties added. It is 
critical you do this.

If you had your own models, you would write the code to import them and
make predictions yourself. Note, you don't technically need machine learning 
based models, this is just what I typically use.
Next is [go into how we created the fingerprints for the
models](fingerprinting.md).
