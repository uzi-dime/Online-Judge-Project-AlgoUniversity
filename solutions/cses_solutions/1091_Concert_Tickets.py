# CSES Problem: Concert Tickets
# Problem ID: 1091
# Generated on: 2025-07-30 22:05:26

import sys
import bisect

def solve():
    n, m = map(int, sys.stdin.readline().split())
    tickets = list(map(int, sys.stdin.readline().split()))
    customers = list(map(int, sys.stdin.readline().split()))

    tickets.sort()
    result = []
    for price in customers:
        # Find insertion point where price could be inserted to keep tickets sorted
        idx = bisect.bisect_right(tickets, price)
        if idx == 0:
            # No ticket <= price
            result.append(-1)
        else:
            # Ticket at idx-1 is the best available for this customer
            result.append(tickets[idx-1])
            # Remove sold ticket
            tickets.pop(idx-1)

    print('\n'.join(map(str, result)))


if __name__ == "__main__":
    solve()
