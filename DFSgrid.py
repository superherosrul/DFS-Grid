import pygame # I used this to visualize the grid
from random import choice
import datetime

timestarts = datetime.datetime.now()

resolution = w, h = 909, 909 #size of the screen
cellsize = 18 #the size of each cell

cols, rows = w // cellsize, h // cellsize #calculates the amount of columns and rows

pygame.init() #initialize pygame
screen = pygame.display.set_mode(resolution) #sets the screen to the resolution I set
time = pygame.time.Clock() #tracks speed


class defineCell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.sides = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw_current_cell(self):
        x, y = self.x * cellsize, self.y * cellsize
        pygame.draw.rect(screen, pygame.Color('saddlebrown'), (x + 1, y + 1, cellsize - 1, cellsize - 1))

    def draw(self):
        x, y = self.x * cellsize, self.y * cellsize
        if self.visited:
            pygame.draw.rect(screen, pygame.Color('black'), (x, y, cellsize, cellsize))
        
        if self.sides['top']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y), (x + cellsize, y), 9)
        if self.sides['right']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + cellsize, y), (x + cellsize, y + cellsize), 9)
        if self.sides['bottom']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + cellsize, y + cellsize), (x, y + cellsize), 9)
        if self.sides['left']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y + cellsize), (x, y), 9)

    def cell_check(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return gridcell[find_index(x, y)]
        
    def check_neighbors(self):
        neighbors = []
        top = self.cell_check(self.x, self.y - 1)
        right = self.cell_check(self.x + 1, self.y)
        bottom = self.cell_check(self.x, self.y + 1)
        left = self.cell_check(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
def remove_sides(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.sides['left'] = False
        next.sides['right'] = False
    elif dx == -1:
        current.sides['right'] = False
        next.sides['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.sides['top'] = False
        next.sides['bottom'] = False
    elif dy == -1:
        current.sides['bottom'] = False
        next.sides['top'] = False
    
#Creates grid cells
gridcell = [defineCell(col, row) for row in range(rows) for col in range(cols)]
currentcell = gridcell[0]
stack = []
colors, color = [], 40

#starts maze generation
while True:
    screen.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    #Draw all cells
    [cell.draw() for cell in gridcell]
    currentcell.visited = True
    currentcell.draw_current_cell()
    [pygame.draw.rect(screen, colors[i], (cell.x * cellsize + 6, cell.y * cellsize + 6,
                                          cellsize - 12, cellsize - 12), border_radius= 14) for i, cell in enumerate(stack)]

    next_cell = currentcell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(currentcell)
        colors.append((min(color, 255), 10, 100))
        color += 1
        remove_sides(currentcell, next_cell)
        currentcell = next_cell
    elif stack:
        currentcell = stack.pop()

    
    pygame.display.flip()
    time.tick(60)

    if len(stack) == 0:
        break

time_elapsed = datetime.datetime.now() - timestarts
print(f"Time to generate the maze using dfs: {time_elapsed}")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    pygame.display.flip()
