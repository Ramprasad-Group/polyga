import pytest

import pandas as pd

from polyga import selection_schemes
import numpy as np

def test_elite():
    df = pd.DataFrame()
    df['id'] = [1, 2, 3, 4, 5]
    df['birth_nation'] = ['one', 'one', 'two', 'two', 'two']
    df['fitness'] = [50, 100, 1, 2, 3]
    num_parents_per_nationality = {'one': 1, 'two': 2}
    elite = selection_schemes.elite(df, num_parents_per_nationality)
    for id in [2, 4, 5]:
        assert id in elite.id.to_list()
    for id in [1, 3]:
        assert id not in elite.id.to_list()
        
def test_random():
    df = pd.DataFrame()
    df['id'] = [1, 2, 3, 4, 5]
    df['birth_nation'] = ['one', 'one', 'two', 'two', 'two']
    df['fitness'] = [50, 100, 1, 2, 3]
    num_parents_per_nationality = {'one': 1, 'two': 2}
    parents = selection_schemes.random(df, num_parents_per_nationality)
    for id in [2, 3, 4]:
        assert id in parents.id.to_list()
    for id in [1, 5]:
        assert id not in parents.id.to_list()
