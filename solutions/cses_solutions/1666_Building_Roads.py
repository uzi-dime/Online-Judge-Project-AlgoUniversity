# CSES Problem: Building Roads
# Problem ID: 1666
# Generated on: 2025-07-22 20:27:09

import sys
import threading

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    n, m = map(int, sys.stdin.readline().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        adj[a].append(b)
        adj[b].append(a)

    visited = [False] * (n + 1)
    reps = []

    # Use iterative DFS to avoid recursion limit issues
    def dfs(start):
        stack = [start]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in adj[node]:
                    if not visited[neighbor]:
                        stack.append(neighbor)

    for city in range(1, n + 1):
        if not visited[city]:
            reps.append(city)
            dfs(city)

    # To connect all components, connect each representative to the next
    k = len(reps) - 1
    print(k)
    for i in range(k):
        print(reps[i], reps[i + 1])

threading.Thread(target=main).start()