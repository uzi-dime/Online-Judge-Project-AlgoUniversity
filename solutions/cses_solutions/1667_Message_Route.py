# CSES Problem: Message Route
# Problem ID: 1667
# Generated on: 2025-07-22 20:27:18

import sys
import threading
from collections import deque

def main():
    n, m = map(int, sys.stdin.readline().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        adj[a].append(b)
        adj[b].append(a)

    # BFS from node 1 to node n
    visited = [False] * (n + 1)
    parent = [0] * (n + 1)
    queue = deque()
    queue.append(1)
    visited[1] = True

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.append(v)
                if v == n:
                    break

    if not visited[n]:
        print("IMPOSSIBLE")
        return

    # Reconstruct path
    path = []
    cur = n
    while cur != 0:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    print(len(path))
    print(' '.join(map(str, path)))

# For PyPy3 compatibility and to avoid recursion limit issues
threading.Thread(target=main).start()