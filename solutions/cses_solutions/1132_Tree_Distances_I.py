# CSES Problem: Tree Distances I
# Problem ID: 1132
# Generated on: 2025-07-22 20:32:44

import sys
import threading
from collections import deque

def main():
    sys.setrecursionlimit(1 << 25)
    n = int(sys.stdin.readline())
    edges = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, sys.stdin.readline().split())
        edges[a - 1].append(b - 1)
        edges[b - 1].append(a - 1)

    # Helper: BFS to find farthest node and distances from start
    def bfs(start):
        dist = [-1] * n
        q = deque()
        q.append(start)
        dist[start] = 0
        farthest = start
        while q:
            u = q.popleft()
            for v in edges[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
                    if dist[v] > dist[farthest]:
                        farthest = v
        return farthest, dist

    # 1. Find one endpoint of the diameter
    u, _ = bfs(0)
    # 2. Find the other endpoint and distances from u
    v, dist_u = bfs(u)
    # 3. Get distances from v
    _, dist_v = bfs(v)

    # 4. For each node, the answer is max(dist_u[i], dist_v[i])
    res = [str(max(dist_u[i], dist_v[i])) for i in range(n)]
    print(' '.join(res))

threading.Thread(target=main).start()