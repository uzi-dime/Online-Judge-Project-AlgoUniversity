# CSES Problem: Finding Borders
# Problem ID: 1732
# Generated on: 2025-07-22 20:24:20

# Efficient solution using prefix function (KMP failure function)
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
    pi = compute_prefix_function(s)
    borders = []
    k = pi[-1]
    while k > 0:
        borders.append(k)
        k = pi[k - 1]
    borders.reverse()
    print(' '.join(map(str, borders)))

if __name__ == "__main__":
    main()