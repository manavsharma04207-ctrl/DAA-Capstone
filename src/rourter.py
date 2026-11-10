import heapq
import pandas as pd

def build_adjacency_list(graph_df):
    graph = {}
    for _, row in graph_df.iterrows():
        u, v, w = row['from_node'], row['to_node'], row['distance_km']
        if u not in graph: graph[u] = {}
        if v not in graph: graph[v] = {}
        graph[u][v] = w
        graph[v][u] = w  # Undirected graph
    return graph

def dijkstra(graph, start_node):
    """Computes shortest path distances from start_node to all other nodes."""
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    pq = [(0, start_node)]

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node]:
            continue
        for neighbor, weight in graph[curr_node].items():
            dist = curr_dist + weight
            if dist < distances[neighbor]:
                distances[neighbor] = dist
                heapq.heappush(pq, (dist, neighbor))

    return distances

def nearest_neighbor_tsp(graph, start_node, target_nodes):
    """TSP Nearest-Neighbor approximation algorithm."""
    unvisited = set(target_nodes)
    curr_node = start_node
    route = [curr_node]
    total_distance = 0

    while unvisited:
        distances = dijkstra(graph, curr_node)
        next_node = min(unvisited, key=lambda node: distances[node])
        total_distance += distances[next_node]
        route.append(next_node)
        unvisited.remove(next_node)
        curr_node = next_node

    # Return to depot
    return_dist = dijkstra(graph, curr_node)[start_node]
    route.append(start_node)
    total_distance += return_dist

    return route, total_distance

if __name__ == '__main__':
    try:
        df = pd.read_csv('../datasets/delivery_graph.csv')
    except:
        df = pd.read_csv('datasets/delivery_graph.csv')
    
    graph = build_adjacency_list(df)
    print("--- Shortest Path Distances from Depot ---")
    print(dijkstra(graph, 'Depot'))
    
    print("\n--- Optimized TSP Delivery Route ---")
    targets = ['Hub_A', 'Hub_B', 'Hub_C', 'Hub_D']
    route, dist = nearest_neighbor_tsp(graph, 'Depot', targets)
    print(f"Optimal Route: {' -> '.join(route)}")
    print(f"Total Travel Distance: {dist} km")