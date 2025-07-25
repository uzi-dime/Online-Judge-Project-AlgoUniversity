# CSES Problem: Distinct Numbers
# Problem ID: 1621
# Generated on: 2025-07-22 20:20:10

# Read input efficiently
import sys

n_and_rest = sys.stdin.read().split()
n = int(n_and_rest[0])
numbers = map(int, n_and_rest[1:])

# Use a set to store distinct values
distinct_values = set(numbers)

# Output the number of distinct values
print(len(distinct_values))