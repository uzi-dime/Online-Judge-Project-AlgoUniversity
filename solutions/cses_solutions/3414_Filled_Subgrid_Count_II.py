# CSES Problem: Filled Subgrid Count II
# Problem ID: 3414
# Generated on: 2025-07-22 20:29:19

import sys
import threading

def main():
    import sys

    sys.setrecursionlimit(1 << 25)
    n, k = map(int, sys.stdin.readline().split())
    grid = [sys.stdin.readline().strip() for _ in range(n)]
    letters = [chr(ord('A') + i) for i in range(k)]
    result = [0] * k

    # For each letter, process the grid
    for idx, ch in enumerate(letters):
        # For each cell, compute the height of consecutive ch's above (including itself)
        height = [0] * n
        for top in range(n):
            # Reset height for each new top row
            for col in range(n):
                height[col] = 0
            for bottom in range(top, n):
                for col in range(n):
                    if grid[bottom][col] == ch:
                        height[col] += 1
                    else:
                        height[col] = 0
                # Now, for this row segment (top..bottom), count rectangles
                # Each contiguous segment of height[col] == (bottom-top+1) forms rectangles
                width = 0
                for col in range(n):
                    if height[col] == (bottom - top + 1):
                        width += 1
                        result[idx] += width
                    else:
                        width = 0

    for val in result:
        print(val)

threading.Thread(target=main).start()