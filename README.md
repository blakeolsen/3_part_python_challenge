# Programming Challenge
Author: Blake Olsen

### Dependencies
`python3 --version` == `Python 3.6.4`
`pip3 install -r requirements.txt`
### How To Run
run `./challenge{n}.sh -h` for each challenge to list details on how to run

## Challenge #1
For this challenge I used the Flask web framework to handle https requests. I implemented a Key Value Server adapter interface which I used a simple Dictionary to implement. This adapter could be extended to use any type of database to help with security/performance.

Performance Question: The biggest bottleneck will be DB lookup latency with large numbers of keys. By implementing the KVStore interface with a distributed database with issue can be mitigated. With a database implementation (instead of my local dictionary key store implementation) the Applet can be horizontally scaled to handle additional connection points. 
## Challenge #2
For this challenge I implemented a greedy algorithm to take advantage of the order of the elements. Since the items are ordered least to greatest we can ensure that items are not matched together twice. I partition the remaining available items (items[i:]) into n partitions. Where a partition is the a subset of all items. I then find the total cost of purchasing the first item in that list. I find the most money spent on items (staying below the gift card limit). We know that the we can spend the most money on some gift in that partition. So we repeat the process with that partition by partitioning it.

Note: I had a plan to implement parallelism through a thread pool. However I had difficulties implementing partial execution of functions (I would require a context switch after the "map" call of each batch however I was unable to implement that). Therefore it will automatically launch "number of items" ^ "number of gifts" threads to ensure there is no deadlock

Performance Question: BigO is still O((log(i))^g): i=number of items, g=number of gifts, since searching for the best item takes log(i) time, however we still need to perform this g times.

## Challenge #3

For this challenge I broke up the string into partitioned, generated all variations of that substring, then puts it all back together. This can be optimized with "--max_threads" and "--partition_size".

Performance Question: BigO is O(log n) where n is the number of items. 
