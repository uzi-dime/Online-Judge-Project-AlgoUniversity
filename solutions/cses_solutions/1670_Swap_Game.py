# CSES Problem: Swap Game
# Problem ID: 1670
# Generated on: 2025-07-22 20:33:52

from collections import deque

# Read the input grid
start = []
for _ in range(3):
    start.extend(map(int, input().split()))

# The goal state
goal = tuple([1,2,3,4,5,6,7,8,9])

# Precompute the neighbors for each position in the 3x3 grid
neighbors = [
    [1,3],        # 0
    [0,2,4],      # 1
    [1,5],        # 2
    [0,4,6],      # 3
    [1,3,5,7],    # 4
    [2,4,8],      # 5
    [3,7],        # 6
    [4,6,8],      # 7
    [5,7]         # 8
]

def bfs(start):
    start = tuple(start)
    if start == goal:
        return 0
    visited = {start: 0}
    q = deque()
    q.append(start)
    while q:
        curr = q.popleft()
        dist = visited[curr]
        for i in range(9):
            for j in neighbors[i]:
                # Swap i and j
                lst = list(curr)
                lst[i], lst[j] = lst[j], lst[i]
                nxt = tuple(lst)
                if nxt not in visited:
                    if nxt == goal:
                        return dist + 1
                    visited[nxt] = dist + 1
                    q.append(nxt)
    return -1  # Should never happen for this problem

print(bfs(start))