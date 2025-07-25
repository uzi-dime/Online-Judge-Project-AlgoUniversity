# CSES Problem: Subordinates
# Problem ID: 1674
# Generated on: 2025-07-22 20:32:15

import sys
import threading

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    n = int(sys.stdin.readline())
    boss = list(map(int, sys.stdin.readline().split()))
    
    # Build the tree as adjacency list
    children = [[] for _ in range(n + 1)]
    for i, b in enumerate(boss, start=2):
        children[b].append(i)
    
    # Array to store the number of subordinates for each employee
    subordinates = [0] * (n + 1)
    
    # Iterative DFS to avoid recursion limit
    stack = [(1, 0)]  # (node, 0=enter, 1=exit)
    order = []
    while stack:
        node, typ = stack.pop()
        if typ == 0:
            stack.append((node, 1))
            for child in children[node]:
                stack.append((child, 0))
        else:
            cnt = 0
            for child in children[node]:
                cnt += subordinates[child] + 1
            subordinates[node] = cnt

    print(' '.join(str(subordinates[i]) for i in range(1, n + 1)))

threading.Thread(target=main).start()