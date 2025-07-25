# CSES Problem: Weird Algorithm
# Problem ID: 1068
# Generated on: 2025-07-22 20:34:13

# Read input
n = int(input())

# Store the sequence in a list for efficient output
sequence = []

while True:
    sequence.append(str(n))
    if n == 1:
        break
    if n % 2 == 0:
        n //= 2
    else:
        n = n * 3 + 1

# Print the sequence as a single line
print(' '.join(sequence))