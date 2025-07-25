# CSES Problem: Bouncing Ball Steps
# Problem ID: 3215
# Generated on: 2025-07-22 20:36:26

import sys

input = sys.stdin.readline

def solve_case(n, m, k):
    # The ball starts at (1,1), moving (+1,+1)
    # The ball bounces off borders, so its movement is periodic.
    # The period is 2*(n-1) for rows, 2*(m-1) for columns.

    # If n==2, period is 2, etc.
    # For position after k steps:
    # Row: 1 + d_row * k, but reflected at borders.
    # The position along a line of length L after k steps, bouncing at ends:
    # pos = 1 + s, where s = k % (2*(L-1))
    # If s < L-1: pos = 1 + s
    # else: pos = L - (s - (L-1))

    def get_pos(L, k):
        if L == 1:
            return 1
        period = 2 * (L - 1)
        s = k % period
        if s < L - 1:
            return 1 + s
        else:
            return L - (s - (L - 1))

    def get_bounces(L, k):
        if L == 1:
            return 0
        period = 2 * (L - 1)
        # Each period: 2 bounces (one at each end)
        full_periods = k // period
        bounces = full_periods * 2
        rem = k % period
        # In the remaining steps, count how many borders are hit
        # At s = L-1: first bounce (at far end)
        # At s = period: second bounce (back at start)
        if rem >= L - 1:
            bounces += 1
        # If rem == period-1, we hit the start again, but that's already counted in full_periods
        return bounces

    row = get_pos(n, k)
    col = get_pos(m, k)
    bounces_row = get_bounces(n, k)
    bounces_col = get_bounces(m, k)
    # The ball changes direction whenever it hits a border (row or column)
    # But if it hits a corner (both borders at once), it only counts as one change
    # So, need to count the number of times both row and column hit border at the same step

    # The times when the ball hits a border:
    # For rows: at steps where s_row == 0 (start) or s_row == n-1 (end)
    # For columns: at steps where s_col == 0 or s_col == m-1

    # The ball starts at (1,1), so first border hit is at step min(n-1, m-1)
    # The steps when both row and column hit border at the same time:
    # These are the steps where both s_row in {0, n-1} and s_col in {0, m-1}
    # The period for both is lcm(2*(n-1), 2*(m-1))
    from math import gcd

    def lcm(a, b):
        return a * b // gcd(a, b)

    if n == 1 or m == 1:
        # Only one row or column, so only one direction to bounce
        total_bounces = bounces_row + bounces_col
    else:
        period_row = 2 * (n - 1)
        period_col = 2 * (m - 1)
        l = lcm(period_row, period_col)
        # In each lcm period, how many times do both hit border at same time?
        # At step t in [0, l), if t % (n-1) == 0 and t % (m-1) == 0 and t != 0 and t <= k
        # But only at t != 0 and t <= k
        # Actually, at t in [0, l), t % (n-1) == 0 and t % (m-1) == 0 and t % period_row in {0, n-1} and t % period_col in {0, m-1}
        # But for both to be at border, t % (n-1) == 0 and t % (m-1) == 0, and t % period_row in {0, n-1}, t % period_col in {0, m-1}
        # But for simplicity, let's just count the steps t in [1, k] where both row and col are at border

        # The ball hits a corner at steps t where t % (n-1) == 0 and t % (m-1) == 0 and t != 0 and t <= k
        # But only at t where the direction is reversed, i.e., at t % period_row in {0, n-1} and t % period_col in {0, m-1}
        # But in practice, at t = 0, n-1, 2*(n-1), ... and t = 0, m-1, 2*(m-1), ... so at t = lcm(n-1, m-1), 2*lcm(n-1, m-1), ...

        # Let's find the number of t in [1, k] where t % lcm(n-1, m-1) == 0 and t <= k
        if n == 2 and m == 2:
            # Special case: always at corners
            corners = k // 1
        else:
            l_corner = lcm(n - 1, m - 1)
            corners = k // l_corner
        total_bounces = bounces_row + bounces_col - corners

    return f"{row} {col} {total_bounces}"

t = int(sys.stdin.readline())
for _ in range(t):
    n, m, k = map(int, sys.stdin.readline().split())
    print(solve_case(n, m, k))