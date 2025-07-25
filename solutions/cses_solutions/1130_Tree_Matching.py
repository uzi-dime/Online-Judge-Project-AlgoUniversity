# CSES Problem: Tree Matching
# Problem ID: 1130
# Generated on: 2025-07-22 20:32:26

import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

n = int(input())
edges = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges[a].append(b)
    edges[b].append(a)

# dp[u][0]: max matching in subtree rooted at u, u is not matched
# dp[u][1]: max matching in subtree rooted at u, u is matched with one of its children
dp = [[0, 0] for _ in range(n + 1)]

def dfs(u, parent):
    total = 0
    for v in edges[u]:
        if v == parent:
            continue
        dfs(v, u)
        total += max(dp[v][0], dp[v][1])
    dp[u][0] = total
    for v in edges[u]:
        if v == parent:
            continue
        # Try matching u with v
        candidate = 1 + dp[v][0] + (total - max(dp[v][0], dp[v][1]))
        dp[u][1] = max(dp[u][1], candidate)

dfs(1, 0)
print(max(dp[1][0], dp[1][1]))