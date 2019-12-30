# Assignment 4

Shujun Liu (username: liushuj)

The "nearest" (code in "train" and "test") uses "correlation distance" from scipy.spatial as the distance metric and k=20. I tested several different metrics under different k's and this combination gives the best accuracy, although Euclidean distance can be speeded up using techniques like kd-tree.
The test results are as follows (although strictly some of them are not "distance" for they don't satisfy the triangle inequality) :

|                | k=1    | k=5    | k=20   | k=50   | k=100  | k=200  |
|----------------|--------|--------|--------|--------|--------|--------|
| braycurtis     | 68.61% | 70.0%  | 70.84% | 72.11% | 70.62% | 70.94% |
| canberra       | 67.02% | 69.14% | 68.93% | 71.16% | 71.37% | 71.16% |
| chebyshev      | 61.72% | 66.91% | 69.14% | 71.47% | 70.84% | 71.79% |
| Manhattan      | 67.97% | 69.67% | 70.41% | 70.63% | 71.05% | 70.31% |
| correlation    | 69.14% | 72.32% | 72.43% | 71.37% | 71.05% | 70.52% |
| cosine         | 68.82% | 71.79% | 72.00% | 71.69% | 70.84% | 71.47% |
| Euclidean      | 67.23% | 69.14% | 70.52% | 71.26% | 70.31% | 71.26% |
| Minkowski, p=3 | 65.96% |        | 70.52% | 71.37% | 71.05% | 71.69% |
| dice           | 61.82% | 61.19% | 63.41% | 64.79% | 66.6%  | 67.23% |
| hamming        | 47.72% | 54.61% | 57.69% | 63.52% | 65.01% | 67.02% |
| kulsinski      | 62.25% | 61.19% | 63.52% | 64.69% | 66.81% | 67.34% |

The program can run very slowly (~20min on the given dataset).



For "tree" the program randomly chooses tree_feats pairs of pixels and use their difference as the features; at the same time, randomly chooses n_samples samples to build a tree using Information Gain. This procedure is repeated n_trees times, and at the end all the trees vote for the classification result.
While the approach is affected by randomness, generally under same n_samples and n_feats, the more trees I use, the better the accuracy is; under same n_trees and n_samples, the more feature I use, the better the accuracy is.


For "nnet" a simple network with one input, one hidden layer, and one output is trained using back propagation.
