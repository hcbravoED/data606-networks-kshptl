import numpy as np
from collections import deque

## TODO: Implement this function
##
## Implements the breadth-first algorithm of Girvan-Newman to compute
##   number (fractional) of shortest paths starting from a given vertex
##   that go through each edge of the graph
##
## Input:
##   - vertex (int): index of vertex paths start from
##   - mat (np.array): n-by-n adjacency matrix
##
## Output:
##   (np.array): n-by-n edge count matrix
##
## Note: assume input adjacency matrix is binary and symmetric
def edge_counts(vertex, mat):
    num_vertices = mat.shape[0]
    paths_matrix = np.full(num_vertices, np.inf)
    edge_count = np.full((num_vertices, num_vertices), 0.0)

    Q = deque()
    leaf = []

    # initialize visited and layer vectors
    visited = np.full((num_vertices), False)
    layer = np.full((num_vertices), np.inf)

    # set first vertex in queue and set as visited
    Q.append([vertex, 1])
    visited[vertex] = True
    layer[vertex] = 1
    paths_matrix[vertex] = 1

    # run through network while there are still vertices left in the queue
    while Q:
        # current reference number of shortest paths
        path = Q[0][1]

        # determine adjacent vertices
        adj_vert = np.where(mat[Q[0][0]] > 0)[0]

        # filter out parent and sibling vertices
        adj_vert = [vert for vert in adj_vert if layer[vert] > layer[Q[0][0]]]

        # run if there exists any viable adjacent vertices
        if adj_vert:

            # record the number of shortest paths to the vertices and their layer
            for j in adj_vert:
                if paths_matrix[j] == np.inf:
                    np.put(paths_matrix, j, path)
                else:
                    np.put(paths_matrix, j, paths_matrix[j] + path)

            for k in adj_vert:
                layer[k] = layer[Q[0][0]] + 1

            # add adjacent vertices to queue and set them as visited
            [Q.append([vert, paths_matrix[vert]]) for vert in adj_vert]
            np.put(visited, adj_vert, True)

            # remove current vertex from queue
            Q.popleft()

        # if there is no viable adjacent vertex, set this vertex as a leaf
        else:
            leaf.append(Q[0][0])
            Q.popleft()

    ## calculate edge counts
    layer_copy = layer
    layer_copy = sorted(set(layer_copy), reverse=True)
    layer_copy.remove(layer_copy[0])

    # assign credit of 1 to each leaf
    credit = np.full(num_vertices, 1.0)
    # np.put(credit,leaf,1)

    # at each layer, except bottom-most one
    for j in layer_copy:

        # for every vertex that is in this layer
        for v, l in np.ndenumerate(layer):
            if l == j:

                # for every vertex in lower layer that is adjacent to this vertex
                for v_lower, l_lower in np.ndenumerate(layer):
                    if l_lower == l + 1 and mat[v][v_lower] == 1:
                        # divide shortest path count of current layer vertex (v) by that of the lower layer vertex (v_lower) multiply by the credit of the lower vertex.

                        # print('v=',v[0],'v_lower=',v_lower[0])
                        # print('v credit=',credit[v[0]],', v_lower credit=',credit[v_lower[0]])
                        # print('v path = ',paths_matrix[v], "v_lower path = ",paths_matrix[v_lower])

                        edge_credit = (
                            paths_matrix[v] / paths_matrix[v_lower]
                        ) * credit[v_lower[0]]

                        # add this edge credit the the appropriate place in edge_count matrix at both locations
                        edge_count[v][v_lower] = edge_credit
                        edge_count[v_lower][v] = edge_credit

                        # update credit recieved from each child vertex
                        credit[v[0]] += edge_count[v][v_lower]

                        # print("edge_count = ",edge_count[v][v_lower])
                        # print('----------------v credit =',credit[v[0]],"\n")
    return edge_count


## Compute edge betweeness for a graph
##
## Input:
##   - mat (np.array): n-by-n adjacency matrix.
##
## Output:
##   (np.array): n-by-n matrix of edge betweenness
##
## Notes: Input matrix is assumed binary and symmetric
def edge_betweenness(mat):
    res = np.zeros(mat.shape)
    num_vertices = mat.shape[0]
    for i in range(num_vertices):
        res += edge_counts(i, mat)
    return res / 2.0
