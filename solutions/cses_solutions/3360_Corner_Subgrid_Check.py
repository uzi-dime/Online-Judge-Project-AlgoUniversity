# CSES Problem: Corner Subgrid Check
# Problem ID: 3360
# Generated on: 2025-07-22 20:35:25

import sys

input = sys.stdin.readline

n, k = map(int, input().split())
grid = [input().strip() for _ in range(n)]

# Prepare data structures for each letter
from collections import defaultdict

# For each letter, store the min/max row and min/max col where it appears
min_row = [n] * k
max_row = [-1] * k
min_col = [n] * k
max_col = [-1] * k

# Map letter to index
def l2i(c):
    return ord(c) - ord('A')

# First pass: find min/max row/col for each letter
for i in range(n):
    for j in range(n):
        idx = l2i(grid[i][j])
        min_row[idx] = min(min_row[idx], i)
        max_row[idx] = max(max_row[idx], i)
        min_col[idx] = min(min_col[idx], j)
        max_col[idx] = max(max_col[idx], j)

# For each letter, check if there is a subgrid of at least 2x2 with all corners having that letter
results = ['NO'] * k

for letter in range(k):
    if max_row[letter] - min_row[letter] < 1 or max_col[letter] - min_col[letter] < 1:
        continue  # Not enough spread for 2x2
    found = False
    # Check all four corners of the bounding rectangle
    corners = [
        (min_row[letter], min_col[letter]),
        (min_row[letter], max_col[letter]),
        (max_row[letter], min_col[letter]),
        (max_row[letter], max_col[letter])
    ]
    # For efficiency, check all possible pairs of rows and columns in the bounding box
    # Only need to find one valid 2x2 or larger subgrid with all corners matching
    for r1 in range(min_row[letter], max_row[letter]):
        for r2 in range(r1+1, max_row[letter]+1):
            for c1 in range(min_col[letter], max_col[letter]):
                for c2 in range(c1+1, max_col[letter]+1):
                    if (grid[r1][c1] == grid[r1][c2] == grid[r2][c1] == grid[r2][c2] == chr(ord('A') + letter)):
                        found = True
                        break
                if found:
                    break
            if found:
                break
        if found:
            break
    if found:
        results[letter] = 'YES'

for res in results:
    print(res)