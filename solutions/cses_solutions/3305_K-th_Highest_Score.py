# CSES Problem: K-th Highest Score
# Problem ID: 3305
# Generated on: 2025-07-22 20:22:24

import sys

input = sys.stdin.readline
print_flush = lambda x: (print(x), sys.stdout.flush())

# Read n (number per country) and k (k-th highest overall)
n, k = map(int, input().split())

# Helper to query the i-th highest score from a country
def query(country, i):
    print_flush(f"{country} {i}")
    return int(input())

# Binary search:
# Let F[i] be the i-th highest in Finland, S[j] the j-th highest in Sweden.
# The k-th highest overall is the max x such that at least k scores >= x.
# We can binary search for x, and for each x, count how many scores >= x.

# To do this efficiently, we can precompute the full sorted list for each country
# by querying all n scores for each country (2n queries, <= 2*1e5 <= 1e5*2).
# But n can be up to 1e5, so that's too many queries.
# Instead, we can binary search for the answer, and for each candidate value,
# count how many scores in Finland and Sweden are >= x using binary search on
# the virtual sorted arrays (by querying only the needed indices).

# But since we can only ask for the i-th highest, we can do a "virtual" binary search
# on the sorted arrays by querying the median, etc.

# We'll do a binary search on the possible score values (1 to 1e9).
lo, hi = 1, 10**9

while lo < hi:
    mid = (lo + hi + 1) // 2  # Try for higher values first

    # For Finland: find how many scores >= mid
    # Binary search for the smallest i such that F[i] < mid
    l, r = 1, n
    finland_ge = 0
    while l <= r:
        m = (l + r) // 2
        val = query('F', m)
        if val >= mid:
            finland_ge = n - m + 1
            r = m - 1
        else:
            l = m + 1

    # For Sweden: same
    l, r = 1, n
    sweden_ge = 0
    while l <= r:
        m = (l + r) // 2
        val = query('S', m)
        if val >= mid:
            sweden_ge = n - m + 1
            r = m - 1
        else:
            l = m + 1

    total_ge = finland_ge + sweden_ge

    if total_ge >= k:
        lo = mid
    else:
        hi = mid - 1

# Output the answer
print_flush(f"! {lo}")