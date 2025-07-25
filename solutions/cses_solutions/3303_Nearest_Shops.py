# CSES Problem: Nearest Shops
# Problem ID: 3303
# Generated on: 2025-07-22 20:24:55

import sys
import threading
from collections import deque

def main():
    import sys

    sys.setrecursionlimit(1 << 25)
    n, m, k = map(int, sys.stdin.readline().split())
    anime_shops = set(map(int, sys.stdin.readline().split()))

    # Build the graph
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        graph[a].append(b)
        graph[b].append(a)

    # Initialize distances and owner arrays
    dist = [-1] * (n + 1)
    owner = [0] * (n + 1)  # which anime shop this city is closest to

    # Multi-source BFS from all anime shops
    q = deque()
    for shop in anime_shops:
        dist[shop] = 0
        owner[shop] = shop
        q.append(shop)

    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                owner[v] = owner[u]
                q.append(v)
            # If already visited, do nothing (first found is always shortest)

    # For each city, find the minimum distance to another anime shop
    res = []
    for city in range(1, n + 1):
        min_dist = -1
        for v in graph[city]:
            if v in anime_shops and v != city:
                # Direct neighbor with anime shop
                min_dist = 1
                break
            elif owner[v] != owner[city] and owner[v] != 0:
                # Neighbor's closest shop is different
                d = dist[v] + 1
                if min_dist == -1 or d < min_dist:
                    min_dist = d
        res.append(str(min_dist))

    print(' '.join(res))

threading.Thread(target=main).start()