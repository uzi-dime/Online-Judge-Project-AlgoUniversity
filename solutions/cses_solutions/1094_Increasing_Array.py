# CSES Problem: Increasing Array
# Problem ID: 1094
# Generated on: 2025-07-22 20:34:37

# Read input
import sys
input = sys.stdin.readline

n = int(input())
arr = list(map(int, input().split()))

moves = 0
for i in range(1, n):
    if arr[i] < arr[i - 1]:
        moves += arr[i - 1] - arr[i]
        arr[i] = arr[i - 1]  # Increase current element to previous

print(moves)