import numpy as np
import random
import math

## TODO: Implement this function
##
## Input:
##  - dmat (np.array): symmetric array of distances
##  - K (int): Number of clusters
##
## Output:
##   (np.array): initialize by choosing random number of points as medioids
def random_init(dmat, K):
    num_vertices = dmat.shape[0]
    medioids = np.array(random.sample(range(0, num_vertices), K))
    return medioids


## TODO: Implement this function
##
## Input:
##   - dmat (np.array): symmetric array of distances
##   - medioids (np.array): indices of current medioids
##
## Output:
##   - (np.array): assignment of each point to nearest medioid
def assign(dmat, medioids):
    num_vertices = dmat.shape[0]
    assignments = []

    # for every vertex
    for x in range(num_vertices):

        # calculate distance to every mediod
        d = [dmat[x][medioids[k]] ** 2 for k, _ in enumerate(medioids)]

        # closest cluster has minimum distance
        # if there are two matching minimum distances, choose the mediod who's vertex number is larger
        if d.count(min(d)) > 1:
            idx = d.index(min(d))  # index of first instance
            d[idx] = math.inf
            idx2 = d.index(min(d))  # index of second instance
            m = max(medioids[idx], medioids[idx2])  # choose larger mediod
        else:
            m = medioids[d.index(min(d))]

        # assign the vertex to this cluster
        assignments.append(m)
    return assignments


## TODO: Implement this function
##
## Input:
##   - dmat (np.array): symmetric array of distances
##   - assignment (np.array): cluster assignment for each point
##   - K (int): number of clusters
##
## Output:
##   (np.array): indices of selected medioids
def get_medioids(dmat, assignment, K):

    # get unique medioids from assignment matrix
    medioids = np.unique(assignment)

    return medioids


## TODO: Finish implementing this function
##
## Input:
##   - dmat (np.array): symmetric array of distances
##   - K (int): number of clusters
##   - niter (int): maximum number of iterations
##
## Output:
##   - (np.array): assignment of each point to cluster
def kmedioids(dmat, K, niter=10):
    num_vertices = dmat.shape[0]

    # we're checking for convergence by seeing if medioids
    # don't change so set some value to compare to
    old_medioids = np.full((K), np.inf, dtype=np.int)
    medioids = random_init(dmat, K)

    # this is here to define the variable before the loop
    assignment = np.full((num_vertices), np.inf)

    it = 0
    while np.any(old_medioids != medioids) and it < niter:
        it += 1
        old_medioids = medioids

        assignment = assign(dmat, medioids)
        medioids = get_medioids(dmat, assignment, K)
        print(old_medioids, medioids)
    return assignment
