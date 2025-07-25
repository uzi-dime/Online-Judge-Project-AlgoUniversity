# CSES Problem: Sliding Window Sum
# Problem ID: 3220
# Generated on: 2025-07-22 20:23:02

import sys
import threading

def main():
    import sys

    input = sys.stdin.readline

    n, k = map(int, sys.stdin.readline().split())
    x, a, b, c = map(int, sys.stdin.readline().split())

    # Generate the array on the fly, only store the last k elements for the window
    window = [0] * k
    window_sum = 0
    xor_result = 0

    # Generate first k elements and fill the window
    xi = x
    for i in range(k):
        window[i] = xi
        window_sum += xi
        if i != k - 1:
            xi = (a * xi + b) % c

    xor_result ^= window_sum

    # Slide the window through the rest of the array
    for i in range(k, n):
        xi = (a * xi + b) % c
        out_idx = i % k
        window_sum += xi - window[out_idx]
        window[out_idx] = xi
        xor_result ^= window_sum

    print(xor_result)

threading.Thread(target=main).start()