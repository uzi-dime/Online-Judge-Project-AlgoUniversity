# CSES Problem: Counting Bits
# Problem ID: 1146
# Generated on: 2025-07-22 20:30:22

# Efficiently count the total number of '1' bits in binary representations of all numbers from 1 to n

def count_ones(n):
    total = 0
    i = 0
    while (1 << i) <= n:
        # For each bit position i:
        # Count how many full cycles of 0..1 there are in this bit position
        cycle_len = 1 << (i + 1)
        full_cycles = n // cycle_len
        ones_in_full_cycles = full_cycles * (cycle_len // 2)
        # Count ones in the last (possibly incomplete) cycle
        remainder = n % cycle_len
        ones_in_remainder = max(0, remainder - (cycle_len // 2) + 1)
        total += ones_in_full_cycles + ones_in_remainder
        i += 1
    return total

n = int(input())
print(count_ones(n))