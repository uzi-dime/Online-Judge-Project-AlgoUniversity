# CSES Problem: Hamming Distance
# Problem ID: 2136
# Generated on: 2025-07-22 20:35:13

import sys

# Read input
input = sys.stdin.readline
n, k = map(int, input().split())
bit_strings = [int(input().strip(), 2) for _ in range(n)]

# Use a set to check for duplicates (distance 0)
seen = set()
for b in bit_strings:
    if b in seen:
        print(0)
        sys.exit(0)
    seen.add(b)

# Sort for efficient neighbor comparison
bit_strings.sort()

# Function to compute Hamming distance between two bitmasks
def hamming(a, b):
    return bin(a ^ b).count('1')

min_dist = k + 1

# Compare each string with its next 10 neighbors (empirically enough for random bitstrings)
for i in range(n):
    for j in range(i+1, min(i+11, n)):
        d = hamming(bit_strings[i], bit_strings[j])
        if d < min_dist:
            min_dist = d
        if min_dist == 1:
            print(1)
            sys.exit(0)

print(min_dist)