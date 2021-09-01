[README](../README.md)

Here we discuss some example fitness functions one can use to design polymers.
As stated previously, all models should be in your model folder as follows

```
.
+-- script.py
+-- models
|   +-- exp_Tg
|       +-- model.pkl
|   +-- exp_Eg
|       +-- model.pkl
|   +-- exp_Dk
|       +-- model.pkl
|   +-- exp_CED
|       +-- model.pkl
|   +-- exp_EIB
|       +-- model.pkl
```
Tg = glass transition temperature, Eg = bandgap, Dk = dielectric constant,
CED = coheisve energy density, EIB = Electron charge injection barrier

Now, this first example is a simple fitness function that attempts to find
the polymer with the highest glass transition temperature

```Python
import numpy as np
import pandas as pd
from sklearn import preprocessing
def single_property_fitness_function(df):
    """Encourage the evolution of polymers with glass transition temperatures of
       9999 K.

    All fitness functions must returns list with order unaltered
    """
    tgs = df.exp_Tg.values
    # Those with values closest to 9999 will have highest fitness score
    tgs = [9999 - abs(tg-9999) for tg in tgs]
    tgs = np.array(tgs)
    # Reshape for processing
    tgs = np.reshape(tgs,(len(tgs),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    tgs = scaler.fit_transform(tgs)
    tgs = [tg[0] for tg in tgs]
    return tgs
```

Once again, we return the list back with the score. This next function tries
to maximize bandgap and glass transition temperature. The score is based on an
equally weighted linear combination of the two values.

```Python
import numpy as np
import pandas as pd
from sklearn import preprocessing
def dual_property_fitness_function(df):
    """Encourage the evolution of polymers with glass transition temperatures of
       9999 K and bandgap of 9999 eV.

    All fitness functions must returns list with order unaltered
    """
    tgs = df.exp_Tg.values
    # Those with values closest to 9999 will have highest fitness score
    tgs = [9999 - abs(tg-9999) for tg in tgs]
    tgs = np.array(tgs)
    # Reshape for processing
    tgs = np.reshape(tgs,(len(tgs),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    tgs = scaler.fit_transform(tgs)

    egs = df.exp_Eg.values
    # Those with values closest to 9999 will have highest fitness score
    egs = [9999 - abs(eg-9999) for eg in egs]
    egs = np.array(egs)
    # Reshape for processing
    egs = np.reshape(egs,(len(egs),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    egs = scaler.fit_transform(egs)

    scores = []
    # Linear combination of values
    for i in range(len(tgs)):
        tg = tgs[i][0]
        eg = egs[i][0]
        score = 0.5*tg + 0.5*eg
        scores.append(score)

    return scores
```

This could be repeated for any number of feature combinations. I can also do
more complex functions. For instance, perhaps instead of maximizing a feature,
I just want to ensure 5 of my features are above a certain threshold. In that
case, I can create the following fitness function

```Python
import numpy as np
import pandas as pd
from sklearn import preprocessing
def multi_property_clamping_fitness_function(df):
    """Encourage the evolution of polymers with five property thresholds

    Tg > 500 K, Eg > 5 eV, CED < 80 cal/cc, Dk > 4, and EIB > 3 eV


    All fitness functions must returns list with order unaltered
    """
    tgs = df.exp_Tg.values
    # Those with values larger than 500 K will have highest fitness score
    tgs = [min(tg, 500) for tg in tgs]
    tgs = np.array(tgs)
    # Reshape for processing
    tgs = np.reshape(tgs,(len(tgs),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    tgs = scaler.fit_transform(tgs)

    egs = df.exp_Eg.values
    # Those with values larger than 5 eV will have highest fitness score
    egs = [min(eg, 5) for eg in egs]
    egs = np.array(egs)
    # Reshape for processing
    egs = np.reshape(egs,(len(egs),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    egs = scaler.fit_transform(egs)

    dks = df.exp_Dk.values
    # Those with values larger than 4 will have highest fitness score
    dks = [min(dk, 4) for dk in dks]
    dks = np.array(dks)
    # Reshape for processing
    dks = np.reshape(dks,(len(dks),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    dks = scaler.fit_transform(dks)

    ceds = df.exp_CED.values
    # Those with values less than 80 cal/cc will have highest fitness score
    ceds = [-1*max(ced, 80) for ced in ceds]
    ceds = np.array(ceds)
    # Reshape for processing
    ceds = np.reshape(ceds,(len(ceds),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    ceds = scaler.fit_transform(ceds)

    eibs = df.exp_EIB.values
    # Those with values larger than 3 eV will have highest fitness score
    eibs = [min(3, eib) for eib in eibs]
    eibs = np.array(eibs)
    # Reshape for processing
    eibs = np.reshape(eibs,(len(eibs),-1))
    scaler = preprocessing.MinMaxScaler()
    # Scale so all values between 0 and 1
    eibs = scaler.fit_transform(eibs)

    scores = []
    # Linear combination of values
    for i in range(len(tgs)):
        tg = tgs[i][0]
        eg = egs[i][0]
        ced = ceds[i][0]
        eib = eibs[i][0]
        dk = dks[i][0]

        score = 0.2*tg + 0.2*eg + 0.2*ced + 0.2*eib + 0.2*dk
        scores.append(score)

    return scores
```

That should give you a good enough idea for some fitness functions you can
create, but the sky is the limit. Just make sure the order of rows
is never altered.
