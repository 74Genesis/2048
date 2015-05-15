import pygame
import struct #Для перевода из hex в rgb
from const import *


class Text(pygame.sprite.Sprite): #Создание спрайта
	def __init__(self, x, y, num):
		super().__init__()

		numLen = len(str(num))
		fontSize = 30

		#Изменение размера и положения текста в зависимости от размера числа
		if numLen >= 1:
			y += CELL_SIZE/2 - 22
			x += CELL_SIZE/2 - 9
		if numLen >= 2:
			x += CELL_SIZE/2 - 40
		if numLen >= 3:
			x += CELL_SIZE/2 - 40
		if numLen > 3:
			y += CELL_SIZE/2 - 25
			x += 1
			fontSize = 23		
		if numLen > 4:
			y += CELL_SIZE/2 - 27
			fontSize = 18
		if numLen > 5:
			y += CELL_SIZE/2 - 28
			fontSize = 16



		#цвет
		if num < 8:
			color = (119,110,101)
		elif num >= 8:
			color = (249,246,242)


		font = pygame.font.Font("font/ClearSans-Bold.ttf", fontSize)
		self.image = font.render(str(num), True, color)
		self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
