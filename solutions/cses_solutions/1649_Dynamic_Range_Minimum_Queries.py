# CSES Problem: Dynamic Range Minimum Queries
# Problem ID: 1649
# Generated on: 2025-07-22 20:31:54

import sys

# Fast input
input = sys.stdin.readline

# Fenwick Tree (Binary Indexed Tree) for range sum queries and point updates
class FenwickTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (self.n + 2)

    def add(self, idx, value):
        while idx <= self.n:
            self.tree[idx] += value
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
arr = list(map(int, input().split()))

# 1-based indexing for Fenwick Tree
ft = FenwickTree(n)
for i in range(n):
    ft.add(i + 1, arr[i])

for _ in range(q):
    parts = input().split()
    if parts[0] == '1':
        # Update: set arr[k-1] = u
        k = int(parts[1])
        u = int(parts[2])
        diff = u - arr[k - 1]
        ft.add(k, diff)
        arr[k - 1] = u
    else:
        # Query: sum from a to b
        a = int(parts[1])
        b = int(parts[2])
        print(ft.range_sum(a, b))