# CSES Problem: Border Subgrid Count I
# Problem ID: 3417
# Generated on: 2025-07-22 20:30:04

import sys
import threading

def main():
    import sys

    sys.setrecursionlimit(1 << 25)
    n, k = map(int, sys.stdin.readline().split())
    grid = [sys.stdin.readline().strip() for _ in range(n)]

    # Prepare answer array for each letter
    ans = [0] * k
    # Map letter to index
    letter_to_idx = {chr(ord('A') + i): i for i in range(k)}

    # For each letter, process separately
    for c in range(k):
        ch = chr(ord('A') + c)
        # Build a binary grid: 1 if cell == ch, else 0
        bin_grid = [[1 if grid[i][j] == ch else 0 for j in range(n)] for i in range(n)]

        # Precompute prefix sums for rows and columns
        row_sum = [[0] * (n + 1) for _ in range(n)]
        col_sum = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                row_sum[i][j + 1] = row_sum[i][j] + bin_grid[i][j]
                col_sum[j][i + 1] = col_sum[j][i] + bin_grid[i][j]

        # For each cell, compute the maximum possible square size with border ch
        # dp[i][j]: max size of square with bottom-right corner at (i,j) and border ch
        dp = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if bin_grid[i][j] == 0:
                    dp[i][j] = 0
                else:
                    if i == 0 or j == 0:
                        dp[i][j] = 1
                    else:
                        # The maximum size possible is limited by the previous squares
                        max_prev = min(dp[i-1][j-1] + 1, i+1, j+1)
                        # Binary search for largest possible size
                        low, high = 1, max_prev
                        res = 1
                        while low <= high:
                            mid = (low + high) // 2
                            # Check if all border cells of square of size mid ending at (i,j) are ch
                            x1, y1 = i - mid + 1, j - mid + 1
                            if x1 < 0 or y1 < 0:
                                high = mid - 1
                                continue
                            # Top and bottom rows
                            top_row = row_sum[x1][j+1] - row_sum[x1][y1]
                            bot_row = row_sum[i][j+1] - row_sum[i][y1]
                            # Left and right columns (excluding corners already counted)
                            left_col = col_sum[y1][i] - col_sum[y1][x1+1]
                            right_col = col_sum[j][i] - col_sum[j][x1+1]
                            border_count = top_row + bot_row + left_col + right_col
                            needed = 4 * (mid - 1)
                            if mid == 1:
                                needed = 1
                                border_count = 1 if bin_grid[i][j] == 1 else 0
                            if border_count == needed:
                                res = mid
                                low = mid + 1
                            else:
                                high = mid - 1
                        dp[i][j] = res
                        # For each possible size, the square with size res ending at (i,j) is valid
                        ans[c] += dp[i][j]

    for cnt in ans:
        print(cnt)

threading.Thread(target=main).start()