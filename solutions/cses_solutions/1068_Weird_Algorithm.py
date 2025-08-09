# CSES Problem: Weird Algorithm
# Problem ID: 1068
# Generated on: 2025-07-30 22:00:34

import sys

def solve():
    n = int(sys.stdin.readline())
    
    # Print the initial value of n
    print(n, end=" ")
    
    # Continue the process until n becomes 1
    while n != 1:
        if n % 2 == 0:
            # If n is even, divide it by two
            n //= 2
        else:
            # If n is odd, multiply it by three and add one
            n = 3 * n + 1
        
        # Print the new value of n, followed by a space
        print(n, end=" ")
    
    # Print a newline character at the end of the output
    print()

solve()