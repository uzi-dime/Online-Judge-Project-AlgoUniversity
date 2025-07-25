# CSES Problem: Meet in the Middle
# Problem ID: 1628
# Generated on: 2025-07-22 20:35:01

# Meet-in-the-middle approach for subset sum
import sys
from collections import Counter

input = sys.stdin.readline

n, x = map(int, input().split())
arr = list(map(int, input().split()))

# Split array into two halves
mid = n // 2
left = arr[:mid]
right = arr[mid:]

# Generate all subset sums for a list
def subset_sums(nums):
    sums = []
    m = len(nums)
    for mask in range(1 << m):
        s = 0
        for i in range(m):
            if mask & (1 << i):
                s += nums[i]
        sums.append(s)
    return sums

left_sums = subset_sums(left)
right_sums = subset_sums(right)

# Count frequency of each sum in right_sums
right_count = Counter(right_sums)

# For each sum in left_sums, count how many right_sums make total x
ans = 0
for s in left_sums:
    ans += right_count[x - s]

print(ans)