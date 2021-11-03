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
`pip install polyga`

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
6. [(OPTIONAL) tutorial background](background.md)

## Advanced Tutorials
1. [Loading manual first generation](tutorials/advanced/first_gen.md)

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

### Why is the sql database taking so long to load?
This could be because you've generated a lot of polymers. I've found it can
take a minute or two to load when I have over 100,000 polymers. 

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

### Why do some ids not show up even though they're in the DNA list?
If they only have one connection joint, they are automatically removed. This
prevents the removal of all connection joints.


## References
1. J. Kern, L. Chen, C. Kim, and R. Ramprasad, “Design of 
polymers for energy storage capacitors using machine 
learning and evolutionary algorithms,” J Mater Sci, 
Sep. 2021, doi: 10.1007/s10853-021-06520-x.

2. Chiho Kim, R. Batra, L. Chen, H. Tran, and R. Ramprasad, 
“Polymer design using genetic algorithm and machine learning,” 
Computational Materials Science, vol. 186, p. 110067, Jan. 2021, 
doi: 10.1016/j.commatsci.2020.110067.
