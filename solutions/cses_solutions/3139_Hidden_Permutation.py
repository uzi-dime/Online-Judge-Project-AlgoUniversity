# CSES Problem: Hidden Permutation
# Problem ID: 3139
# Generated on: 2025-07-22 20:22:02

import sys

def flush():
    sys.stdout.flush()

def ask(i, j):
    print(f"? {i} {j}")
    flush()
    return input().strip() == "YES"

def main():
    n = int(input())
    # Find the index of the maximum element (n)
    candidate = 1
    for i in range(2, n + 1):
        if ask(candidate, i):
            candidate = i

    # candidate now holds the index of the largest element (value n)
    ans = [0] * (n + 1)  # 1-based indexing

    ans[candidate] = n

    # Find the value for each other position
    for i in range(1, n + 1):
        if i == candidate:
            continue
        # If ai < an, then ai < n, so ai < candidate
        # We can binary search, but since only one value is left for each, just ask
        print(f"? {i} {candidate}")
        flush()
        res = input().strip()
        if res == "YES":
            # ai < n, so ai < candidate, so ai < n, so ai in [1, n-1]
            # But we don't know the exact value yet, so we will fill it later
            pass
        else:
            # ai > candidate, which is impossible since candidate is the largest
            # So ai < candidate always
            pass

    # Now, for each i != candidate, we can find its value by counting how many elements it's less than
    # For each i, count how many j (j != i) such that ai < aj
    for i in range(1, n + 1):
        if i == candidate:
            continue
        cnt = 0
        for j in range(1, n + 1):
            if i == j:
                continue
            print(f"? {i} {j}")
            flush()
            if input().strip() == "YES":
                cnt += 1
        ans[i] = cnt + 1  # Since values are from 1 to n

    # Output the answer
    print("! " + " ".join(str(ans[i]) for i in range(1, n + 1)))
    flush()

if __name__ == "__main__":
    main()