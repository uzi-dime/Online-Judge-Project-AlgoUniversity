# CSES Problem: Building Teams
# Problem ID: 1668
# Generated on: 2025-07-22 20:27:48

import sys
import threading
from collections import deque

def main():
    sys.setrecursionlimit(1 << 25)
    n, m = map(int, sys.stdin.readline().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        adj[a].append(b)
        adj[b].append(a)

    color = [0] * (n + 1)  # 0: unvisited, 1: team 1, 2: team 2

    for start in range(1, n + 1):
        if color[start] == 0:
            queue = deque()
            queue.append(start)
            color[start] = 1
            while queue:
                node = queue.popleft()
                for neighbor in adj[node]:
                    if color[neighbor] == 0:
                        color[neighbor] = 3 - color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        print("IMPOSSIBLE")
                        return

    print(' '.join(str(color[i]) for i in range(1, n + 1)))

threading.Thread(target=main).start()