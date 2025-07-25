# CSES Problem: Josephus Queries
# Problem ID: 2164
# Generated on: 2025-07-22 20:26:02

import sys

input = sys.stdin.readline

# For each query, we need to find the k-th child removed in the Josephus problem with step=2.
# We can simulate the removal order recursively:
# - For n children, the removal order is:
#   - Remove all even positions in order (2, 4, 6, ...)
#   - Then recursively remove from the remaining (odd positions, renumbered)
# To find the k-th removed child, we can use recursion or iteration.

def find_kth_removed(n, k):
    # We want the k-th removed child in Josephus(n, 2)
    # The removal order is:
    # 1st: 2
    # 2nd: 4
    # ...
    # n//2-th: largest even <= n
    # Then, recursively, the rest are the Josephus(n - n//2, 2) on the odd positions
    # The mapping from the recursive call to the original positions:
    # If n is even: odd positions are 1,3,5,...,n-1
    # If n is odd: odd positions are 1,3,5,...,n

    if k <= n // 2:
        # k-th removed is the k-th even number
        return 2 * k
    else:
        # After removing all evens, the remaining are the odds, renumbered 1..n-n//2
        # The (k - n//2)-th removed in the new group maps to the (2 * pos - 1) in the original
        # So, recursively find the position in the reduced problem
        pos = find_kth_removed(n - n // 2, k - n // 2)
        return 2 * pos - 1

q = int(sys.stdin.readline())
res = []
for _ in range(q):
    n, k = map(int, sys.stdin.readline().split())
    res.append(str(find_kth_removed(n, k)))
print('\n'.join(res))