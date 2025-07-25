# CSES Problem: Common Divisors
# Problem ID: 1081
# Generated on: 2025-07-22 20:26:33

import sys

# Read input
input = sys.stdin.readline
n = int(input())
arr = list(map(int, input().split()))

MAX = 10**6 + 1
count = [0] * MAX

# Count occurrences of each number
for x in arr:
    count[x] += 1

# For each possible GCD from high to low, check if at least two multiples exist
for g in range(MAX - 1, 0, -1):
    multiples = 0
    for k in range(g, MAX, g):
        multiples += count[k]
        if multiples >= 2:
            print(g)
            sys.exit(0)