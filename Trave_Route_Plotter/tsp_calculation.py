# Python3 program to implement traveling salesman
# problem using naive approach.
from sys import maxsize





def travellingSalesmanProblem(matrix: list, start_point: int, round_trip: bool):
    # store all vertex apart from source and end vertex
    vertex = []
    vertex_len = len(matrix)

    if not round_trip:
        vertex_len -= 1

    for i in range(vertex_len):
        if i != start_point:
            vertex.append(i)

            # store minimum weight Hamiltonian Cycle
    min_path = [-1]
    min_path_cost = maxsize

    while True:
        # store current Path weight(cost)
        current_pathweight = 0

        # compute current path weight
        k = start_point
        for i in range(len(vertex)):
            current_pathweight += matrix[k][vertex[i]]
            k = vertex[i]

        if round_trip:
            current_pathweight += matrix[k][start_point]
        else:
            current_pathweight += matrix[k][vertex_len]

        # update minimum
        if current_pathweight < min_path_cost:
            min_path_cost = current_pathweight
            min_path = [0] + vertex



        if not next_permutation(vertex):
            break

    if round_trip:
        min_path.append(0)
    else:
        min_path.append(vertex_len)

    return min_path_cost, min_path


def next_permutation(L):
    n = len(L)

    i = n - 2
    while i >= 0 and L[i] >= L[i + 1]:
        i -= 1

    if i == -1:
        return False

    j = i + 1
    while j < n and L[j] > L[i]:
        j += 1
    j -= 1

    L[i], L[j] = L[j], L[i]

    left = i + 1
    right = n - 1

    while left < right:
        L[left], L[right] = L[right], L[left]
        left += 1
        right -= 1

    return True



if __name__ == "__main__":
    # matrix representation of graph
    graph = [[0, 10, 15, 20],
             [10, 0, 35, 25],
             [15, 35, 0, 30],
             [20, 25, 30, 0]]
    s = 0
    print(travellingSalesmanProblem(graph, s, True))