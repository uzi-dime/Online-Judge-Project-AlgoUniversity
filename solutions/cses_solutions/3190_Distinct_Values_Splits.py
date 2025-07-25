# CSES Problem: Distinct Values Splits
# Problem ID: 3190
# Generated on: 2025-07-22 20:33:42

import sys

MOD = 10**9 + 7

def main():
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))
    
    dp = [0] * (n + 1)  # dp[i]: number of ways to split first i elements
    dp[0] = 1  # empty prefix has one way
    
    last_occurrence = dict()
    left = 0  # left pointer of current segment
    
    for right in range(1, n + 1):
        x = arr[right - 1]
        if x in last_occurrence:
            left = max(left, last_occurrence[x] + 1)
        # dp[right] = sum of dp[left-1] to dp[right-1]
        # We can use prefix sums to optimize
        # But since left only moves forward, we can keep a running sum
        # Let's use a prefix sum array
        # But since dp[0] is 1, prefix_sum[0] = 0, prefix_sum[1] = dp[0]
        # So prefix_sum[i] = dp[0] + ... + dp[i-1]
        # dp[right] = prefix_sum[right] - prefix_sum[left-1]
        # Let's build prefix_sum on the fly
        # But to save space, we can just keep a running sum
        
        last_occurrence[x] = right - 1
        
        # To avoid recomputing sum, maintain a running window sum
        # We'll keep a variable to store the sum of dp[left] to dp[right-1]
        # Let's use a variable window_sum
        # But since left only increases, we can update window_sum accordingly
        
        # We'll use prefix sums for clarity
        # prefix_sum[i] = dp[0] + ... + dp[i-1]
        # dp[right] = prefix_sum[right] - prefix_sum[left]
        # Let's build prefix_sum
        # prefix_sum[0] = 0
        # prefix_sum[1] = dp[0]
        # prefix_sum[2] = dp[0] + dp[1]
        # ...
        # So prefix_sum[i] = prefix_sum[i-1] + dp[i-1]
        
        # Let's build prefix_sum as we go
        # To avoid O(n^2), we need to update prefix_sum as we go
        # Let's initialize prefix_sum
        # We'll build prefix_sum as we go
        
        # For the first iteration, prefix_sum[0] = 0, prefix_sum[1] = dp[0] = 1
        # So for right = 1, left = 0, dp[1] = prefix_sum[1] - prefix_sum[0] = 1 - 0 = 1
        
        # Let's implement this
        
        # We'll keep prefix_sum as a list
        # prefix_sum[i] = dp[0] + ... + dp[i-1]
        # So prefix_sum[0] = 0
        # prefix_sum[1] = dp[0]
        # prefix_sum[2] = dp[0] + dp[1]
        # So for dp[right], we need prefix_sum[right] - prefix_sum[left]
        
        # Let's initialize prefix_sum
        # We'll append as we go
        # For dp[0], prefix_sum[0] = 0
        # For dp[1], prefix_sum[1] = dp[0]
        # For dp[2], prefix_sum[2] = dp[0] + dp[1]
        
        # Let's build prefix_sum as we go
        
        # We'll initialize prefix_sum with 0
        # For each right, we append prefix_sum[-1] + dp[right-1]
        
        # Let's do this outside the loop
        # But for efficiency, let's just keep prefix_sum as a variable
        
        # Actually, since we only need prefix_sum[right] and prefix_sum[left], we can keep prefix_sum as a list
        
        # Let's do this:
        # prefix_sum = [0]
        # for right in range(1, n+1):
        #     dp[right] = (prefix_sum[right-1] - prefix_sum[left-1]) % MOD
        #     prefix_sum.append((prefix_sum[-1] + dp[right]) % MOD)
        
        # Let's implement this
        
    prefix_sum = [0]
    for right in range(1, n + 1):
        x = arr[right - 1]
        if x in last_occurrence:
            left = max(left, last_occurrence[x] + 1)
        last_occurrence[x] = right - 1
        # dp[right] = prefix_sum[right-1] - prefix_sum[left-1]
        dp[right] = (prefix_sum[right - 1] - prefix_sum[left - 1]) % MOD
        prefix_sum.append((prefix_sum[-1] + dp[right]) % MOD)
    
    print(dp[n] % MOD)

if __name__ == "__main__":
    main()