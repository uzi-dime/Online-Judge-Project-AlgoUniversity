# CSES Problem: Sliding Window Distinct Values
# Problem ID: 3222
# Generated on: 2025-07-22 20:23:46

import sys
from collections import defaultdict

# Fast input
input = sys.stdin.readline

n, k = map(int, input().split())
arr = list(map(int, input().split()))

count = defaultdict(int)
distinct = 0
result = []

# Initialize the first window
for i in range(k):
    if count[arr[i]] == 0:
        distinct += 1
    count[arr[i]] += 1

result.append(distinct)

# Slide the window
for i in range(k, n):
    # Remove the element going out
    out_elem = arr[i - k]
    count[out_elem] -= 1
    if count[out_elem] == 0:
        distinct -= 1

    # Add the new element
    in_elem = arr[i]
    if count[in_elem] == 0:
        distinct += 1
    count[in_elem] += 1

    result.append(distinct)

print(' '.join(map(str, result)))