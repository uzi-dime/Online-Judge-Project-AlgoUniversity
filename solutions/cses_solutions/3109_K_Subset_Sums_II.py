# CSES Problem: K Subset Sums II
# Problem ID: 3109
# Generated on: 2025-07-22 20:37:11

import sys
import heapq

input = sys.stdin.readline

n, m, k = map(int, input().split())
arr = list(map(int, input().split()))
arr.sort()

# Start with the smallest m elements
init = arr[:m]
init_sum = sum(init)

# Each state: (current_sum, indices of elements used)
# To avoid duplicates, we use a tuple of indices
# But to optimize, we use a tuple of positions where we can swap in a larger element

# The state is represented by:
# (current_sum, [positions of elements in arr used for the subset])
# We always keep the indices sorted

# We use a min-heap to get the next smallest sum
heap = []
visited = set()

# Initial state: sum of first m elements, indices 0..m-1
init_indices = tuple(range(m))
heapq.heappush(heap, (init_sum, init_indices))
visited.add(init_indices)

results = []

for _ in range(k):
    curr_sum, indices = heapq.heappop(heap)
    results.append(curr_sum)
    # Try to generate new states by replacing one element with the next unused element
    # To avoid duplicates, only allow increasing the index at each position
    for i in range(m):
        if indices[i] < n - (m - i):
            # Create new indices by incrementing indices[i] by 1, and adjusting the rest
            new_indices = list(indices)
            new_indices[i] += 1
            # Ensure strictly increasing order
            for j in range(i+1, m):
                new_indices[j] = new_indices[j-1] + 1
            if new_indices[-1] >= n:
                continue
            new_indices_tuple = tuple(new_indices)
            if new_indices_tuple in visited:
                continue
            # Calculate new sum efficiently
            # Remove arr[indices[i]], add arr[new_indices[i]]
            new_sum = curr_sum - arr[indices[i]] + arr[new_indices[i]]
            # For j > i, we replaced arr[indices[j]] with arr[new_indices[j]]
            for j in range(i+1, m):
                new_sum = new_sum - arr[indices[j]] + arr[new_indices[j]]
            heapq.heappush(heap, (new_sum, new_indices_tuple))
            visited.add(new_indices_tuple)

print(' '.join(map(str, results)))