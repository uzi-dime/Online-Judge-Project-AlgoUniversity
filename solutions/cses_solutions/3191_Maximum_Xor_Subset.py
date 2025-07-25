# CSES Problem: Maximum Xor Subset
# Problem ID: 3191
# Generated on: 2025-07-22 20:30:46

import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))
    
    # Basis for the linear basis (max 31 bits for 0 <= xi <= 1e9)
    basis = [0] * 31
    
    for num in arr:
        for i in reversed(range(31)):
            if num & (1 << i):
                if not basis[i]:
                    basis[i] = num
                    break
                num ^= basis[i]
    
    # The answer is obtained by XORing basis elements greedily
    res = 0
    for i in reversed(range(31)):
        if (res ^ basis[i]) > res:
            res ^= basis[i]
    print(res)

if __name__ == "__main__":
    main()