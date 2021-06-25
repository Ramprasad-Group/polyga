# PolyGA
PolyGA is an improved version of the genetic algorithm code written by
Chiho Kim. This version of the code uses the object oriented paradigm
to run the genetic algorithm. The user creates a
PolyPlanet with various PolyLands that each have their own environmental factors
(mutation rate, crossover rate, fitness function), and PolyNations that
have their own cultural factors (selection scheme, genetic preference, mating
rituals). Combined, these environmental and culutral factors influence the
evolution of your polymers.
PolyPlanet keeps track of the PolyLands and PolyNations 
and facilitates migration between nations.

## Intall
If you run into any issues, post an issue in the "Issues" tab on the github
source code page.

### pip install
1. `pip install git+https://github.com/jdkern11/polyga.git`

### Anaconda install
1. `run "conda create -n polyga python=3.7"` 
2. run "conda activate polyga"
3. `pip install git+https://github.com/jdkern11/polyga.git`



## Tutorials
1. [Introduction](tutorials/introduction.md)
2. [Analyzing your runs](tutorials/accessing_old_runs.md)
3. [Example fitness functions](tutorials/example_fitness_functions.md)

## Author
Joseph Kern (jkern34@gatech.edu)

## FAQ
### Why don't you save the fitness score of polymers?
Typically, fitness scores are population and land dependent, 
meaning a polymer will have a
different score in different populations. I do not want the user to mistakingly
sort polymers from different nations with the fitness score they acquire on 
their land, as the comparison is not accurate.

### Why do I have to pass my own generative, prediction, and fingerprinting functions?
I wanted to generalize the code so other users could change how they generate
the species, predict on them and run fingerprinting.

### Why do I have to pass my own fitness function?
There are so many possible fitness functions one could use, it just
doesn't make sense to hard code them into the model. 
I can provide examples for you to use, however.

### Why save into an sql database?
This database is easy to import with pandas, takes up less space than a million
csv files, and can quickly save and load data.

### How come when I load the sql database, the chromosome list is a string?
SQL can't easily store a list in a database. I made the choice to store the list
as a string, as it is easy to reconvert it back to a list from a string. TODO
add explanation of how to.

### Why have "lands" and "nations" and "planets"?
I wanted to replicate the way evolution occurs in nature. I thought it would be
more fun to implement with the idea that the land you are in can affect
a species' evolution, and the nation they live in can affect culture. For
instance, people living in Australia have higher rates of skin cancer (mutation
rate), and people in the U.S. are (typically) very punctual (culture).

### How do I know which chromosomes are which?
If you create your own dna list, you should keep access to it and refer back
to that for which chromosome\_id corresponds with which chromosome. Else,
the default dna list will have the list of all chromosomes.
Minnesota originally (selection scheme).

## References
1. Chiho Kim, R. Batra, L. Chen, H. Tran, and R. Ramprasad, 
“Polymer design using genetic algorithm and machine learning,” 
Computational Materials Science, vol. 186, p. 110067, Jan. 2021, 
doi: 10.1016/j.commatsci.2020.110067. ` Documentation:
