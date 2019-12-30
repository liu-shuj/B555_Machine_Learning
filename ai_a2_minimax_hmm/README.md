# Assignment 2
Shujun Liu(liushuj)


Part 1:

Inside ai_IJK.py is a simple implementation of alpha-beta pruning minimax algorithm.

Maximum depth is set to 6 and evaluation of a board is score(player)-score(opponent) where score is calculated by:
1. 2^(order of alphabet)-1, ensuring that a bigger letter scores more than two previous letters, eg. score('C') >2* score('B'), plus
2. a penalty of 2^(order of next alphabet)-1 if in opponent's turn there is a pair of adjacent uppercase and lowercase letters, 
or a reward of same value when it's player's turn.

Besides decision made by minimax, it acts aggressively by trying to merge opponent's tile whenever possible. 

The nondeterministic version actually uses the same algorithm but only setting depth to 0, making it a greedy strategy.

Part 2:

horizon1.py simply take the pixel with the most local contrast of each column as the pixel on the ridge.
Certainly it does not perform well when there are local contrast more than that of the ridge.

horizon2.py implements a (logarithmtic) Viterbi algorithm.
The emission probability is set to a value proportional to P(s|w) (because P(s|w) is proportional to P(w|s) according to Bayes' law), 
which is (edge_strength**2)/((edge_strength**2).sum(0)), squared to make brighter pixels on the contrast map more likely to be on the ridge.
As for the transition probability, I assume here that the difference of index of row of two neighboring pixels on the ridge to be of Gaussian(0,1.33) and transition probability of a row number to another is calculated according to CDF of this Gaussian distribution. Transition to a pixel of more than 12 pixels higher or lower is assumed impossible to speedup calculation.

However, it does not perform well when there are more than one ridge-like curve on an image:

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output.jpg?raw=true)

horizon3.py uses the same algorithm as horizon2.py but with human feedback(making emission probability at that pixel to be 100% and 0% for other pixels on the column), more weight is given to smoothness of the possible ridge by adding an multiplication to log of transition probability.
By adjusting the weight the algorithm seem to perform well for most of the 9 images when provided a pixel on the ridge. At the same time it can be seen that the algorithm acts differently when given different pixel.

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output1.jpg?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output2.jpg?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output4.jpg?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output5.jpg?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output6.jpg?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output7.jpg?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output8.jpg?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output9.jpg?raw=true)

Same picture, given (93,0):

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output3.jpg?raw=true)

Given (27,32):

![alt text](https://github.iu.edu/cs-b551-fa2019/liushuj-a2/blob/master/part2/output3_1.jpg?raw=true)
