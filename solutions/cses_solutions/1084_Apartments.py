# CSES Problem: Apartments
# Problem ID: 1084
# Generated on: 2025-07-22 20:20:18

import sys

# Fast input
input = sys.stdin.readline

# Read n, m, k
n, m, k = map(int, input().split())

# Read desired sizes and apartment sizes
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# Sort both lists for two-pointer approach
a.sort()
b.sort()

i = j = res = 0

# Two-pointer matching
while i < n and j < m:
    if abs(a[i] - b[j]) <= k:
        res += 1
        i += 1
        j += 1
    elif b[j] < a[i] - k:
        j += 1
    else:
        i += 1

print(res)