# CSES Problem: Line Segment Intersection
# Problem ID: 2190
# Generated on: 2025-07-22 20:28:13

import sys

# Fast input
input = sys.stdin.readline

def orientation(ax, ay, bx, by, cx, cy):
    # Returns:
    # 0 if colinear
    # 1 if clockwise
    # 2 if counterclockwise
    val = (by - ay) * (cx - bx) - (bx - ax) * (cy - by)
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def on_segment(ax, ay, bx, by, cx, cy):
    # Returns True if point (cx,cy) lies on segment (ax,ay)-(bx,by)
    return min(ax, bx) <= cx <= max(ax, bx) and min(ay, by) <= cy <= max(ay, by)

def segments_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    o1 = orientation(x1, y1, x2, y2, x3, y3)
    o2 = orientation(x1, y1, x2, y2, x4, y4)
    o3 = orientation(x3, y3, x4, y4, x1, y1)
    o4 = orientation(x3, y3, x4, y4, x2, y2)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special Cases
    # x3, y3 is colinear with segment 1 and lies on segment 1
    if o1 == 0 and on_segment(x1, y1, x2, y2, x3, y3):
        return True
    # x4, y4 is colinear with segment 1 and lies on segment 1
    if o2 == 0 and on_segment(x1, y1, x2, y2, x4, y4):
        return True
    # x1, y1 is colinear with segment 2 and lies on segment 2
    if o3 == 0 and on_segment(x3, y3, x4, y4, x1, y1):
        return True
    # x2, y2 is colinear with segment 2 and lies on segment 2
    if o4 == 0 and on_segment(x3, y3, x4, y4, x2, y2):
        return True

    return False

t = int(input())
results = []
for _ in range(t):
    x1, y1, x2, y2, x3, y3, x4, y4 = map(int, input().split())
    if segments_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
        results.append("YES")
    else:
        results.append("NO")

print('\n'.join(results))