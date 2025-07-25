# CSES Problem: Minimal Rotation
# Problem ID: 1110
# Generated on: 2025-07-22 20:24:37

# Booth's Algorithm for Lexicographically Minimal String Rotation
import sys

def minimal_rotation(s):
    s += s  # Concatenate string to itself
    n = len(s) // 2
    f = [-1] * len(s)
    k = 0  # Least rotation of string found so far
    for j in range(1, len(s)):
        i = f[j - k - 1]
        while i != -1 and s[j] != s[k + i + 1]:
            if s[j] < s[k + i + 1]:
                k = j - i - 1
            i = f[i]
        if i == -1 and s[j] != s[k]:
            if s[j] < s[k]:
                k = j
            f[j - k] = -1
        else:
            f[j - k] = i + 1
    return s[k:k + n]

if __name__ == "__main__":
    s = sys.stdin.readline().strip()
    print(minimal_rotation(s))