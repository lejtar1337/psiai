import random

def fitness(board):
    clashes = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                clashes += 1
    return clashes

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

def mutate(board):
    n = len(board)
    board[random.randint(0, n - 1)] = random.randint(0, n - 1)
    return board

def genetic_algorithm(n, pop_size=100, max_iter=10000, p_cross=0.8, p_mut=0.2):
    population = [[random.randint(0, n - 1) for _ in range(n)] for _ in range(pop_size)]
    
    for i in range(max_iter):
        population.sort(key=fitness)
        min_err = fitness(population[0])
        print(f"Iteracja: {i+1}. Minimalny błąd: {min_err}")
        
        if min_err == 0:
            print(f"Iteracja: {i+1} - odnaleziono ustawienie!")
            return population[0]
            
        new_gen = []
        
        for _ in range(int(pop_size * p_cross) // 2):
            p1, p2 = random.sample(population[:pop_size//2], 2)
            c1, c2 = crossover(p1, p2)
            new_gen.extend([c1, c2])
            
        for _ in range(int(pop_size * p_mut)):
            ind = random.choice(population)
            new_gen.append(mutate(list(ind)))
            
        population.extend(new_gen)
        population.sort(key=fitness)
        population = population[:pop_size]
        
    return population[0]

def print_board(board):
    n = len(board)
    headers = "   " + "".join(chr(ord('A') + i) for i in range(n))
    print(headers)
    for i in range(n):
        row_num = str(i + 1).rjust(2)
        row_str = "".join("X" if board[i] == j else "." for j in range(n))
        print(f"{row_num} {row_str}")

N = 8
print(f"N = {N}")
solution = genetic_algorithm(N)
print(f"Lista: {', '.join(map(str, solution))}")
print()
print_board(solution)
