# CSES Problem: Number of Subset Xors
# Problem ID: 3211
# Generated on: 2025-07-22 20:30:57

import sys

# Read input
input = sys.stdin.readline
n = int(input())
arr = list(map(int, input().split()))

# Basis for linear basis (max 32 bits for 0 <= xi <= 1e9)
basis = [0] * 32

for num in arr:
    x = num
    for i in reversed(range(32)):
        if (x >> i) & 1:
            if basis[i] == 0:
                basis[i] = x
                break
            else:
                x ^= basis[i]

# Count non-zero basis vectors
rank = sum(1 for b in basis if b != 0)

# The number of different subset xors is 2^rank
print(1 << rank)