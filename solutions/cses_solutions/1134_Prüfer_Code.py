# CSES Problem: Prüfer Code
# Problem ID: 1134
# Generated on: 2025-07-22 20:25:04

import sys
import heapq

def main():
    input = sys.stdin.readline
    n = int(input())
    code = list(map(int, input().split()))
    
    degree = [1] * (n + 1)  # degree[0] unused
    for v in code:
        degree[v] += 1

    # Min-heap of leaves (nodes with degree 1)
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heapq.heappush(leaves, i)

    edges = []
    for v in code:
        u = heapq.heappop(leaves)
        edges.append((u, v))
        degree[u] -= 1
        degree[v] -= 1
        if degree[v] == 1:
            heapq.heappush(leaves, v)

    # Two nodes remain
    u = heapq.heappop(leaves)
    v = heapq.heappop(leaves)
    edges.append((u, v))

    for a, b in edges:
        print(a, b)

if __name__ == "__main__":
    main()