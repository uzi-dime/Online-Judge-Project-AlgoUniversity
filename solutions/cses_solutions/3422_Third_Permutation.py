# CSES Problem: Third Permutation
# Problem ID: 3422
# Generated on: 2025-07-22 20:37:44

import sys

input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# All numbers from 1 to n
all_nums = set(range(1, n + 1))

# Prepare c with -1
c = [-1] * n

# For each position, try to assign a number not equal to a[i] or b[i]
used = set()
for i in range(n):
    # Candidates: all numbers except a[i], b[i], and already used
    candidates = all_nums - {a[i], b[i]} - used
    if not candidates:
        print("IMPOSSIBLE")
        sys.exit(0)
    # Pick any candidate (smallest for determinism)
    val = min(candidates)
    c[i] = val
    used.add(val)

print(' '.join(map(str, c)))