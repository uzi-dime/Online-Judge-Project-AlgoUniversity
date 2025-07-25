# CSES Problem: Static Range Minimum Queries
# Problem ID: 1647
# Generated on: 2025-07-22 20:31:38

import sys
import threading

def main():
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    arr = list(map(int, input().split()))

    # Build segment tree for range minimum query
    size = 1
    while size < n:
        size <<= 1
    INF = 10**18
    seg = [INF] * (2 * size)
    # Fill leaves
    for i in range(n):
        seg[size + i] = arr[i]
    # Build tree
    for i in range(size - 1, 0, -1):
        seg[i] = min(seg[2 * i], seg[2 * i + 1])

    def range_min(l, r):
        # Query min in [l, r)
        l += size
        r += size
        res = INF
        while l < r:
            if l % 2:
                res = min(res, seg[l])
                l += 1
            if r % 2:
                r -= 1
                res = min(res, seg[r])
            l //= 2
            r //= 2
        return res

    for _ in range(q):
        a, b = map(int, input().split())
        # Convert to 0-based, [a-1, b)
        print(range_min(a - 1, b))

threading.Thread(target=main).start()