# CSES Problem: Polygon Lattice Points
# Problem ID: 2193
# Generated on: 2025-07-22 20:28:54

import sys
import math

# Read input
input = sys.stdin.readline
n = int(input())
points = [tuple(map(int, input().split())) for _ in range(n)]

# Shoelace formula for twice the area
area2 = 0
boundary = 0

for i in range(n):
    x1, y1 = points[i]
    x2, y2 = points[(i + 1) % n]
    area2 += (x1 * y2 - x2 * y1)
    # Count lattice points on the edge using gcd
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    boundary += math.gcd(dx, dy)

area2 = abs(area2)

# Pick's theorem: A = I + B/2 - 1
# I = (A - B + 2) // 2
interior = (area2 - boundary + 2) // 2

print(f"{interior} {boundary}")