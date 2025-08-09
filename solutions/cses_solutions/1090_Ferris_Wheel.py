# CSES Problem: Ferris Wheel
# Problem ID: 1090
# Generated on: 2025-07-30 22:05:08

import sys

def solve():
    n, x = map(int, sys.stdin.readline().split())
    p = list(map(int, sys.stdin.readline().split()))
    p.sort()

    left = 0
    right = n - 1
    gondolas = 0

    while left <= right:
        gondolas += 1
        if left == right:
            break
        if p[left] + p[right] <= x:
            left += 1
        right -= 1

    print(gondolas)

if __name__ == "__main__":
    solve()