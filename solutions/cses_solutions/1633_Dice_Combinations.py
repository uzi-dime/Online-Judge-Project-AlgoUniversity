# CSES Problem: Dice Combinations
# Problem ID: 1633
# Generated on: 2025-07-22 20:20:55

MOD = 10**9 + 7

n = int(input())

# dp[x] = number of ways to get sum x
dp = [0] * (n + 1)
dp[0] = 1  # 1 way to get sum 0: no dice thrown

for x in range(1, n + 1):
    for d in range(1, 7):
        if x - d >= 0:
            dp[x] = (dp[x] + dp[x - d]) % MOD

print(dp[n])