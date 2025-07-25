# CSES Problem: String Matching
# Problem ID: 1753
# Generated on: 2025-07-22 20:24:12

# Efficient pattern matching using KMP algorithm

import sys

def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of the previous longest prefix suffix

    # lps[0] is always 0, so start from 1
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_count(text, pattern):
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    count = 0
    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                count += 1
                j = lps[j - 1]  # Continue searching for next match
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return count

def main():
    # Read input efficiently
    text = sys.stdin.readline().strip()
    pattern = sys.stdin.readline().strip()
    print(kmp_count(text, pattern))

if __name__ == "__main__":
    main()