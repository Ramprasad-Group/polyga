# polyga: Background
## Tutorial Navigation:
- [Home](../README.md)
- Background
- [Analyzing your runs](accessing_old_runs.md)
- [Example fitness functions](example_fitness_functions.md)

## Background 
In this background I will explain two things: how genetic algorithms (GAs) work 
and how polyga is implemented. I feel you should understand some of the basics 
behind GAs first so you understand why people use them, and then I can explain 
how polyga is implemented and why it is implemented in this way.

If you already know a lot about GAs and only care about how polyga is 
implemented, see [polyga](#polyga).

### Genetic Algorithms
All genetic algorithms work based off the circle of life and Darwinian 
evolution.

![GA-Circle-Of-Life](../imgs/circle-of-life.png)

At the top of the circle is selection. This is where certain animals (bears in
this case) are selected to breed based on environmental (or cultural) factors.
In this case, global warming (an environmental factor) is causing temperatures 
to rise, killing our poor polar bears that are maladapted to warm environments. 
Thus, only brown bears breed during the next "crossover" phase.

In this phase, animals (or polymers) breed, exchanging genetic material and
creating new children, potentially more suited to the new environment. In 
nature, this crossover is of genes, but this it is different depending on
the design task. For instance, GAs can be used to tune hyperparameters of 
machine learning models, in which case the values of those 
hyperparameters are "crossed over" or mixed. For polymers, chemically unique 
blocks are crossed over (seen in the image below). The main point is, 
this crossing over generates a new child that may have the best (or worst) 
features of both parents.

![Polymer-Cross-Over](../imgs/crossover.png)

### polyga

In order to facilitate usage as a general algorithm as opposed to one 
specialized for polymers, it requires a small amount of work on your part. 
However, if you're like me, you really enjoy programming, so I think this will
be fun!

