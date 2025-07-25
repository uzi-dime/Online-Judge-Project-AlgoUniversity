# CSES Problem: K Subset Xors
# Problem ID: 3192
# Generated on: 2025-07-22 20:31:08

import sys
import threading
import heapq

def main():
    import sys
    input = sys.stdin.readline

    n, k = map(int, sys.stdin.readline().split())
    arr = list(map(int, sys.stdin.readline().split()))

    # Step 1: Build the xor basis (linear basis over GF(2))
    basis = []
    for x in arr:
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x)
    basis.sort()

    # Step 2: Generate the k smallest subset xors using a min-heap
    # Each subset xor can be represented as a sum of basis elements with 0/1 coefficients
    # We use a heap to generate them in order

    # If the basis is empty, only 0 is possible
    if not basis:
        print('0' * k if k == 1 else ' '.join(['0'] * k))
        return

    m = len(basis)
    heap = []
    visited = set()

    # Start with 0 (empty subset)
    heapq.heappush(heap, (0, 0))  # (xor_value, mask)
    visited.add(0)

    res = []
    while len(res) < k and heap:
        val, mask = heapq.heappop(heap)
        res.append(val)
        for i in range(m):
            nmask = mask | (1 << i)
            if nmask not in visited:
                nval = val ^ basis[i]
                heapq.heappush(heap, (nval, nmask))
                visited.add(nmask)

    # Output
    print(' '.join(map(str, sorted(res)[:k])))

threading.Thread(target=main).start()