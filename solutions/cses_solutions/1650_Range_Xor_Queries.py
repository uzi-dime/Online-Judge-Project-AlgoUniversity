# CSES Problem: Range Xor Queries
# Problem ID: 1650
# Generated on: 2025-07-22 20:32:01

import sys

input = sys.stdin.readline

n, q = map(int, input().split())
arr = list(map(int, input().split()))

# Compute prefix xor
prefix_xor = [0] * (n + 1)
for i in range(n):
    prefix_xor[i + 1] = prefix_xor[i] ^ arr[i]

# Process queries
for _ in range(q):
    a, b = map(int, input().split())
    # XOR of [a, b] is prefix_xor[b] ^ prefix_xor[a-1]
    print(prefix_xor[b] ^ prefix_xor[a - 1])