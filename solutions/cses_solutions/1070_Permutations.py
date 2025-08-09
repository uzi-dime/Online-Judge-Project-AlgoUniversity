# CSES Problem: Permutations
# Problem ID: 1070
# Generated on: 2025-07-30 22:01:05

import sys

def solve():
    n = int(sys.stdin.readline())

    if n == 2 or n == 3:
        print("NO SOLUTION")
        return

    # For n=1, the permutation is [1] which is beautiful.
    # For n=4, we can have [2, 4, 1, 3] or [3, 1, 4, 2].
    # The general strategy is to print all even numbers first, then all odd numbers.
    # This ensures that no two adjacent numbers have a difference of 1,
    # except possibly between the last even number and the first odd number,
    # and the last odd number and the first even number (if n is even).

    # Print even numbers from n down to 2
    for i in range(n, 0, -2):
        if i % 2 == 0:
            sys.stdout.write(str(i) + " ")

    # Print odd numbers from n-1 down to 1
    for i in range(n, 0, -2):
        if i % 2 != 0:
            sys.stdout.write(str(i) + " ")
    sys.stdout.write("\n")

solve()