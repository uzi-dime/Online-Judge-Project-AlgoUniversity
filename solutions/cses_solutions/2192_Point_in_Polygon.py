# CSES Problem: Point in Polygon
# Problem ID: 2192
# Generated on: 2025-07-22 20:28:38

import sys

input = sys.stdin.readline

def point_on_segment(px, py, x1, y1, x2, y2):
    # Check if point (px, py) is on segment (x1, y1)-(x2, y2)
    # First, check collinearity using cross product
    dx1, dy1 = x2 - x1, y2 - y1
    dx2, dy2 = px - x1, py - y1
    cross = dx1 * dy2 - dy1 * dx2
    if cross != 0:
        return False
    # Then, check if within bounding box
    if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2):
        return True
    return False

def point_in_polygon(px, py, polygon):
    n = len(polygon)
    cnt = 0
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        # Check if point is on edge
        if point_on_segment(px, py, x1, y1, x2, y2):
            return "BOUNDARY"
        # Ray casting: count crossings of horizontal ray to the right
        # Check if edge crosses the horizontal line at py
        # We want y1 <= py < y2 or y2 <= py < y1
        if (y1 <= py < y2) or (y2 <= py < y1):
            # Compute intersection x coordinate
            x_int = x1 + (px - x1) * (y2 - y1) / (y2 - y1) if y2 != y1 else x1
            # Actually, we want to compute intersection of edge with y=py
            # x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            x_cross = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x_cross > px:
                cnt += 1
    return "INSIDE" if cnt % 2 == 1 else "OUTSIDE"

n, m = map(int, input().split())
polygon = [tuple(map(int, input().split())) for _ in range(n)]
points = [tuple(map(int, input().split())) for _ in range(m)]

for px, py in points:
    print(point_in_polygon(px, py, polygon))