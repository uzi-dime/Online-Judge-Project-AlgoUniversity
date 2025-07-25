# CSES Problem: Chess Tournament
# Problem ID: 1697
# Generated on: 2025-07-22 20:38:11

import sys
import heapq

input = sys.stdin.readline

n = int(input())
x = list(map(int, input().split()))

# Each player is (games_wanted, player_index)
players = [(-games, idx + 1) for idx, games in enumerate(x) if games > 0]

# Check if total games wanted is even (each game involves 2 players)
total_games = sum(x)
if total_games % 2 != 0:
    print("IMPOSSIBLE")
    sys.exit(0)

# Use a max-heap (by negative games_wanted)
heapq.heapify(players)
res = []

while players:
    games1, p1 = heapq.heappop(players)
    games1 = -games1
    if games1 == 0:
        continue
    if not players:
        # Someone still wants games but no one left to pair with
        print("IMPOSSIBLE")
        sys.exit(0)
    games2, p2 = heapq.heappop(players)
    games2 = -games2
    # Schedule a game between p1 and p2
    res.append((p1, p2))
    games1 -= 1
    games2 -= 1
    if games1 > 0:
        heapq.heappush(players, (-games1, p1))
    if games2 > 0:
        heapq.heappush(players, (-games2, p2))

print(len(res))
for a, b in res:
    print(a, b)