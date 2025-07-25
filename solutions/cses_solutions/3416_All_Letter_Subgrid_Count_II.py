# CSES Problem: All Letter Subgrid Count II
# Problem ID: 3416
# Generated on: 2025-07-22 20:29:42

import sys

input = sys.stdin.readline

n, k = map(int, input().split())
grid = [input().strip() for _ in range(n)]

# Map each letter to a bit position
letter_to_bit = {chr(ord('A') + i): i for i in range(k)}
full_mask = (1 << k) - 1

# Precompute for each row, for each column, the bitmask of the letter at that cell
bitmasks = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        c = grid[i][j]
        if c in letter_to_bit:
            bitmasks[i][j] = 1 << letter_to_bit[c]
        else:
            bitmasks[i][j] = 0

result = 0

# For each pair of rows (top, bottom)
for top in range(n):
    col_masks = [0] * n  # For each column, the OR of letters between top and bottom
    for bottom in range(top, n):
        for col in range(n):
            col_masks[col] |= bitmasks[bottom][col]

        # Now, for this row span, count the number of subarrays (columns) whose OR is full_mask
        left = 0
        curr_mask = 0
        for right in range(n):
            curr_mask |= col_masks[right]
            while left <= right and curr_mask == full_mask:
                # Try to shrink from the left as much as possible
                curr_mask ^= col_masks[left]
                left += 1
            # The number of valid subarrays ending at 'right' is (left)
            result += left

print(result)