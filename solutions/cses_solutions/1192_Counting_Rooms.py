# CSES Problem: Counting Rooms
# Problem ID: 1192
# Generated on: 2025-07-22 20:26:47

import sys
from collections import deque

# Read input efficiently
input = sys.stdin.readline

n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]
visited = [[False] * m for _ in range(n)]

def bfs(start_i, start_j):
    queue = deque()
    queue.append((start_i, start_j))
    visited[start_i][start_j] = True
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if not visited[nx][ny] and grid[nx][ny] == '.':
                    visited[nx][ny] = True
                    queue.append((nx, ny))

room_count = 0
for i in range(n):
    for j in range(m):
        if grid[i][j] == '.' and not visited[i][j]:
            bfs(i, j)
            room_count += 1

print(room_count)