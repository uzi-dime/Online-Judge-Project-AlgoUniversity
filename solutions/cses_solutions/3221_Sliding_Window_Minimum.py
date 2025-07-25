# CSES Problem: Sliding Window Minimum
# Problem ID: 3221
# Generated on: 2025-07-22 20:23:13

import sys
import collections

# Fast input
input = sys.stdin.readline

n, k = map(int, sys.stdin.readline().split())
x, a, b, c = map(int, sys.stdin.readline().split())

# Generator for the array
def gen_array(n, x, a, b, c):
    curr = x
    yield curr
    for _ in range(n - 1):
        curr = (a * curr + b) % c
        yield curr

# Monotonic queue for sliding window minimum
dq = collections.deque()
result = 0

arr_gen = gen_array(n, x, a, b, c)

for i, val in enumerate(arr_gen):
    # Remove elements from the back that are >= current value
    while dq and dq[-1][0] >= val:
        dq.pop()
    dq.append((val, i))
    # Remove elements from the front that are out of the window
    if dq[0][1] <= i - k:
        dq.popleft()
    # When we have a full window, take the minimum (front of deque)
    if i >= k - 1:
        result ^= dq[0][0]

print(result)