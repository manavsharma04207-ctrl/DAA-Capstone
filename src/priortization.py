import pandas as pd

def sort_parcels(parcels_list, by='deadline_hours', ascending=True):
    """Sorts parcels based on priority, deadline, or weight."""
    return sorted(parcels_list, key=lambda x: x[by], reverse=not ascending)

def knapsack_01_optimizer(parcels_list, max_capacity):
    """
    0/1 Knapsack Dynamic Programming approach to select the optimal parcel subset
    that maximizes priority score within vehicle weight capacity.
    """
    n = len(parcels_list)
    dp = [[0 for _ in range(max_capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels_list[i-1]['weight_kg']
        val = parcels_list[i-1]['priority_score']
        for c in range(1, max_capacity + 1):
            if weight <= c:
                dp[i][c] = max(val + dp[i-1][c - weight], dp[i-1][c])
            else:
                dp[i][c] = dp[i-1][c]

    # Traceback to extract selected parcel items
    selected_parcels = []
    c = max_capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i-1][c]:
            selected_parcels.append(parcels_list[i-1])
            c -= parcels_list[i-1]['weight_kg']

    return selected_parcels[::-1], dp[n][max_capacity]

if __name__ == '__main__':
    df = pd.read_csv('../datasets/parcels.csv') if __file__.endswith('prioritization.py') else pd.read_csv('datasets/parcels.csv')
    parcels = df.to_dict(orient='records')
    
    print("--- 1. Sorted by Deadline ---")
    sorted_p = sort_parcels(parcels, by='deadline_hours', ascending=True)
    for p in sorted_p:
        print(p)
        
    print("\n--- 2. Knapsack Optimization (Cap: 25kg) ---")
    selected, total_val = knapsack_01_optimizer(parcels, max_capacity=25)
    print(f"Total Priority Score Achieved: {total_val}")
    print("Selected Parcels:")
    for p in selected:
        print(p)