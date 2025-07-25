# CSES Problem: Beautiful Permutation II
# Problem ID: 3175
# Generated on: 2025-07-22 20:34:01

# Read input
n = int(input())

# For n = 2 or 3, no solution exists
if n == 2 or n == 3:
    print("NO SOLUTION")
else:
    # Place all even numbers first, then odd numbers
    evens = list(range(2, n+1, 2))
    odds = list(range(1, n+1, 2))
    # Concatenate and print
    result = evens + odds
    print(' '.join(map(str, result)))