# polyga: Background
## Tutorial Navigation:
- [Home](../README.md)
- [Background](ga.md)
- polyga

## polyga
First, some basic information about polyga's origin:

1. It was designed to predict hypothetical polymers

2. It was commonly integrated with machine learning models to assess fitness 
functions

3. It used single point crossover

4. It used elite selection

5. The mutation operator selected a random number of chromosome and changed them
to new random chromosomes

These are the basic points about the original implementation of polyga. The 
new implementation has some additions added:

1. The user can specify the dna and design scheme to make use of the basic
algorithm while also being able to do more advanced research for their specific
task

2. The user can generate islands with unique fitness functions, mutation rates,
etc... then populate those islands with nations that have different selection
schemes, family sizes, etc... This allows for two things:

    1. Migration can occur between nations, allowing the user to create niches of
desireable traits and then improve the properties of more complex fitness
functions by having these niche polymers migrate to the more complex land.

    2. Users can run experiments with different hyperparameters concurently
and assess their effects.

3. Additional selection schemes are implemented as seen in the docs.

The reason I designed the algorithm to have planets, lands, and nations is
mostly for fun. I thought it would gamify the reseach process, making it 
more enjoyable. Not that research isn't fun, but why not try to make it more 
fun?

With that being said, each of these objects serves a purpose.

#### 1. Planets

These serve as your repository for all the polymers you create. An sqlite
database in created that will store all information about the polymers (where
they're from, their properties, their fingerprints, etc...) and the planet
faciltiates migration between nations.

#### 2. Lands

These influence how your polymers will evolve, with each land having a unique 
fitness function. In my head, I imagine this is because each land has different
environmental factors that influence the evolution of the animals, just like
on Earth.

#### 3. Nations

This is where most of the work occurs. Different nations have different 
migration patterns, acceptance of foreigners, mating rituals, etc... Again, just
like in real life.

If you want to understand better, you can feel free to read the code or the 
docs.
