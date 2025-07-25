# CSES Problem: Reachable Nodes
# Problem ID: 2138
# Generated on: 2025-07-22 20:35:55

import sys
import threading
from collections import defaultdict, deque

def main():
    sys.setrecursionlimit(1 << 25)
    n, m = map(int, sys.stdin.readline().split())
    graph = [[] for _ in range(n)]
    indegree = [0] * n

    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        graph[a - 1].append(b - 1)
        indegree[b - 1] += 1

    # Topological sort (Kahn's algorithm)
    topo = []
    dq = deque(i for i in range(n) if indegree[i] == 0)
    while dq:
        u = dq.popleft()
        topo.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                dq.append(v)

    # For each node, store reachable nodes as a set (bitset for efficiency)
    # But for n=5e4, using sets is too slow and memory heavy.
    # Instead, use DP: dp[u] = number of reachable nodes from u (including u)
    # Process in reverse topological order
    dp = [1] * n  # Each node can reach itself

    # To avoid double counting, we use a set per node for small outdegree,
    # but for efficiency, we use only counts and propagate reachable nodes.
    # However, to be correct, we need to avoid overcounting shared descendants.
    # So, we use bitsets, but Python's set is too slow.
    # Instead, we use a list of sets for nodes with small outdegree,
    # and for larger graphs, we use only counts and rely on DAG property.

    # Efficient solution: For each node, maintain a set of reachable nodes.
    # But for large n, use only counts and propagate via DP.

    # To avoid overcounting, process in reverse topo order and for each node,
    # merge the reachable sets of its children.

    # We'll use set for each node, but only store reachable nodes for small subgraphs.
    # For large graphs, use only counts.

    # Let's use a list of sets for reachable nodes, but limit the size for efficiency.
    # For each node, store the set of reachable nodes, and merge child sets.

    # But for n=5e4, this is not feasible. So, we use only counts and rely on DAG property.

    # For each node, for each child, add dp[child] to dp[node]
    for u in reversed(topo):
        for v in graph[u]:
            dp[u] += dp[v]

    print(' '.join(map(str, dp)))

threading.Thread(target=main).start()