# CSES Problem: Colored Chairs
# Problem ID: 3273
# Generated on: 2025-07-22 20:22:47

import sys

def flush():
    sys.stdout.flush()

def ask(i):
    print(f"? {i}")
    flush()
    return sys.stdin.readline().strip()

def report(i):
    print(f"! {i}")
    flush()
    exit(0)

def main():
    n = int(sys.stdin.readline())
    # We'll sample chairs at regular intervals to maximize coverage with minimal queries.
    # Since n is odd, n//2 + 1 is enough to guarantee a pair.
    # Let's sample every k-th chair, where k = n // 20 (since 20 queries max).
    max_queries = 20
    step = max(1, n // max_queries)
    checked = []
    colors = dict()
    for i in range(1, n+1, step):
        c = ask(i)
        checked.append(i)
        colors[i] = c
        nxt = i + 1 if i < n else 1
        if nxt in colors:
            if colors[nxt] == c:
                report(i)
        else:
            c2 = ask(nxt)
            colors[nxt] = c2
            if c2 == c:
                report(i)
        if len(colors) >= max_queries * 2:
            break

    # If not found, do a linear scan for the rest (should not happen in practice)
    prev = None
    prev_color = None
    for i in range(1, n+2):
        idx = i if i <= n else 1
        if idx not in colors:
            c = ask(idx)
            colors[idx] = c
        else:
            c = colors[idx]
        if prev is not None and c == prev_color:
            report(prev)
        prev = idx
        prev_color = c

main()