# CSES Problem: Word Combinations
# Problem ID: 1731
# Generated on: 2025-07-22 20:24:00

import sys
import threading

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    MOD = 10**9 + 7

    s = sys.stdin.readline().strip()
    n = len(s)
    k = int(sys.stdin.readline())
    words = [sys.stdin.readline().strip() for _ in range(k)]

    # Build a trie for fast prefix matching
    class TrieNode:
        __slots__ = ['children', 'is_end']
        def __init__(self):
            self.children = dict()
            self.is_end = False

    root = TrieNode()
    for word in words:
        node = root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(n):
        node = root
        j = i
        while j < n and s[j] in node.children:
            node = node.children[s[j]]
            j += 1
            if node.is_end:
                dp[j] = (dp[j] + dp[i]) % MOD

    print(dp[n])

threading.Thread(target=main).start()