# CSES Problem: Tree Distances II
# Problem ID: 1133
# Generated on: 2025-07-22 20:32:54

import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

n = int(input())
tree = [[] for _ in range(n)]
for _ in range(n - 1):
    a, b = map(int, input().split())
    tree[a - 1].append(b - 1)
    tree[b - 1].append(a - 1)

# sum_dist[node]: sum of distances from node to all nodes in its subtree
# size[node]: size of subtree rooted at node
sum_dist = [0] * n
size = [1] * n

def dfs1(u, parent):
    for v in tree[u]:
        if v == parent:
            continue
        dfs1(v, u)
        size[u] += size[v]
        sum_dist[u] += sum_dist[v] + size[v]

dfs1(0, -1)

# ans[node]: sum of distances from node to all other nodes
ans = [0] * n
ans[0] = sum_dist[0]

def dfs2(u, parent):
    for v in tree[u]:
        if v == parent:
            continue
        # When moving root from u to v:
        # ans[v] = ans[u] - size[v] + (n - size[v])
        ans[v] = ans[u] - size[v] + (n - size[v])
        dfs2(v, u)

dfs2(0, -1)

print(' '.join(map(str, ans)))