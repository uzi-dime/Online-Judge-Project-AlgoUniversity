# CSES Problem: Ferris Wheel
# Problem ID: 1090
# Generated on: 2025-07-22 20:20:26

import sys

# Read input efficiently
n, x = map(int, sys.stdin.readline().split())
p = list(map(int, sys.stdin.readline().split()))

# Sort children's weights
p.sort()

# Two pointers: i (lightest), j (heaviest)
i, j = 0, n - 1
gondolas = 0

while i <= j:
    # If lightest and heaviest together fit, pair them
    if p[i] + p[j] <= x:
        i += 1
    # Always take the heaviest child
    j -= 1
    gondolas += 1

print(gondolas)