# CSES Problem: Inverse Inversions
# Problem ID: 2214
# Generated on: 2025-07-22 20:37:26

import sys

def main():
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    res = []
    left = 1
    right = n

    # Greedy: Place the largest possible number at each step to create inversions
    for i in range(1, n + 1):
        # If placing 'right' at current position creates at most k inversions, do it
        if k >= right - left:
            res.append(right)
            k -= (right - left)
            right -= 1
        else:
            res.append(left)
            left += 1

    print(' '.join(map(str, res)))

if __name__ == "__main__":
    main()