from networks_lib.betweenness import edge_betweenness
from networks_lib.distance import bfs_distance
from networks_lib.distance import get_components

import numpy as np
import math

## TODO: FINISH IMPLEMENTING THIS FUNCTION
##
## Find network communities using Girvan-Newman algorithm
##
## Input
##   - mat (np.array): graph adjacency network (n by n)
##   - K (int): number of communities to return
##
## Output
##   (list of int): list of community assignments for each vertex
##
## Note: Assume input matrix mat is binary and symmetric
def girvan_newman(mat, K):
    num_vertices = mat.shape[0]

    # make a copy of matrix since we are going
    # to update it as we remove edges
    work_mat = mat.copy()

    components = get_components(mat)

    # if only 1 component, get_components() returns a 1D list with all vertices....convert this to 2D list for while loop to work
    if isinstance(components[0], list):
        pass
    else:
        components = [components]

    while len(components) < K:
        # print(components)
        # compute edge betweenness (one component at a time)
        eb = np.zeros((num_vertices, num_vertices))
        for vertices in components:
            cur_mat = work_mat[vertices, :][:, vertices]
            cur_eb = edge_betweenness(cur_mat)
            for i in range(len(vertices)):
                eb[vertices[i], vertices] = cur_eb[i, :]

        # find location of maximum betweeness
        edge = np.where(eb == eb.max())

        # remove that edge
        work_mat[edge[0][0], edge[0][1]] = 0
        work_mat[edge[0][1], edge[0][0]] = 0

        # get new components
        components = get_components(work_mat)

        if isinstance(components[0], list):
            pass
        else:
            components = [components]
        # print(components)

    return components_to_assignment(components, num_vertices)


## Turn list of components to list of assignments
##
## Input:
##   - components (list of np.array): list of vertices in each community
##   - num_vertices (int): number of vertices in the graph
##
## Output:
##   (list of int): assignment for each vertex
def components_to_assignment(components, num_vertices):
    assign = np.full((num_vertices), np.nan)
    cur_label = 0
    for vertices in components:
        assign[vertices] = cur_label
        cur_label += 1
    return assign.tolist()
