import pygame
import os
import sys

ROW = COL = 30
WIDTH = HEIGHT = 900
SIZE = WIDTH // ROW
GRID = []

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pathfinder')

EDGE = pygame.image.load(os.path.join('assets', 'box.png'))
GRASS = pygame.image.load(os.path.join('assets', 'grass.png'))
ROCK = pygame.image.load(os.path.join('assets', 'rock.png'))
START = pygame.image.load(os.path.join('assets', 'rabbit.png'))
END = pygame.image.load(os.path.join('assets', 'home.png'))
GRAY = pygame.image.load(os.path.join('assets', 'gray.png'))
PINK = pygame.image.load(os.path.join('assets', 'pink.png'))
PATH = pygame.image.load(os.path.join('assets', 'carrot.png'))

class Square:
	def __init__(self, col, row):
		self.x = col
		self.y = row
		self.start = False
		self.end = False
		self.wall = False
		self.edge = False
		self.queued = False
		self.visited = False
		self.neighbours = []
		self.prior = None

	def draw(self, window, node):
		gridSquare = pygame.transform.scale(node, (SIZE, SIZE))
		window.blit(gridSquare, (self.x * SIZE, self.y * SIZE))

	def setNeighbours(self):
		if self.x > 0:
			self.neighbours.append(GRID[self.x-1][self.y])
		if self.x < COL - 1:
			self.neighbours.append(GRID[self.x+1][self.y])
		if self.y > 0:
			self.neighbours.append(GRID[self.x][self.y-1])
		if self.y < ROW - 1:
			self.neighbours.append(GRID[self.x][self.y+1])

def gridInit(cols, rows, grid):
	for col in range(cols):
		colArr = []
		for row in range(rows):
			colArr.append(Square(col, row))
		grid.append(colArr)

def gridDraw(window, cols, rows, grid):
	for col in range(cols):
		for row in range(rows):
			square = grid[col][row]
			if (col == 0 or col == (cols-1) or row == 0 or row == (rows-1)):
				square.edge = True
				square.draw(window, EDGE)
			else:
				square.draw(window, GRASS)

def initNeighbours(col, row, grid):
	for i in range(COL):
		for j in range(ROW):
			GRID[i][j].setNeighbours()

def main():

	gridInit(COL, ROW, GRID)
	gridDraw(WIN, COL, ROW, GRID)
	initNeighbours(COL, ROW, GRID)

	startPos = False
	endPos = False
	wallPos = False
	beginAlgo = False
	searching = True
	startBox = None
	targetBox = None
	queue = []
	path = []

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEMOTION:
				xPos = pygame.mouse.get_pos()[0]
				yPos = pygame.mouse.get_pos()[1]

				if event.buttons[0]:
					i = xPos // SIZE
					j = yPos // SIZE
					if GRID[i][j].edge or GRID[i][j].start or GRID[i][j].end:
						pass
					else:
						wallBox = GRID[i][j]
						wallBox.wall = True
						wallPos = True
						wallBox.draw(WIN, ROCK)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				xPos = pygame.mouse.get_pos()[0]
				yPos = pygame.mouse.get_pos()[1]
				if event.button == 3 and not startPos:
					i = xPos // SIZE
					j = yPos // SIZE
					if GRID[i][j].edge or GRID[i][j].start or GRID[i][j].wall:
						pass
					else:
						startBox = GRID[i][j]
						startBox.start = True  
						startBox.visited = True 
						queue.append(startBox)  
						startPos = True
						startBox.draw(WIN, START)

				elif event.button == 3 and startPos and not endPos:
					i = xPos // SIZE
					j = yPos // SIZE
					if GRID[i][j].edge or GRID[i][j].start or GRID[i][j].wall:
						pass
					else:
						targetBox = GRID[i][j]
						targetBox.end = True
						endPos = True
						targetBox.draw(WIN, END)

			if event.type == pygame.KEYDOWN and startPos and endPos:
				if event.key == pygame.K_RETURN:
					beginAlgo = True
					
		if beginAlgo:
			if len(queue) > 0 and searching:
				currentBox = queue.pop(0)
				currentBox.visited = True
				if currentBox == targetBox:
					searching = False
					while currentBox.prior != startBox:
						path.append(currentBox.prior)
						currentBox = currentBox.prior
				else:
					for neighbour in currentBox.neighbours:
						if not neighbour.queued and not neighbour.wall and not neighbour.edge and not neighbour.start:
							neighbour.queued = True
							neighbour.prior = currentBox
							queue.append(neighbour)
			else:
				if searching:
					Tk().wm_withdraw()
					messagebox.showinfo('No path available.')
					searching = False

		for col in range(COL):
			for row in range(ROW):
				square = GRID[col][row]
				if square.queued and not square.end:
					square.draw(WIN, PINK)
				if square.visited and not square.start and not square.end:
					square.draw(WIN, GRAY)
				if square in path:
					square.draw(WIN, PATH)
		
		pygame.display.update()

main()
