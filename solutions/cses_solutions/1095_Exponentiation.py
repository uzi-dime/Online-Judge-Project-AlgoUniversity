# CSES Problem: Exponentiation
# Problem ID: 1095
# Generated on: 2025-07-22 20:26:08

import sys

MOD = 10**9 + 7

def main():
    input = sys.stdin.readline
    n = int(input())
    results = []
    for _ in range(n):
        a_str, b_str = input().split()
        a = int(a_str)
        b = int(b_str)
        # Handle special cases
        if a == 0 and b == 0:
            results.append("1")
        elif b == 0:
            results.append("1")
        elif a == 0:
            results.append("0")
        else:
            results.append(str(pow(a, b, MOD)))
    print('\n'.join(results))

if __name__ == "__main__":
    main()