# CSES Problem: K Subset Sums I
# Problem ID: 3108
# Generated on: 2025-07-22 20:36:55

import sys
import heapq

input = sys.stdin.readline

n, k = map(int, input().split())
arr = list(map(int, input().split()))
arr.sort()

# Min-heap: (current_sum, index in arr)
heap = []
heapq.heappush(heap, (0, 0))

# To avoid duplicates: (sum, idx) pairs
seen = set()
seen.add((0, 0))

result = []

for _ in range(k):
    curr_sum, idx = heapq.heappop(heap)
    result.append(curr_sum)
    if idx < n:
        # Include arr[idx]
        next1 = (curr_sum + arr[idx], idx + 1)
        if next1 not in seen:
            heapq.heappush(heap, next1)
            seen.add(next1)
        # Exclude arr[idx]
        next2 = (curr_sum, idx + 1)
        if next2 not in seen:
            heapq.heappush(heap, next2)
            seen.add(next2)

print(' '.join(map(str, result)))