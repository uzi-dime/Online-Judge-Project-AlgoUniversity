# CSES Problem: All Letter Subgrid Count I
# Problem ID: 3415
# Generated on: 2025-07-22 20:29:32

import sys

input = sys.stdin.readline

n, k = map(int, input().split())
grid = [input().strip() for _ in range(n)]

# Map each letter to a bit position
letters = [chr(ord('A') + i) for i in range(k)]
letter_to_bit = {c: i for i, c in enumerate(letters)}
full_mask = (1 << k) - 1

# Precompute prefix sums of bitmasks for each row
prefix = [[0] * (n + 1) for _ in range(n)]
for i in range(n):
    for j in range(n):
        prefix[i][j + 1] = prefix[i][j] | (1 << letter_to_bit[grid[i][j]])

result = 0

# For each possible square size
for size in range(1, n + 1):
    # For each possible top row
    for top in range(n - size + 1):
        # For each possible left column
        for left in range(n - size + 1):
            mask = 0
            # For each row in the square
            for row in range(top, top + size):
                # Get mask for this row in the square
                row_mask = prefix[row][left + size] ^ prefix[row][left]
                mask |= row_mask
                # Early break if already all letters found
                if mask == full_mask:
                    break
            if mask == full_mask:
                result += 1

print(result)