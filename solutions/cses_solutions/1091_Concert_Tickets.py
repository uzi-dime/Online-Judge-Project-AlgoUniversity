# CSES Problem: Concert Tickets
# Problem ID: 1091
# Generated on: 2025-07-22 20:20:35

import sys
import bisect

# Read input efficiently
input = sys.stdin.readline

n, m = map(int, input().split())
ticket_prices = list(map(int, input().split()))
customer_offers = list(map(int, input().split()))

# Sort ticket prices for binary search
ticket_prices.sort()

# We'll use a list to simulate a multiset with bisect for efficient search and removal
from bisect import bisect_right

# Output list for answers
answers = []

for offer in customer_offers:
    # Find the rightmost ticket price <= offer
    idx = bisect_right(ticket_prices, offer) - 1
    if idx >= 0:
        answers.append(str(ticket_prices[idx]))
        # Remove the ticket (O(n), but acceptable with PyPy and only for used tickets)
        ticket_prices.pop(idx)
    else:
        answers.append("-1")

print('\n'.join(answers))