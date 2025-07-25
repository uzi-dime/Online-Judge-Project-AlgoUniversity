# CSES Problem: Corner Subgrid Count
# Problem ID: 2137
# Generated on: 2025-07-22 20:35:33

import sys

input = sys.stdin.readline

n = int(input())
grid = [list(map(int, input().strip())) for _ in range(n)]

# Precompute for each row, the columns where the cell is black
black_cols = [[] for _ in range(n)]
for i in range(n):
    for j in range(n):
        if grid[i][j] == 1:
            black_cols[i].append(j)

result = 0

# For each pair of rows (r1, r2), r1 < r2
for r1 in range(n):
    # Use a marker array for columns that are black in r1
    is_black = [0] * n
    for c in black_cols[r1]:
        is_black[c] = 1
    for r2 in range(r1 + 1, n):
        # Find columns where both r1 and r2 have black cells
        common = []
        for c in black_cols[r2]:
            if is_black[c]:
                common.append(c)
        # For k common columns, number of pairs is k choose 2
        k = len(common)
        if k >= 2:
            result += k * (k - 1) // 2

print(result)