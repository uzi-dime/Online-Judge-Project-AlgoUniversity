# CSES Problem: Permuted Binary Strings
# Problem ID: 3228
# Generated on: 2025-07-22 20:22:35

import sys

def main():
    input = sys.stdin.readline
    print_flush = lambda x: (print(x), sys.stdout.flush())

    n = int(input())
    # We'll use bitmasking: for each bit position, ask a query with that bit set for each index.
    # For each bit position, we can reconstruct the permutation.

    max_bit = n.bit_length()
    responses = []
    for bit in range(max_bit):
        # Build query: set b_i = 1 if i-th index has this bit set, else 0
        query = ['0'] * n
        for i in range(n):
            if (i >> bit) & 1:
                query[i] = '1'
        print_flush('?' + ' ' + ''.join(query))
        resp = input().strip()
        responses.append(resp)

    # For each position in the response, reconstruct the original index
    perm = [0] * n
    for pos in range(n):
        idx = 0
        for bit in range(max_bit):
            if responses[bit][pos] == '1':
                idx |= (1 << bit)
        # idx is 0-based, but permutation is 1-based
        perm[pos] = idx + 1

    print_flush('!' + ' ' + ' '.join(map(str, perm)))

if __name__ == "__main__":
    main()