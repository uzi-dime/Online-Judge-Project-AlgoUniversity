# CSES Problem: Repetitions
# Problem ID: 1069
# Generated on: 2025-07-30 22:00:50

import sys

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)

    if n == 0:
        print(0)
        return

    max_length = 0
    current_length = 0
    current_char = ''

    for char in s:
        if char == current_char:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_char = char
            current_length = 1

    # After the loop, we need to check the last repetition
    max_length = max(max_length, current_length)

    print(max_length)

if __name__ == "__main__":
    solve()