# CSES Problem: Knight Moves Queries
# Problem ID: 3218
# Generated on: 2025-07-22 20:36:44

import sys
import threading

def main():
    import sys

    sys.setrecursionlimit(1 << 25)
    n = int(sys.stdin.readline())
    queries = [tuple(map(int, sys.stdin.readline().split())) for _ in range(n)]

    # Memoization for fast repeated queries
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def min_knight_moves(x, y):
        # Convert to 0-based and use symmetry
        x, y = abs(x - 1), abs(y - 1)
        if x < y:
            x, y = y, x
        # Base cases
        if x == 0 and y == 0:
            return 0
        if x == 1 and y == 0:
            return 3
        if x == 2 and y == 2:
            return 4
        if x == 1 and y == 1:
            return 2
        if x == 2 and y == 0:
            return 2
        if x == 2 and y == 1:
            return 1
        # General case: try two moves that get closer to (0,0)
        return 1 + min(
            min_knight_moves(x - 2, y - 1),
            min_knight_moves(x - 1, y - 2)
        )

    for x, y in queries:
        print(min_knight_moves(x, y))

threading.Thread(target=main).start()