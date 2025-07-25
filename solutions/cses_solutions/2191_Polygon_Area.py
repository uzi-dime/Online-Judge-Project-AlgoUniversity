# CSES Problem: Polygon Area
# Problem ID: 2191
# Generated on: 2025-07-22 20:28:20

# Read input
n = int(input())
points = [tuple(map(int, input().split())) for _ in range(n)]

# Shoelace formula for 2 * area (guaranteed integer)
area2 = 0
for i in range(n):
    x1, y1 = points[i]
    x2, y2 = points[(i + 1) % n]
    area2 += x1 * y2 - x2 * y1

print(abs(area2))