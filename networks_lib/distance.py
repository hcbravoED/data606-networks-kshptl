import numpy as np
from collections import deque

# TODO: Implement this function
##
# input:
# mat (np.array): adjacency matrix for graph
##
# returns:
# (np.array): distance matrix
##
# Note: You can assume input matrix is binary, square and symmetric
# Your output should be square and symmetric


def bfs_distance(mat):
    num_vertices = mat.shape[0]
    res = np.full((num_vertices, num_vertices), np.inf)

    # Finish this loop
    for i in range(num_vertices):

        # initialize deque
        Q = deque()

        # initialize visited vector
        visited = np.full((num_vertices), False)

        # set diagonal elements to distance of 0
        np.fill_diagonal(res, 0)

        # set first vertex in queue and set as visited
        Q.append([i, 0])
        visited[i] = True

        # run through network while there are still vertices left in the queue
        while Q:
            # current reference distance
            distance = Q[0][1]

            # determine adjacent vertices
            adj_vert = np.where(mat[Q[0][0]] > 0)[0]

            # run if there exists any adjacent vertices
            if adj_vert.any():

                # filter out vertices that have already been visited
                adj_vert = [vert for vert in adj_vert if visited[vert] == False]

                # add adjacent vertices to queue and set them as visited
                [Q.append([vert, distance + 1]) for vert in adj_vert]
                np.put(visited, adj_vert, True)

                # record the distance to the vertices
                np.put(res[i], adj_vert, distance + 1)

                # remove current vertex from queue
                Q.popleft()

    return res


# TODO: Implement this function
##
# input:
# mat (np.array): adjacency matrix for graph
##
# returns:
# (list of np.array): list of components
##
# Note: You can assume input matrix is binary, square and symmetric
# Your output should be square and symmetric


def get_components(mat):
    dist_mat = bfs_distance(mat)
    num_vertices = mat.shape[0]
    available = [True for _ in range(num_vertices)]

    components = []

    # finish this loop
    while any(available):

        # get the current node
        current_node = available.index(True)

        # get components for this node
        components.append(np.where(dist_mat[current_node] < np.inf)[0].tolist())

        # finished using this node
        available[current_node] = False

    # filter only unique components
    components = np.unique(components)

    return components
