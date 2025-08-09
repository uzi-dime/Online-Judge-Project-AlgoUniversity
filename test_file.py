

def solve_coin_piles():
    t = int(input())
    
    answer = []

    for _ in range(t):
        a, b = map(int, input().split())
        
        # Check if piles can be emptied
        # Conditions: (a + b) % 3 == 0 and 2*a >= b and 2*b >= a
        if (a + b) % 3 == 0 and 2 * a >= b and 2 * b >= a:
            answer.append("YES")
        else:
            answer.append("NO")
            
    print("\n".join(answer))
# Example usage
if __name__ == "__main__":
    solve_coin_piles()

