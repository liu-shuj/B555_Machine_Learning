Assignment 3

Shujun Liu (Username: liushuj)

Part 1:
The Simple algorithm simply counts which tag is attached to a word most times and choose that when meeting a new example. For words never appeared, it simply randomly chooses a tag. The posterior of the result can be calculated by multiply of all P(w|s)*P(s)'s because of independence of each subgraph.

The HMM algorithm needs two statistics from the training data: the probability of each word given a tag, as the emission probability; and the probability of transition of one state to another for each pair of state. Then the Viterbi algorithm could be used to find the most possible POS tagging and the posterior could be calculated by multiply of P(s0) and all P(s_i|s_i-1)*P(w_i|s_i).

The MCMC algorithm implementation is not finished. The idea should be that during sampling, each node not being the first and last node is sampled from P(s_i|s_i-1,s_i+1,w_i) which is proportional to P(s_i,s_i-1,s_i+1,w_i) and could be written as P(s_i|s_i-1)P(s_i+1|s_i)P(w_i|s_i) according to the structure of the Bayes net. These probabilities should be estimated using the training data. Besides, for the last node an additional probability P(s_n|s_1,s_n-1) should also be estimated and will be used when sampling such node.


Part 2:
When implementing the algorithm, besides P(w_i_j+1|w_i_j), the probability of each word starting with each letter and ending with letter is also approximated; each time only one of the two tables is randomly modified; 6 attempts are made during the breaking, 100 seconds each, and result with largest probability is outputted.


Part 3:
In the implementation, prior is set to 0.5; all letters are turned to lower case; all mails causing decoding error is considered spam; words not seen in the training set is just ignored.
This implementation reaches over 95% accuracyo on given data n my machine.
