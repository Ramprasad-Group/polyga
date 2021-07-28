# polyga: DNA
## Tutorial Navigation:
- [Home](../README.md)
- [Background](background.md)
- How the DNA list works
- [Making a generative function](generative.md)

## DNA
It is the basic building block of all of nature. So to, will it be the basic
building block of our algorithms. Here is what your dna list should look like

```
chromosome_id,chromosome,num_connections    
0,[Bi]C[Bi],2     
1,[Bi]CC([Bi])C,2    
2,[Bi]CC([Bi])CC,2     
3,[Bi]CC([Bi])CCC,2     
4,[Bi]CC([Bi])C(C)C,2  
```

That's it. It's a simple csv file with three headers. However, when combined 
with a generative function, a lot of use can come from these simple blocks
of dna. If you want, you can view the dna.csv list provided by the code
by looking in polyga/default\_files. Now, let's [learn about generative functions.](generative.md)

