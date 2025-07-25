# CSES Problem: Filled Subgrid Count I
# Problem ID: 3413
# Generated on: 2025-07-22 20:29:09

import sys
import threading

def main():
    import sys

    sys.setrecursionlimit(1 << 25)
    n, k = map(int, sys.stdin.readline().split())
    grid = [sys.stdin.readline().strip() for _ in range(n)]

    # Prepare answer array for each letter
    ans = [0] * k
    # For each letter, process the grid
    for letter_ord in range(k):
        letter = chr(ord('A') + letter_ord)
        # dp[i][j]: size of largest square ending at (i, j) with all letter
        dp = [ [0] * n for _ in range(n) ]
        for i in range(n):
            for j in range(n):
                if grid[i][j] == letter:
                    if i == 0 or j == 0:
                        dp[i][j] = 1
                    else:
                        dp[i][j] = 1 + min(
                            dp[i-1][j],
                            dp[i][j-1],
                            dp[i-1][j-1]
                        )
                    ans[letter_ord] += dp[i][j]
                # else dp[i][j] stays 0
    for count in ans:
        print(count)