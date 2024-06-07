import sys

# Function to find the vertex with the minimum distance value from the set of vertices
def minDistance(dist, sptSet):
    min_value = sys.maxsize
    min_index = -1

    # Traverse through all vertices
    for v in range(len(dist)):
        # Select the vertex if it's not in the shortest path tree (sptSet[v] is False)
        # and its distance value is less than the current minimum value
        if not sptSet[v] and dist[v] <= min_value:
            min_value = dist[v]
            min_index = v

    return min_index

# Function to recursively print the path from source to vertex j
def printPath(parent, j):
    if parent[j] == -1:
        return
    printPath(parent, parent[j])
    print(j, end=' ')

# Function to print the solution including distances and paths
def printSolution(dist, parent, src):
    print("Vertex \t Distance from Source \t Path")
    for i in range(len(dist)):
        print(f"{i}\t\t\t{dist[i]}\t\t\t", end='')
        printPath(parent, i)
        print(src)

# Dijkstra's algorithm implementation
def dijkstra(graph, src):
    V = len(graph)
    dist = [sys.maxsize] * V  # Initialize distances to infinity
    sptSet = [False] * V       # Initialize shortest path tree set to False
    parent = [-1] * V          # Initialize parent array to trace paths

    dist[src] = 0              # Distance from source to itself is 0

    # Finding shortest path for all vertices
    for _ in range(V - 1):
        u = minDistance(dist, sptSet)  # Pick the vertex with the minimum distance
        sptSet[u] = True                # Include the picked vertex in the shortest path tree set

        # Update distance values of adjacent vertices of the picked vertex
        for v in range(V):
            # Update dist[v] only if it's not in sptSet, there's an edge from u to v,
            # and the total weight of the path from src to v through u is less than current dist[v]
            if not sptSet[v] and graph[u][v] != 0 and dist[u] != sys.maxsize \
                    and dist[u] + graph[u][v] < dist[v]:
                dist[v] = dist[u] + graph[u][v]
                parent[v] = u

    # Print the constructed distance array and paths
    printSolution(dist, parent, src)

def main():
    V = int(input("Enter the number of nodes (up to 10): "))

    if V < 1 or V > 10:
        print("Invalid number of nodes. Please enter a number between 1 and 10.")
        return

    graph = []
    print("Enter the link costs (adjacency matrix) for the graph:")
    for _ in range(V):
        row = list(map(int, input().split()))
        graph.append(row)

    src = int(input(f"Enter the source node (0 to {V - 1}): "))

    if src < 0 or src >= V:
        print(f"Invalid source node. Please enter a node within the range (0 to {V - 1}).")
        return

    print(f"Shortest paths from source node {src}:")
    dijkstra(graph, src)

if __name__ == "__main__":
    main()
