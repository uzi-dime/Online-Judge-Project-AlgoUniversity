# CSES Problem: Permutation Prime Sums
# Problem ID: 3423
# Generated on: 2025-07-22 20:38:01

import sys

def main():
    import sys
    input = sys.stdin.readline

    n = int(input())
    # For n = 1, the only possible sum is 1+1=2, which is prime
    if n == 1:
        print(1)
        print(1)
        return

    # For n = 2, possible permutations:
    # (1,2) + (2,1) = [3,3] (both prime)
    # (1,2) + (1,2) = [2,4] (4 is not prime)
    # So (1,2) and (2,1) is valid
    if n == 2:
        print(1, 2)
        print(2, 1)
        return

    # For n >= 3, try to construct two permutations such that ai+bi is always prime.
    # Observation: If we take a = [1,2,...,n], b = [n,n-1,...,1], then ai+bi = n+1 for all i.
    # n+1 is prime only for n = 2 (n+1=3), n = 4 (n+1=5), n = 6 (n+1=7), etc.
    # But for large n, n+1 is not always prime.

    # Let's try to check if there is a general solution.
    # For n = 4, a = [1,2,3,4], b = [2,1,4,3]
    # ai+bi = [3,3,7,7] (all primes)
    # For n = 5, a = [1,2,3,4,5], b = [1,2,3,4,5]
    # ai+bi = [2,4,6,8,10] (not all primes)
    # For n = 5, a = [1,2,3,4,5], b = [2,3,4,5,1]
    # ai+bi = [3,5,7,9,6] (9,6 not prime)
    # For n = 5, a = [1,2,3,4,5], b = [5,4,3,2,1]
    # ai+bi = [6,6,6,6,6] (not prime)

    # Let's try to construct for n = 4:
    # a = [1,2,3,4], b = [2,1,4,3]
    # ai+bi = [3,3,7,7] (all primes)
    # For n = 6, a = [1,2,3,4,5,6], b = [5,6,1,2,3,4]
    # ai+bi = [6,8,4,6,8,10] (not all primes)

    # Let's try to construct for n = 3:
    # a = [1,2,3], b = [2,3,1]
    # ai+bi = [3,5,4] (4 not prime)
    # Try a = [1,2,3], b = [3,1,2]
    # ai+bi = [4,3,5] (4 not prime)

    # Try to check for small n
    # For n = 1: possible
    # For n = 2: possible
    # For n = 3: impossible
    # For n = 4: possible
    # For n = 5: impossible

    # Let's check for n up to 10
    # It seems that a solution exists only for n = 1,2,4

    # Let's check for n = 6:
    # Try a = [1,2,3,4,5,6], b = [6,5,4,3,2,1]
    # ai+bi = [7,7,7,7,7,7] (all primes)
    # 7 is prime, so possible

    # For n = 8:
    # a = [1,2,3,4,5,6,7,8], b = [8,7,6,5,4,3,2,1]
    # ai+bi = [9,9,9,9,9,9,9,9] (9 not prime)

    # For n = 10:
    # a = [1,2,3,4,5,6,7,8,9,10], b = [10,9,8,7,6,5,4,3,2,1]
    # ai+bi = [11,11,11,11,11,11,11,11,11,11] (11 is prime)

    # So for even n, if n+1 is prime, then a = [1..n], b = [n..1] is a solution

    def is_prime(x):
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        i = 3
        while i * i <= x:
            if x % i == 0:
                return False
            i += 2
        return True

    if is_prime(n + 1):
        a = list(range(1, n + 1))
        b = list(range(n, 0, -1))
        print(' '.join(map(str, a)))
        print(' '.join(map(str, b)))
        return

    # For n = 4, a = [1,2,3,4], b = [2,1,4,3] is a solution
    if n == 4:
        print('1 2 3 4')
        print('2 1 4 3')
        return

    # For n = 2, already handled above
    # For n = 1, already handled above

    print("IMPOSSIBLE")

if __name__ == "__main__":
    main()