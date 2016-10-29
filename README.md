# Strongly_Connected_Components
Code to find Strongly Connected Components in a huge graph.

Uses Kosaraju's Algorithm.

## Constraints:
So I have a vm which has about 1G memory and 1 core. 
This would have been easy if I reconfigured the vm to have more memory, but I decided to take up the challenge.

First thing to note is if I keep all the node information in memory I will run out of memory very fast.

To manage memory better I first I wrote an n-way merge-sort to sort the SCC.txt file in 2 ways.

1. Reverse order: sorted in increasing order of the second column. This will give us the degree when the graph is reversed.

2. Forward direction: sorted in increasing order of the first column. This will give us the degree when the graph is not-reversed. Sorting takes about a minute each.

I then wrote a class that will use binary search to find an entry in the sorted files using file seek. 
Binary search gives me O(log n) time to search directly from file (not RAM) as the files are already sorted. 
I wrote an LRU cache on top of this with limited number of cache entries to speed things up a bit using a dictionary. 
This way I avoid bringing all the data into memory.

Recursive DFS was causing a segmentation fault (python stack frames seem to be huge) 
so wrote the iterative version of DFS using a dictionary to check for seen nodes. 
This dictionary eats a LOT of memory but allows me O(1) lookup time while lists became unbearably slow around 10000 nodes.

## Inputs:
SCC.txt is the input huge graph with about 870000 nodes numbered 1,2,3...
The format is 
A B
where A and B are node numbers and this line means there is a directed edge from A to B

## Note on Kosaraju's Algorithm:
(DFS: Depth first search)
1. Reverse the arcs of the graph
2. run DFS over all nodes scoring each completed node in increasing order.
3. make the arcs once again point in the correct direction
4. run DFS over all nodes in the decreasing order of score calculated in [1]
5. Each run of DFS will uncover an SCC

In this code we just calculate the lengths of the SCCs and list the top 5 in decreasing order of size.
