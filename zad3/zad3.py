import tkinter as tk
from tkinter import filedialog, messagebox
import math
import heapq

class PathFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Szukanie drogi w grafie")
        
        self.coords = {}
        self.adj = {}
        self.n = 0
        self.scale = 40
        self.offset = 20
        
        self.start_node = None
        self.goal_node = None
        
        self.generator = None
        self.came_from = {}
        self.cost_so_far = {}
        
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Button(frame, text="Wczytaj graf", command=self.load_graph).pack(side=tk.LEFT)
        
        self.algo_var = tk.StringVar(value="a_star")
        tk.Radiobutton(frame, text="Dijkstra", variable=self.algo_var, value="dijkstra").pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="Best First", variable=self.algo_var, value="best_first").pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="A*", variable=self.algo_var, value="a_star").pack(side=tk.LEFT)
        
        tk.Button(frame, text="Krok", command=self.step).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Rozwiąż", command=self.solve_all).pack(side=tk.LEFT)
        tk.Button(frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)
        
        self.info_lbl = tk.Label(frame, text="Koszt: 0.00 | Start: ? | Cel: ?")
        self.info_lbl.pack(side=tk.LEFT, padx=10)
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.set_start)
        self.canvas.bind("<Button-3>", self.set_goal)

    def load_graph(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not filepath: return
        
        with open(filepath, 'r') as f:
            lines = [l.strip().split() for l in f if l.strip()]
            
        self.n = int(lines[0][0])
        self.coords.clear()
        self.adj.clear()
        
        for i in range(1, self.n + 1):
            self.coords[i] = (int(lines[i][0]), int(lines[i][1]))
            
        for i in range(1, self.n + 1):
            parts = list(map(int, lines[self.n + i]))
            self.adj[i] = parts[1:]
            
        self.reset()

    def draw_graph(self, current=None):
        self.canvas.delete("all")
        if not self.coords: return
        
        # Rysowanie krawędzi
        for u in self.adj:
            x1, y1 = self.coords[u]
            for v in self.adj[u]:
                x2, y2 = self.coords[v]
                self.canvas.create_line(x1*self.scale+self.offset, y1*self.scale+self.offset,
                                        x2*self.scale+self.offset, y2*self.scale+self.offset, fill="lightgray")
        
        # Rysowanie odwiedzonych
        for node in self.came_from:
            parent = self.came_from[node]
            if parent:
                x1, y1 = self.coords[node]
                x2, y2 = self.coords[parent]
                self.canvas.create_line(x1*self.scale+self.offset, y1*self.scale+self.offset,
                                        x2*self.scale+self.offset, y2*self.scale+self.offset, fill="blue", width=2)
                                        
        # Rysowanie ścieżki
        if self.goal_node in self.came_from and current == self.goal_node:
            curr = self.goal_node
            while curr != self.start_node:
                p = self.came_from[curr]
                x1, y1 = self.coords[curr]
                x2, y2 = self.coords[p]
                self.canvas.create_line(x1*self.scale+self.offset, y1*self.scale+self.offset,
                                        x2*self.scale+self.offset, y2*self.scale+self.offset, fill="red", width=3)
                curr = p
                
        # Rysowanie węzłów
        r = 5
        for u, (x, y) in self.coords.items():
            cx, cy = x*self.scale+self.offset, y*self.scale+self.offset
            color = "white"
            if u == self.start_node: color = "green"
            elif u == self.goal_node: color = "red"
            elif u == current: color = "yellow"
            elif u in self.came_from: color = "lightblue"
            
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color, outline="black")
            
        start_txt = self.start_node if self.start_node else "?"
        goal_txt = self.goal_node if self.goal_node else "?"
        cost = self.cost_so_far.get(self.goal_node, 0.0) if current == self.goal_node else 0.0
        self.info_lbl.config(text=f"Koszt: {cost:.2f} | Start: {start_txt} | Cel: {goal_txt}")

    def get_closest_node(self, event):
        if not self.coords: return None
        click_x, click_y = event.x, event.y
        best_node, min_dist = None, float('inf')
        for u, (x, y) in self.coords.items():
            cx, cy = x*self.scale+self.offset, y*self.scale+self.offset
            dist = math.hypot(cx - click_x, cy - click_y)
            if dist < min_dist and dist < 20:
                min_dist, best_node = dist, u
        return best_node

    def set_start(self, event):
        node = self.get_closest_node(event)
        if node:
            self.start_node = node
            self.reset_search()

    def set_goal(self, event):
        node = self.get_closest_node(event)
        if node:
            self.goal_node = node
            self.reset_search()

    def reset(self):
        self.start_node = None
        self.goal_node = None
        self.reset_search()

    def reset_search(self):
        self.generator = None
        self.came_from.clear()
        self.cost_so_far.clear()
        self.draw_graph()

    def dist(self, u, v):
        return math.hypot(self.coords[u][0] - self.coords[v][0], self.coords[u][1] - self.coords[v][1])

    def search_algorithm(self):
        frontier = []
        heapq.heappush(frontier, (0, self.start_node))
        self.came_from = {self.start_node: None}
        self.cost_so_far = {self.start_node: 0}
        algo = self.algo_var.get()

        while frontier:
            _, current = heapq.heappop(frontier)
            yield current

            if current == self.goal_node:
                break

            for next_node in self.adj[current]:
                new_cost = self.cost_so_far[current] + self.dist(current, next_node)
                if next_node not in self.cost_so_far or new_cost < self.cost_so_far[next_node]:
                    self.cost_so_far[next_node] = new_cost
                    self.came_from[next_node] = current
                    
                    g = new_cost
                    h = self.dist(next_node, self.goal_node)
                    
                    if algo == 'dijkstra': f = g
                    elif algo == 'best_first': f = h
                    else: f = g + h
                        
                    heapq.heappush(frontier, (f, next_node))

    def step(self):
        if not self.start_node or not self.goal_node:
            messagebox.showwarning("Błąd", "Wybierz węzeł startowy (LPM) i końcowy (PPM).")
            return
            
        if self.generator is None:
            self.came_from.clear()
            self.cost_so_far.clear()
            self.generator = self.search_algorithm()
            
        try:
            current = next(self.generator)
            self.draw_graph(current)
        except StopIteration:
            pass

    def solve_all(self):
        if not self.start_node or not self.goal_node: return
        if self.generator is None:
            self.generator = self.search_algorithm()
            
        for current in self.generator:
            pass
        self.draw_graph(self.goal_node)

if __name__ == "__main__":
    root = tk.Tk()
    app = PathFinderApp(root)
    root.mainloop()