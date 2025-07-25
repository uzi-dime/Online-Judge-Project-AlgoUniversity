# CSES Problem: Removing Digits
# Problem ID: 1637
# Generated on: 2025-07-22 20:21:28

# Read the input as a string to handle very large numbers
n = input().strip()

# Initialize a counter for steps
steps = 0

# Loop until n becomes '0'
while n != '0':
    # Find the maximum digit in the current number
    max_digit = max(map(int, n))
    # Subtract the maximum digit from n
    n = str(int(n) - max_digit)
    steps += 1

print(steps)