# CSES Problem: Dynamic Range Sum Queries
# Problem ID: 1648
# Generated on: 2025-07-22 20:31:46

import sys

# Fast input
input = sys.stdin.readline

# Fenwick Tree (Binary Indexed Tree) for range sum and point update
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 2)  # 1-based indexing

    def add(self, idx, delta):
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & -idx
        return res

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

n, q = map(int, input().split())
arr = [0] + list(map(int, input().split()))  # 1-based indexing

ft = FenwickTree(n)
for i in range(1, n + 1):
    ft.add(i, arr[i])

output = []
for _ in range(q):
    parts = input().split()
    if parts[0] == '1':
        k = int(parts[1])
        u = int(parts[2])
        diff = u - arr[k]
        arr[k] = u
        ft.add(k, diff)
    else:
        a = int(parts[1])
        b = int(parts[2])
        output.append(str(ft.range_sum(a, b)))

print('\n'.join(output))