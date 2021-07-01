# polyga
polyga is a genetic algorithm written in Python and designed to create new 
polymers, although, it is implemented it in such a way that it can be a 
framework for other design tasks. The user creates a
PolyPlanet with various PolyLands that have unique environments and PolyNations that
have unique cultures. Combined, these environmental and culutral factors
influence the evolution of your polymers. PolyPlanet keeps track of the 
PolyLands and PolyNations and facilitates migration between nations.

## Intall
If you run into any issues, post an issue in the "Issues" tab on the github
source code page.

### pip install
`pip install git+https://github.com/jdkern11/polyga.git`  
or  
`pip install git+ssh://git@github.com:jdkern11/polyga.git`

### Anaconda install
1. `conda create -n polyga python=3.7` 
2. `conda activate polyga`
3. [Run pip install](#pip-install)



## Basic Tutorials
1. [Running polyga](tutorials/basic/basic.md)
2. [Analyzing polyga run](tutorials/basic/analyzing.md) 
3. [Prediction of properties](tutorials/basic/predict.md)
4. [Fingerprinting function](tutorials/basic/fingerprinting.md)
5. [Creating fitness functions](tutorials/basic/fitness.md)

## Advanced Tutorials
1. [How the DNA list works](tutorials/dna.md)
2. [Making a generative function](tutorials/generative.md)

## Background
1. [Genetic Algorithms](background/ga.md)
2. [polyga](background/polyga.md)

## Author
Joseph Kern (jkern34@gatech.edu)  
### Author of original GA
Chiho Kim (chiho80@gmail.com)


## FAQ
### I think you should add a cool new feature, can you?
Sure, you can either email me with your idea or write it up in a separate
branch and request it be merged.

### I am getting an error, what do I do?
Please create a new issue on github and I will get to it as soon as I can!

### Why don't you save the fitness score of polymers?
Typically, fitness scores are population and land dependent, 
meaning a polymer will have a
different score in different populations. I do not want the user to mistakingly
sort polymers from different nations with the fitness score they acquire on 
their land, as the comparison is not accurate.

### Why do I have to pass my own generative, prediction, and fingerprinting functions?
I wanted to generalize the code so other users could change how they generate
the species, predict on them and run fingerprinting. However, I have added 
tutorials to showcase how I originally intended the algorithm to run.

### Why do I have to pass my own fitness function?
There are so many possible fitness functions one could use, it just
doesn't make sense to hard code them into the model. 
I do provide examples for you to use, however.

### Why save into an sql database?
This database is easy to import with pandas and can be saved during runtime.

### Why are there multiple tables for fingerprints?
Sqlite sets a maximum of 2000 columns per table. This is a compile time 
constant, so even though I could find a way to increase it, I felt it would make
general usage of the code harder. Thus, if you have more than 1999 fingerprints
per object (with 1 column for indices), you will have more fingerprint tables.

fingerprint tables are named 'fingerprints\_T#' with number being the number
of the table (i.e., T1, T2...). If you know you have less than 1999 
fingerprints, the only table will be 'fingerprints\_T1

To determine how many fingerprint tables you have you can use the following
code:
```Python
import sqlite3
my_database = 'path/to/my/database.sqlite'
conn = sqlite3.connect(my_database)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
fingerprint_tables = []
for i in range(len(tables)):
    if i != 0:
        table = tables[i][0]
        fingerprint_tables.append(table)
```

### Why is the sql database taking so long to load?
This could be because you've generated a lot of polymers. I've found it can
take a minute or two to load when I have over 100,000 polymers. 

### Why is the chromosome list a string when I load the database?
SQL can't easily store a list in a database. I made the choice to store the list
as a string, as it is easy to reconvert it back to a list from a string. To do
so you can run the following code:
```Python
import os
import sqlite3

import pandas as pd

save_loc = os.path.join('path', 'to', 'my', 'planetary_database.sqlite')
conn = sqlite3.connect(save_loc)
query = "SELECT * FROM planetary_database"
df = pd.read_sql(query, conn)
conn.close()

def str_to_list(string):
    """remove [] and whitespace, then create list of integers to return"""
    string = string[1:-1].replace(' ', '').split(',')
    return [int(str_id) for str_id in string]

df['chromosome_ids'] = [str_to_list(str_ids) for str_ids 
                        in df.str_chromosome_ids]

```

### Why have "lands" and "nations" and "planets"?
I wanted to replicate the way evolution occurs in nature. I thought it would be
more fun to implement with the idea that the land you are in can affect
a species' evolution, and the nation they live in can affect culture. For
instance, people living in Australia typically have higher rates of skin cancer 
(mutation rate), and people in the U.S. are (typically) monogamous 
(number of parents in a family). 

### How do I know which chromosomes are which?
If you create your own dna list, you should keep access to it and refer back
to that for which chromosome\_id corresponds with which chromosome. Else,
the default dna list will have the list of all chromosomes.

## References
1. Chiho Kim, R. Batra, L. Chen, H. Tran, and R. Ramprasad, 
“Polymer design using genetic algorithm and machine learning,” 
Computational Materials Science, vol. 186, p. 110067, Jan. 2021, 
doi: 10.1016/j.commatsci.2020.110067. ` Documentation:
