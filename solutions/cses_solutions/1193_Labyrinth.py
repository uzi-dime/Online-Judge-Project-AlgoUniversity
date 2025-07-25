# CSES Problem: Labyrinth
# Problem ID: 1193
# Generated on: 2025-07-22 20:27:01

import sys
from collections import deque

def main():
    n, m = map(int, sys.stdin.readline().split())
    grid = [list(sys.stdin.readline().strip()) for _ in range(n)]
    
    # Find start (A) and end (B)
    start = end = None
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'A':
                start = (i, j)
            elif grid[i][j] == 'B':
                end = (i, j)
    
    # BFS setup
    directions = [('U', -1, 0), ('D', 1, 0), ('L', 0, -1), ('R', 0, 1)]
    visited = [[False for _ in range(m)] for _ in range(n)]
    parent = [[None for _ in range(m)] for _ in range(n)]
    q = deque()
    q.append(start)
    visited[start[0]][start[1]] = True
    
    found = False
    while q:
        i, j = q.popleft()
        if (i, j) == end:
            found = True
            break
        for d, di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj] and grid[ni][nj] != '#':
                visited[ni][nj] = True
                parent[ni][nj] = (i, j, d)
                q.append((ni, nj))
    
    if not found:
        print("NO")
        return
    
    # Reconstruct path
    path = []
    i, j = end
    while (i, j) != start:
        pi, pj, d = parent[i][j]
        path.append(d)
        i, j = pi, pj
    path.reverse()
    
    print("YES")
    print(len(path))
    print(''.join(path))

if __name__ == "__main__":
    main()