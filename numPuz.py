import pygame
import sys
import random
import math


class Tile:
	def __init__(self, val, x, y):
		self.value = val
		self.surface = pygame.Surface((200, 200))
		self.position = (x, y)
		self.clickbox = pygame.Rect((x * 200, y * 200), (200, 200))
	
	def draw(self):
		# Don't fill in color or text for the blank tile
		if self.value == ' ':
			self.surface.fill((255, 255, 255))
			return
		
		tile_color = (255, 0, 0)
		self.surface.fill(tile_color)
		textImage = textGenerator.render(str(self.value), True, (255, 255, 255))
		self.surface.blit(textImage, (85, 65))
		
	def click_collides(self, click):
		if self.value == ' ':
			return False
	
		return self.clickbox.collidepoint(click[0], click[1])
	
	def reposition(self):
		self.clickbox = pygame.Rect((self.position[0] * 200, self.position[1] * 200), (200, 200))
	
	def move(self, direction):
		if direction == 'UP':
			self.position = (self.position[0], self.position[1] - 1)
			self.reposition()
		elif direction == 'DOWN':
			self.position = (self.position[0], self.position[1] + 1)
			self.reposition()
		elif direction == 'LEFT':
			self.position = (self.position[0] - 1, self.position[1])
			self.reposition()
		elif direction == 'RIGHT':
			self.position = (self.position[0] + 1, self.position[1])
			self.reposition()


class Game:
	def __init__(self):
		# Generate a 3 x 3 array of tiles
		self.tiles = generate_tiles()
		
		for i in self.tiles:
			print(i)
		
		# While loop that makes sure the puzzle is never generated pre-solved.
		while self.count_inversions() % 2 == 1:
			self.tiles = generate_tiles()
	
	def get_tile_values(self):
		return [[self.tiles[x][y].value for x in range(3)] for y in range(3)]
	
	def is_solved(self):
		return True if self.get_tile_values() == [[1, 2, 3], [4, 5, 6], [7, 8, ' ']] else False
	
	def draw_tiles(self, surface):
		for x in range(3):
			for y in range(3):
				tile = self.tiles[x][y]
				tile.draw()
				surface.blit(tile.surface, (tile.position[0] * 200, tile.position[1] * 200))
				
	def handle_mouse_click(self, click):
		if 0 > click[0] > 600 or 0 > click[1] > 600:
			print("Please don't click outside of the board!")
			return
		
		for x in range(3):
			for y in range(3):
				tile = self.tiles[x][y]
				if tile.click_collides(click):
					self.move_tile(x, y)
	
	def move_blank_tile(self, direction):
		for x in range(3):
			for y in range(3):
				if self.tiles[x][y].value == ' ':
					self.tiles[x][y].move(direction)
					return
	
	# noinspection PyUnresolvedReferences
	def move_tile(self, tileX, tileY):
		clickedTile = self.tiles[tileX][tileY]

		if tileY > 0:
			if self.tiles[tileX][tileY - 1].value == ' ':
				clickedTile.move('UP')
				self.move_blank_tile('DOWN')
				self.tiles[tileX][tileY], self.tiles[tileX][tileY - 1] = \
					self.tiles[tileX][tileY - 1], self.tiles[tileX][tileY]

		if tileY < 2:
			if self.tiles[tileX][tileY + 1].value == ' ':
				clickedTile.move('DOWN')
				self.move_blank_tile('UP')
				self.tiles[tileX][tileY], self.tiles[tileX][tileY + 1] = \
					self.tiles[tileX][tileY + 1], self.tiles[tileX][tileY]

		if tileX > 0:
			if self.tiles[tileX - 1][tileY].value == ' ':
				clickedTile.move('LEFT')
				self.move_blank_tile('RIGHT')
				self.tiles[tileX - 1][tileY], self.tiles[tileX][tileY] = \
					self.tiles[tileX][tileY], self.tiles[tileX - 1][tileY]

		if tileX < 2:
			if self.tiles[tileX + 1][tileY].value == ' ':
				clickedTile.move('RIGHT')
				self.move_blank_tile('LEFT')
				self.tiles[tileX + 1][tileY], self.tiles[tileX][tileY] = \
					self.tiles[tileX][tileY], self.tiles[tileX + 1][tileY]
	
		
	def count_inversions(self):
		inversions = 0
		
		for x in range(9):
			selectedVal = self.tiles[math.floor(x / 3)][x % 3].value
			if selectedVal == ' ':
				continue
			
			for y in range(x, 9):
				comparedVal = self.tiles[math.floor(y / 3)][y % 3].value
				if comparedVal == ' ':
					continue
				inversions += 1 if selectedVal > comparedVal else 0
		
		return inversions + 1

def generate_tiles():
	possibleTiles = [1, 2, 3, 4, 5, 6, 7, 8, ' ']
	res = [[], [], []]
	
	for x in range(3):
		for y in range(3):
			res[x].append(Tile(random.choice(possibleTiles), x, y))
			possibleTiles.remove(res[x][y].value)
	
	return res


def draw_grid(surface):
	black = (0, 0, 0)
	# Draw outline along window lines
	boardOutlinePoints = ((0, 0), (width, 0), (width, height), (0, height))
	pygame.draw.lines(surface, black, closed = True, points = boardOutlinePoints, width = 2)
	# Draw horizontal grid lines
	for i in range(1, 3):
		pygame.draw.line(surface, black, start_pos = (0, i * 200), end_pos = (width, i * 200))
	# Draw vertical grid lines
	for i in range(1, 3):
		pygame.draw.line(surface, black, start_pos = (i * 200, 0), end_pos = (i * 200, height))


pygame.init()

fps = 60
width, height = 600, 600

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
puzzle = Game()

pygame.display.set_caption('Sliding Number Puzzle')
textGenerator = pygame.font.SysFont('arial', 48)
pygame.mouse.set_visible(True)

while True:
	screen.fill((255, 255, 255))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			pos = pygame.mouse.get_pos()
			puzzle.handle_mouse_click(pos)
	
	puzzle.draw_tiles(screen)
	draw_grid(screen)
	
	pygame.display.flip()
	fpsClock.tick(fps)

	if puzzle.is_solved():
		print('Congratulations!')
		sys.exit()
