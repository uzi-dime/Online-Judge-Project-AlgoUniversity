# CSES Problem: Restaurant Customers
# Problem ID: 1619
# Generated on: 2025-07-30 22:05:33

import sys

def solve():
    n = int(sys.stdin.readline())
    events = []
    for _ in range(n):
        a, b = map(int, sys.stdin.readline().split())
        # Arrival event: +1 customer
        events.append((a, 1))
        # Leaving event: -1 customer
        events.append((b, -1))

    # Sort events by time. If times are equal, process arrivals before departures.
    # This is crucial because if a customer arrives at time t and another leaves at time t,
    # the arriving customer is considered to be in the restaurant at time t.
    # The problem statement guarantees distinct arrival and leaving times,
    # so this tie-breaking rule is not strictly necessary based on the constraints,
    # but it's a good general practice for this type of problem.
    events.sort()

    current_customers = 0
    max_customers = 0

    for time, type in events:
        current_customers += type
        max_customers = max(max_customers, current_customers)

    print(max_customers)

if __name__ == "__main__":
    solve()