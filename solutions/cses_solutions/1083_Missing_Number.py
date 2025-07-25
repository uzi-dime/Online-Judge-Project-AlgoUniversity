# CSES Problem: Missing Number
# Problem ID: 1083
# Generated on: 2025-07-22 20:34:21

# Read input efficiently
import sys

n = int(sys.stdin.readline())
numbers = list(map(int, sys.stdin.readline().split()))

# Calculate expected sum of 1..n
expected_sum = n * (n + 1) // 2

# Calculate actual sum of given numbers
actual_sum = sum(numbers)

# The missing number is the difference
print(expected_sum - actual_sum)