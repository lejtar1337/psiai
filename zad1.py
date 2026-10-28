import sys
import time
import os
from collections import deque

CHARS = {
    '\u253C': {'U', 'D', 'L', 'R'}, # ┼
    '\u2510': {'D', 'L'},           # ┐
    '\u2524': {'U', 'D', 'L'},      # ┤
    '\u2575': {'U'},                # ╵
    '\u2502': {'U', 'D'},           # │
    '\u2518': {'U', 'L'},           # ┘
    '\u2534': {'U', 'L', 'R'},      # ┴
    '\u2577': {'D'},                # ╷
    '\u2500': {'L', 'R'},           # ─
    '\u2514': {'U', 'R'},           # └
    '\u251C': {'U', 'D', 'R'},      # ├
    '\u2574': {'L'},                # ╴
    ' ': set(),                     # spacja
    '\u250C': {'D', 'R'},           # ┌
    '\u252C': {'D', 'L', 'R'},      # ┬p
    '\u2576': {'R'}                 # ╶
}

MOVES = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
INV_DIR = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}

def load_map(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip('\n') for line in f]
    max_len = max(len(line) for line in lines)
    return [list(line.ljust(max_len, ' ')) for line in lines]

def print_map(grid, start, end, visited, in_queue):
    out = "\033[H" # Powrót kursora na początek
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            pos = (x, y)
            if pos == start:
                out += f"\033[1;31m{char}\033[0m"
            elif pos == end:
                out += f"\033[1;34m{char}\033[0m"
            elif pos in visited:
                out += f"\033[1;32m{char}\033[0m"
            elif pos in in_queue:
                out += f"\033[1;33m{char}\033[0m"
            else:
                out += char
        out += "\n"
    sys.stdout.write(out)
    sys.stdout.flush()

def main():
    if len(sys.argv) < 2:
        print("Użycie: python script.py <sciezka_do_mapy>")
        return

    map_path = sys.argv[1]
    grid = load_map(map_path)

    for y, row in enumerate(grid):
        print("".join(row))

    print("\nPodaj dane (współrzędne to X i Y, gdzie X to kolumna, a Y to wiersz, liczone od 0):")
    sx = int(input("Start X: "))
    sy = int(input("Start Y: "))
    ex = int(input("Koniec X: "))
    ey = int(input("Koniec Y: "))
    algo = input("Algorytm (BFS/DFS): ").strip().upper()

    start = (sx, sy)
    end = (ex, ey)
    h, w = len(grid), len(grid[0])

    q = deque([(start, [start])])
    visited = set()
    in_queue = {start}
    steps = 0
    found = False

    os.system('cls' if os.name == 'nt' else 'clear')

    while q:
        #  BFS (kolejka FIFO, zdjęcie z początku)
        if algo == "BFS":       
            curr, path = q.popleft()
        else:
            curr, path = q.pop() 
        # DFS (stos LIFO, zdejmuje z końca)

        in_queue.discard(curr)
        visited.add(curr)
        steps += 1

        print_map(grid, start, end, visited, in_queue)
        time.sleep(0.1)

        if curr == end:
            found = True
            break

        cx, cy = curr
        char = grid[cy][cx]
        allowed = CHARS.get(char, set())

        for d in allowed:
            dy, dx = MOVES[d]
            nx, ny = cx + dx, cy + dy

            if 0 <= ny < h and 0 <= nx < w:
                nchar = grid[ny][nx]
                nallowed = CHARS.get(nchar, set())
                
                if INV_DIR[d] in nallowed:
                    npos = (nx, ny)
                    if npos not in visited and npos not in in_queue:
                        q.append((npos, path + [npos]))
                        in_queue.add(npos)

    print("\n--- PODSUMOWANIE ---")
    if found:
        print(f"Znaleziono ścieżkę! Długość ścieżki: {len(path)}")
    else:
        print("Brak ścieżki pomiędzy wybranymi polami.")
    print(f"Ilość wykonanych kroków algorytmu: {steps}")

if __name__ == "__main__":
    main()
    