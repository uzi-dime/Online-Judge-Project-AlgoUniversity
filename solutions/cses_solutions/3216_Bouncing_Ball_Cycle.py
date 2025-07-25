# CSES Problem: Bouncing Ball Cycle
# Problem ID: 3216
# Generated on: 2025-07-22 20:36:34

import sys
import math

input = sys.stdin.readline

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    g = gcd(n - 1, m - 1)
    # The ball returns after lcm(n-1, m-1) * 2 steps
    lcm = ((n - 1) * (m - 1)) // g
    steps = 2 * lcm
    # Number of distinct cells visited: n + m - gcd(n-1, m-1)
    visited = n + m - g
    print(f"{steps} {visited}")