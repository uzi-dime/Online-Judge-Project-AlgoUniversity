# CSES Problem: Minimizing Coins
# Problem ID: 1634
# Generated on: 2025-07-22 20:21:03

import sys

# Read input
n, x = map(int, sys.stdin.readline().split())
coins = list(map(int, sys.stdin.readline().split()))

# Initialize DP array: dp[i] = min coins to make sum i
INF = int(1e9)
dp = [INF] * (x + 1)
dp[0] = 0

# Dynamic programming to fill dp array
for coin in coins:
    for i in range(coin, x + 1):
        if dp[i - coin] + 1 < dp[i]:
            dp[i] = dp[i - coin] + 1

# Output result
print(dp[x] if dp[x] != INF else -1)