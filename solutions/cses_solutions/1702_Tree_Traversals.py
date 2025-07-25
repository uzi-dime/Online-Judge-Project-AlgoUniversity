# CSES Problem: Tree Traversals
# Problem ID: 1702
# Generated on: 2025-07-22 20:25:15

import sys
import threading

def main():
    sys.setrecursionlimit(1 << 25)
    n = int(sys.stdin.readline())
    preorder = list(map(int, sys.stdin.readline().split()))
    inorder = list(map(int, sys.stdin.readline().split()))

    # Map each value to its index in inorder traversal for O(1) lookups
    in_index = {val: idx for idx, val in enumerate(inorder)}

    # Use an explicit stack to avoid recursion depth issues
    result = []
    stack = []
    # Each stack item: (pre_l, pre_r, in_l, in_r)
    stack.append((0, n, 0, n))

    while stack:
        pre_l, pre_r, in_l, in_r = stack.pop()
        if pre_l >= pre_r or in_l >= in_r:
            continue
        root = preorder[pre_l]
        in_root_idx = in_index[root]
        left_size = in_root_idx - in_l

        # Postorder: left, right, root
        # Push root last, so process after subtrees
        result.append(root)
        # Push right subtree first, so it is processed after left
        stack.append((pre_l + left_size + 1, pre_r, in_root_idx + 1, in_r))
        stack.append((pre_l + 1, pre_l + left_size + 1, in_l, in_root_idx))

    # The result is in reverse postorder (root, right, left), so reverse it
    print(' '.join(map(str, reversed(result))))

threading.Thread(target=main).start()