# CSES Problem: Acyclic Graph Edges
# Problem ID: 1756
# Generated on: 2025-07-22 20:25:38

import sys
import threading
from collections import deque

def main():
    sys.setrecursionlimit(1 << 25)
    n, m = map(int, sys.stdin.readline().split())
    edges = []
    adj = [[] for _ in range(n + 1)]
    for idx in range(m):
        a, b = map(int, sys.stdin.readline().split())
        edges.append((a, b))
        adj[a].append((b, idx))
        adj[b].append((a, idx))

    # Check if the graph is a forest (acyclic)
    visited = [False] * (n + 1)
    def is_cyclic():
        parent = [0] * (n + 1)
        for start in range(1, n + 1):
            if not visited[start]:
                queue = deque()
                queue.append(start)
                visited[start] = True
                while queue:
                    u = queue.popleft()
                    for v, _ in adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            parent[v] = u
                            queue.append(v)
                        elif parent[u] != v:
                            return True
        return False

    if is_cyclic():
        print("IMPOSSIBLE")
        return

    # If acyclic, assign directions from parent to child in BFS
    edge_dir = [None] * m
    visited = [False] * (n + 1)
    for start in range(1, n + 1):
        if not visited[start]:
            queue = deque()
            queue.append(start)
            visited[start] = True
            while queue:
                u = queue.popleft()
                for v, idx in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        edge_dir[idx] = (u, v)
                        queue.append(v)
                    elif edge_dir[idx] is None:
                        # Already visited, but edge not assigned: assign in the other direction
                        edge_dir[idx] = (u, v)

    for a, b in edge_dir:
        print(a, b)