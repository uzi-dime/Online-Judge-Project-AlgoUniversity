# CSES Problem: Missing Number
# Problem ID: 1083
# Generated on: 2025-07-30 22:00:42

import sys

def solve():
    n = int(sys.stdin.readline())
    numbers = list(map(int, sys.stdin.readline().split()))

    # The sum of numbers from 1 to n is n * (n + 1) // 2
    expected_sum = n * (n + 1) // 2

    # The sum of the given n-1 numbers
    actual_sum = sum(numbers)

    # The missing number is the difference between the expected sum and the actual sum
    missing_number = expected_sum - actual_sum
    print(missing_number)

if __name__ == "__main__":
    solve()