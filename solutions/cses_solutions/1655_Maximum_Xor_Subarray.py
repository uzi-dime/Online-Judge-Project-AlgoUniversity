# CSES Problem: Maximum Xor Subarray
# Problem ID: 1655
# Generated on: 2025-07-22 20:30:31

import sys

input = sys.stdin.readline

# Trie node for storing prefix XORs in binary
class TrieNode:
    def __init__(self):
        self.child = [None, None]

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    # Insert a number into the trie
    def insert(self, num):
        node = self.root
        for i in reversed(range(32)):  # 32 bits for up to 10^9
            bit = (num >> i) & 1
            if not node.child[bit]:
                node.child[bit] = TrieNode()
            node = node.child[bit]
    
    # Find max XOR of num with any prefix in the trie
    def query(self, num):
        node = self.root
        res = 0
        for i in reversed(range(32)):
            bit = (num >> i) & 1
            toggled = 1 - bit
            if node.child[toggled]:
                res |= (1 << i)
                node = node.child[toggled]
            else:
                node = node.child[bit]
        return res

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    
    trie = Trie()
    prefix_xor = 0
    max_xor = 0
    
    trie.insert(0)  # Insert prefix_xor=0 for subarrays starting at index 0
    
    for x in arr:
        prefix_xor ^= x
        max_xor = max(max_xor, trie.query(prefix_xor))
        trie.insert(prefix_xor)
    
    print(max_xor)

if __name__ == "__main__":
    main()