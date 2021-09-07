<a name="analysis"></a>

# analysis

<a name="analysis.str_to_list"></a>

#### str\_to\_list

```python
str_to_list(string)
```

remove [] and whitespace, then create list of integers to return

<a name="analysis.load_planet"></a>

#### load\_planet

```python
load_planet(planet: str) -> (pd.DataFrame, pd.DataFrame)
```

Loads planetary database and returns pandas dataframe

Converts properties json string to columns of property values and
converts fingerprint column to a separate dataframe indexed by the
planetary_id.

**Arguments**:

  planet(str):
  Planet name (full or relative path of it).
  

**Returns**:

  df (pd.DataFrame):
  Dataframe of polymers and their properties.
  fp_df (pd.DataFrame):
  Dataframe of polymer fingerprints, indexed by planetary_id.

