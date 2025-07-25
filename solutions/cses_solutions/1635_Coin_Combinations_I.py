# CSES Problem: Coin Combinations I
# Problem ID: 1635
# Generated on: 2025-07-22 20:21:11

import sys

MOD = 10**9 + 7

def main():
    input = sys.stdin.readline
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    
    # dp[i]: number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # one way to make sum 0: use no coins

    for coin in coins:
        for i in range(coin, x + 1):
            dp[i] = (dp[i] + dp[i - coin]) % MOD

    print(dp[x])

if __name__ == "__main__":
    main()