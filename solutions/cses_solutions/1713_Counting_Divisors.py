# CSES Problem: Counting Divisors
# Problem ID: 1713
# Generated on: 2025-07-22 20:26:25

import sys

# Read all input at once for efficiency
input = sys.stdin.read
data = input().split()

n = int(data[0])
xs = list(map(int, data[1:]))

MAX_X = 10**6

# Precompute number of divisors for every number up to MAX_X
divisors = [0] * (MAX_X + 1)
for i in range(1, MAX_X + 1):
    for j in range(i, MAX_X + 1, i):
        divisors[j] += 1

# Output the number of divisors for each input number
output = []
for x in xs:
    output.append(str(divisors[x]))

print('\n'.join(output))