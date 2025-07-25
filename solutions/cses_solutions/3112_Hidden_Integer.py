# CSES Problem: Hidden Integer
# Problem ID: 3112
# Generated on: 2025-07-22 20:21:42

import sys

def main():
    # Define the search range
    low = 1
    high = 10**9

    # Binary search for the hidden integer x
    while low < high:
        mid = (low + high) // 2
        # Ask if x > mid
        print(f"? {mid}", flush=True)
        response = input().strip()
        if response == "YES":
            # x > mid
            low = mid + 1
        else:
            # x <= mid
            high = mid

    # Found the hidden integer x
    print(f"! {low}", flush=True)

if __name__ == "__main__":
    main()