# CSES Problem: Monotone Subsequences
# Problem ID: 2215
# Generated on: 2025-07-22 20:37:34

import sys

input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    # Impossible if k < 1 or k > n
    if k < 1 or k > n:
        print("IMPOSSIBLE")
        continue
    # To make the longest monotone subsequence exactly k:
    # Place the first n-k+1 numbers in decreasing order, then the rest in increasing order
    # This ensures both LIS and LDS are exactly k
    res = []
    # First n-k+1 in decreasing order
    for i in range(n-k+1, 0, -1):
        res.append(i)
    # Then k-1 in increasing order
    for i in range(n-k+2, n+1):
        res.append(i)
    print(' '.join(map(str, res)))