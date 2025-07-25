# CSES Problem: Exponentiation II
# Problem ID: 1712
# Generated on: 2025-07-22 20:26:18

import sys

# Constants
MOD = 10**9 + 7

def main():
    import sys
    input = sys.stdin.readline

    n = int(input())
    results = []

    for _ in range(n):
        a_str, b_str, c_str = input().split()
        a = int(a_str)
        b = int(b_str)
        c = int(c_str)

        # Handle special case: 0^0 = 1
        if a == 0 and b == 0:
            results.append(1)
            continue

        # Compute exponent: b^c mod (MOD-1) using Fermat's little theorem
        # Since pow(a, k, MOD) cycles every MOD-1 (when MOD is prime)
        if b == 0 and c == 0:
            exp = 1
        elif b == 0:
            exp = 0
        elif c == 0:
            exp = 1
        else:
            exp = pow(b, c, MOD-1)
        results.append(pow(a, exp, MOD))

    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    main()