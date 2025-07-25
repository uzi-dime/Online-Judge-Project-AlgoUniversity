# CSES Problem: Static Range Sum Queries
# Problem ID: 1646
# Generated on: 2025-07-22 20:31:21

import sys

# Fast input reading
input = sys.stdin.readline

n, q = map(int, input().split())
arr = list(map(int, input().split()))

# Compute prefix sums
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + arr[i]

# Process queries
for _ in range(q):
    a, b = map(int, input().split())
    # Output sum in range [a, b] (1-based indexing)
    print(prefix[b] - prefix[a - 1])