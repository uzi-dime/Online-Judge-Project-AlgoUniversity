# CSES Problem: Repetitions
# Problem ID: 1069
# Generated on: 2025-07-22 20:34:29

# Read the DNA sequence from standard input
s = input().strip()

# Initialize variables to track the current and maximum repetition lengths
max_len = 1
curr_len = 1

# Iterate through the string, comparing each character to the previous one
for i in range(1, len(s)):
    if s[i] == s[i - 1]:
        curr_len += 1
        if curr_len > max_len:
            max_len = curr_len
    else:
        curr_len = 1

print(max_len)