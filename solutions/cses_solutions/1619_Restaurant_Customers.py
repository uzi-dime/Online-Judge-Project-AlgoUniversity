# CSES Problem: Restaurant Customers
# Problem ID: 1619
# Generated on: 2025-07-22 20:20:43

import sys

# Read all input at once for efficiency
input = sys.stdin.read
data = input().split()

n = int(data[0])
events = []

# Collect all arrival and leaving events
for i in range(n):
    a = int(data[1 + 2 * i])
    b = int(data[2 + 2 * i])
    events.append((a, 1))  # arrival: +1 customer
    events.append((b, -1)) # leaving: -1 customer

# Sort events: by time; arrivals (+1) before departures (-1) if same time
events.sort()

current = 0
maximum = 0

# Sweep through events, tracking current number of customers
for _, change in events:
    current += change
    if current > maximum:
        maximum = current

print(maximum)