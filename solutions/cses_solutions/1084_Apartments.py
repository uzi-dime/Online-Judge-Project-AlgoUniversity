# CSES Problem: Apartments
# Problem ID: 1084
# Generated on: 2025-07-30 22:04:58

import sys

def solve():
    n, m, k = map(int, sys.stdin.readline().split())
    applicants = list(map(int, sys.stdin.readline().split()))
    apartments = list(map(int, sys.stdin.readline().split()))

    applicants.sort()
    apartments.sort()

    applicant_idx = 0
    apartment_idx = 0
    count = 0

    while applicant_idx < n and apartment_idx < m:
        desired_size = applicants[applicant_idx]
        apartment_size = apartments[apartment_idx]

        lower_bound = desired_size - k
        upper_bound = desired_size + k

        if lower_bound <= apartment_size <= upper_bound:
            # Applicant gets the apartment
            count += 1
            applicant_idx += 1
            apartment_idx += 1
        elif apartment_size < lower_bound:
            # Apartment is too small for the current applicant, try the next apartment
            apartment_idx += 1
        else: # apartment_size > upper_bound
            # Apartment is too large for the current applicant, try the next applicant
            applicant_idx += 1

    print(count)

if __name__ == "__main__":
    solve()