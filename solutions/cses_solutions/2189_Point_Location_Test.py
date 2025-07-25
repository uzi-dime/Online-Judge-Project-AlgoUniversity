# CSES Problem: Point Location Test
# Problem ID: 2189
# Generated on: 2025-07-22 20:28:01

import sys

# Read all input at once for efficiency
input = sys.stdin.read
data = input().split()

t = int(data[0])
res = []
idx = 1

for _ in range(t):
    x1 = int(data[idx])
    y1 = int(data[idx+1])
    x2 = int(data[idx+2])
    y2 = int(data[idx+3])
    x3 = int(data[idx+4])
    y3 = int(data[idx+5])
    idx += 6

    # Compute the cross product to determine the relative position
    cross = (x2 - x1)*(y3 - y1) - (y2 - y1)*(x3 - x1)
    if cross > 0:
        res.append("LEFT")
    elif cross < 0:
        res.append("RIGHT")
    else:
        res.append("TOUCH")

print('\n'.join(res))