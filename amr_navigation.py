import numpy as np

# ==================== STEP 1: OCCUPANCY GRID ====================
print("=" * 50)
print("PROJECT 3: Autonomous Mobile Robot Navigation")
print("=" * 50)

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

print("\nOccupancy Grid (0=Free, 1=Wall):")
for row in grid:
    print(" ".join(["⬜" if cell == 0 else "⬛" for cell in row]))

# ==================== STEP 2: A* PATHFINDING ====================
print("\n" + "=" * 50)
print("Running A* Pathfinding Algorithm...")
print("=" * 50)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, grid):
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in directions:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < 10 and 0 <= ny < 10 and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def astar(grid, start, goal):
    open_list = [(0, start, [start])]
    closed = set()
    
    while open_list:
        open_list.sort(key=lambda x: x[0])
        f, current, path = open_list.pop(0)
        
        if current == goal:
            return path
        
        if current in closed:
            continue
        closed.add(current)
        
        for neighbor in get_neighbors(current, grid):
            if neighbor not in closed:
                g = len(path)
                h = heuristic(neighbor, goal)
                new_path = path + [neighbor]
                open_list.append((g + h, neighbor, new_path))
    
    return None

start = (0, 0)
goal = (9, 9)

print(f"Start: {start}")
print(f"Goal: {goal}")

path = astar(grid, start, goal)

if path:
    print(f"\nPath Found! {len(path)} steps")
    print(f"Path: {path}")
else:
    print("No path found!")
    exit()

# ==================== STEP 3: VISUALIZE IN TERMINAL ====================
print("\n" + "=" * 50)
print("Path Visualization:")
print("=" * 50)

for i in range(10):
    row_str = ""
    for j in range(10):
        if (i, j) == start:
            row_str += "🟢"
        elif (i, j) == goal:
            row_str += "🔴"
        elif (i, j) in path:
            row_str += "🟠"
        elif grid[i][j] == 1:
            row_str += "⬛"
        else:
            row_str += "⬜"
    print(row_str)

# ==================== STEP 4: OBSTACLE AVOIDANCE ====================
print("\n" + "=" * 50)
print("Simulating Dynamic Obstacle...")
print("=" * 50)

obstacle = (5, 5)
print(f"Obstacle detected at: {obstacle}")

if obstacle in path:
    print("Obstacle is in path! Replanning...")
    grid[obstacle[0]][obstacle[1]] = 1
    new_path = astar(grid, start, goal)
    
    if new_path:
        print(f"New Path Found! {len(new_path)} steps")
        print(f"New Path: {new_path}")
        path = new_path
    else:
        print("Cannot reach goal!")

# ==================== STEP 5: FINAL MAP ====================
print("\n" + "=" * 50)
print("Final Path with Obstacle Avoidance:")
print("=" * 50)

for i in range(10):
    row_str = ""
    for j in range(10):
        if (i, j) == start:
            row_str += "🟢"
        elif (i, j) == goal:
            row_str += "🔴"
        elif (i, j) == obstacle:
            row_str += "🟡"
        elif (i, j) in path:
            row_str += "🟠"
        elif grid[i][j] == 1:
            row_str += "⬛"
        else:
            row_str += "⬜"
    print(row_str)

print("\n" + "=" * 50)
print("PROJECT 3 COMPLETE! Autonomous Mobile Robot Navigation Simulation Finished.")
print("=" * 50)