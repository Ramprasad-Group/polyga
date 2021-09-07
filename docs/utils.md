<a name="utils"></a>

# utils

<a name="utils.longest_smiles"></a>

#### longest\_smiles

```python
longest_smiles(smiles)
```

Returns longest chain of polymer with more than two stars.

Done so only a linear chain is returned.

<a name="utils.chromosome_ids_to_smiles"></a>

#### chromosome\_ids\_to\_smiles

```python
chromosome_ids_to_smiles(chromosome_ids: list, chromosomes: dict, rng: default_rng, **kwargs) -> str
```

Combined chromosome ids to create new polymer smiles

Combines chromosomes sequentially according to index, but combines
joints randomly.

**Arguments**:

  chromosome_ids (list):
  list of chromosome ids
  chromosomes (dict):
  dict with key of chromosome id and value of the chromosome
  rng (default_rng):
  random number generator
  
  
  Returns (str):
  smiles string of combined chromosomes

