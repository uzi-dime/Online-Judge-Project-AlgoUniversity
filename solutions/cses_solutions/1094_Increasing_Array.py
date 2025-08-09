# CSES Problem: Increasing Array
# Problem ID: 1094
# Generated on: 2025-07-30 22:00:57

import sys

def solve():
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    moves = 0
    # Iterate through the array starting from the second element
    # We want to ensure a[i] >= a[i-1]
    for i in range(1, n):
        if a[i] < a[i-1]:
            # If the current element is smaller than the previous one,
            # we need to increase it to be at least equal to the previous one.
            # The number of moves required is the difference.
            diff = a[i-1] - a[i]
            moves += diff
            # Update the current element to satisfy the increasing condition
            a[i] = a[i-1]
    
    print(moves)

solve()