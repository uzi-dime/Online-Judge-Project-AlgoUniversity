# CSES Problem: Shortest Subsequence
# Problem ID: 1087
# Generated on: 2025-07-22 20:33:09

import sys
import itertools

# Read input DNA sequence
s = sys.stdin.readline().strip()
n = len(s)
alphabet = ['A', 'C', 'G', 'T']

# Preprocess: for each character, store the next occurrence position for every index
next_pos = [[n] * 4 for _ in range(n + 2)]  # next_pos[i][c] = next position of char c after i-1

# Fill from the end
for i in range(n - 1, -1, -1):
    for j in range(4):
        next_pos[i][j] = next_pos[i + 1][j]
    # Update current character
    next_pos[i][alphabet.index(s[i])] = i

# Try all possible strings of increasing length
for length in range(1, 8):  # 4^7 = 16384, safe for n up to 1e6
    for comb in itertools.product(alphabet, repeat=length):
        t = ''.join(comb)
        # Check if t is a subsequence of s
        pos = 0
        found = True
        for ch in t:
            idx = alphabet.index(ch)
            if next_pos[pos][idx] == n:
                found = False
                break
            pos = next_pos[pos][idx] + 1
        if not found:
            print(t)
            sys.exit(0)