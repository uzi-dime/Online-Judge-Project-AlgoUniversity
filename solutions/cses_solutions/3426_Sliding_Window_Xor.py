# CSES Problem: Sliding Window Xor
# Problem ID: 3426
# Generated on: 2025-07-22 20:23:23

import sys
import threading

def main():
    import sys

    input = sys.stdin.readline

    n, k = map(int, sys.stdin.readline().split())
    x, a, b, c = map(int, sys.stdin.readline().split())

    # Generate the array on the fly, keep only the last k elements for the window
    window = [0] * k
    xi = x
    for i in range(k):
        window[i] = xi
        xi = (a * xi + b) % c

    # Compute the xor for the first window
    curr_xor = 0
    for v in window:
        curr_xor ^= v

    result = curr_xor

    # Slide the window
    for i in range(k, n):
        # Remove window[i - k], add xi
        out_elem = window[i % k]
        in_elem = xi
        curr_xor ^= out_elem
        curr_xor ^= in_elem
        window[i % k] = in_elem
        result ^= curr_xor
        xi = (a * xi + b) % c

    print(result)

threading.Thread(target=main).start()