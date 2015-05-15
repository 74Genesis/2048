import pygame
from const import *

class Cell(pygame.sprite.Sprite): #Создание спрайта
	def __init__(self, x, y, num):
		super().__init__()
		color = "#EEE4DA"
		#цвет
		if num == 2:
			color = "#eee4da"
		if num == 4:
			color = "#ede0c8"
		if num == 8:
			color = "#f2b179"
		if num == 16:
			color = "#f59563"
		if num == 32:
			color = "#f67c5f"
		if num == 64:
			color = "#f65e3b"
		if num == 128:
			color = "#edcf72"
		if num == 256:
			color = "#edcc61"
		if num == 512:
			color = "#edc850"
		if num == 1024:
			color = "#edc53f"
		if num == 2048:
			color = "#edc22e"
		if num > 2048:
			color = "#CC0033"

		#Рисунок объекта
		self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
		self.image.fill(pygame.Color(color))
		#Настоящий размер объекта
		self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)