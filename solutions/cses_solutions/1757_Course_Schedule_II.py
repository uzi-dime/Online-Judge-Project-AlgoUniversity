# CSES Problem: Course Schedule II
# Problem ID: 1757
# Generated on: 2025-07-22 20:25:25

import sys
import threading
import heapq

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    n, m = map(int, sys.stdin.readline().split())
    adj = [[] for _ in range(n + 1)]
    indegree = [0] * (n + 1)

    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        adj[a].append(b)
        indegree[b] += 1

    # Min-heap for lex smallest order
    heap = []
    for i in range(1, n + 1):
        if indegree[i] == 0:
            heapq.heappush(heap, i)

    res = []
    while heap:
        u = heapq.heappop(heap)
        res.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(heap, v)

    print(' '.join(map(str, res)))

threading.Thread(target=main).start()