# CSES Problem: Coin Combinations II
# Problem ID: 1636
# Generated on: 2025-07-22 20:21:20

import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n, x = map(int, input().split())
coins = list(map(int, input().split()))

# dp[i] = number of ordered ways to make sum i
dp = [0] * (x + 1)
dp[0] = 1  # base case: one way to make sum 0 (choose nothing)

for i in range(1, x + 1):
    for c in coins:
        if i - c >= 0:
            dp[i] = (dp[i] + dp[i - c]) % MOD

print(dp[x])