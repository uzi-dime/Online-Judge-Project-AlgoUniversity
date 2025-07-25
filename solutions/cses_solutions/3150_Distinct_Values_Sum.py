# CSES Problem: Distinct Values Sum
# Problem ID: 3150
# Generated on: 2025-07-22 20:33:20

import sys
import threading

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    n = int(sys.stdin.readline())
    x = list(map(int, sys.stdin.readline().split()))

    last_occurrence = dict()
    total = 0
    prev = 0

    # For each right end b, count the number of subarrays ending at b
    # where x[b] is a new unique element in the subarray.
    for i in range(n):
        # If x[i] was last seen at position j, then subarrays starting after j
        # will have x[i] as a new unique element.
        # So, number of such subarrays is (i - last_occurrence[x[i]])
        last = last_occurrence.get(x[i], -1)
        prev += i - last
        total += prev
        last_occurrence[x[i]] = i

    print(total)

threading.Thread(target=main).start()