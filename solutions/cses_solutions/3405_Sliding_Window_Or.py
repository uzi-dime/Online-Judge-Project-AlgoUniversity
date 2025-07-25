# CSES Problem: Sliding Window Or
# Problem ID: 3405
# Generated on: 2025-07-22 20:23:38

import sys
import threading
from collections import deque

def main():
    import sys

    input = sys.stdin.readline

    n, k = map(int, sys.stdin.readline().split())
    x, a, b, c = map(int, sys.stdin.readline().split())

    # Generator for the sequence
    arr = [0] * n
    arr[0] = x
    for i in range(1, n):
        arr[i] = (a * arr[i-1] + b) % c

    # For each window, compute bitwise OR efficiently
    # Use a deque to maintain indices of elements that contribute to the current window's OR
    # For each bit position, maintain the rightmost index where the bit is set in the window

    # To optimize, for each bit, keep a queue of indices where that bit is set
    bit_queues = [deque() for _ in range(32)]
    window_or = 0
    result = 0

    # Initialize the first window
    for i in range(k):
        val = arr[i]
        for bit in range(32):
            if (val >> bit) & 1:
                bit_queues[bit].append(i)
    # Compute OR for the first window
    for bit in range(32):
        if bit_queues[bit]:
            window_or |= (1 << bit)
    result ^= window_or

    # Slide the window
    for i in range(k, n):
        out_idx = i - k
        val_in = arr[i]
        val_out = arr[out_idx]
        # Add new value
        for bit in range(32):
            if (val_in >> bit) & 1:
                bit_queues[bit].append(i)
        # Remove old value if it's out of window
        for bit in range(32):
            while bit_queues[bit] and bit_queues[bit][0] <= out_idx:
                bit_queues[bit].popleft()
        # Compute OR for current window
        window_or = 0
        for bit in range(32):
            if bit_queues[bit]:
                window_or |= (1 << bit)
        result ^= window_or

    print(result)

threading.Thread(target=main).start()