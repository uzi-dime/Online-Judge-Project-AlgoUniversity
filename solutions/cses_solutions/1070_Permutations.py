# CSES Problem: Permutations
# Problem ID: 1070
# Generated on: 2025-07-22 20:34:44

# Read input
n = int(input())

# For n = 2 or 3, no solution exists
if n == 2 or n == 3:
    print("NO SOLUTION")
else:
    # Print even numbers first, then odd numbers
    evens = list(range(2, n+1, 2))
    odds = list(range(1, n+1, 2))
    print(' '.join(map(str, evens + odds)))