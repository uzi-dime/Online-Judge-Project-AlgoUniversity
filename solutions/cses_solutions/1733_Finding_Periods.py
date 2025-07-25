# CSES Problem: Finding Periods
# Problem ID: 1733
# Generated on: 2025-07-22 20:24:28

import sys

def compute_prefix_function(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def main():
    s = sys.stdin.readline().strip()
    n = len(s)
    pi = compute_prefix_function(s)
    res = []
    k = n
    while k > 0:
        res.append(k)
        k = pi[k - 1]
    print(' '.join(map(str, sorted(res))))

if __name__ == "__main__":
    main()