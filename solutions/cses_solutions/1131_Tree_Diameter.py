# CSES Problem: Tree Diameter
# Problem ID: 1131
# Generated on: 2025-07-22 20:32:35

import sys
import threading
from collections import deque

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    n = int(sys.stdin.readline())
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = map(int, sys.stdin.readline().split())
        adj[a].append(b)
        adj[b].append(a)

    # BFS to find the farthest node from a starting node
    def bfs(start):
        dist = [-1] * (n + 1)
        q = deque()
        q.append(start)
        dist[start] = 0
        farthest_node = start
        while q:
            node = q.popleft()
            for neighbor in adj[node]:
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[node] + 1
                    q.append(neighbor)
                    if dist[neighbor] > dist[farthest_node]:
                        farthest_node = neighbor
        return farthest_node, dist[farthest_node]

    # First BFS from any node (say, 1) to find one endpoint of the diameter
    u, _ = bfs(1)
    # Second BFS from u to find the actual diameter
    v, diameter = bfs(u)
    print(diameter)

threading.Thread(target=main).start()