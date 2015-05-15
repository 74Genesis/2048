import pygame
import settings
import random
import cell
import text
# from cell import *
from const import * # константы

class Board():
	def __init__(self):
		self.sFile = settings.Settings()
		sDict = self.sFile.getSettings()
		#Настройки игры
		if sDict:
			if "Mode" in sDict:
				self.mode = sDict["Mode"]
			if "Score" in sDict:
				self.score = sDict["Score"]
			if "Best" in sDict:
				self.best = sDict["Best"]
			if "StartGame" in sDict:
				self.startGame = sDict["StartGame"]	
			if "Board" in sDict:
				self.board = sDict["Board"]

		#Если новая игра, то добавить первые две цифры
		if self.startGame:
			self.board = self.totalCell(self.board)
			self.board = self.totalCell(self.board)
			self.startGame = False

		#Пустая клетка доски
		self.drowFreeCell = pygame.Surface((CELL_SIZE, CELL_SIZE))
		self.drowFreeCell.fill(pygame.Color("#CCC0B3"))

		#Индикатор начала движения
		self.startMove = False

		#Передвинута ли доска
		self.boardMove = False

		#Новая доска, счет и карта передвижений
		self.newBoard = None
		self.moveMap = None
		self.newScore = None

		#Кнопка
		self.keyDown = ""


	def freeCell(self, board):
		""" Возвращает массив пар [i.j, i.j] со свободными клетками """
		res = []
		i=j=0
		for i in range(self.mode):
			for j in range(self.mode):
				if not board[i][j]:
					res.append(float(str(i) + '.' + str(j)))
				
		if len(res) > 0:
			return res
		else:
			return False

	def totalCell(self, board):
		""" Добавляет одно новое число на пустое место """
		freeCell = self.freeCell(board) #Свободные клетки
		if not freeCell:
			return False
		numList = [2,2,2,2,2,2,2,4,4,4] #Список для рандомного выбора числа
		num = random.choice(numList) #число
		cell = random.choice(freeCell) #ячейка в виде вещественного числа

		cellRow = int(str(cell).split(".")[0]) # i
		cellCol = int(str(cell).split(".")[1]) # j

		newBoard = board[:]
		newBoard[cellRow][cellCol] = num
		return newBoard

	def move(self, up, down, left, right):
		""" Вернет новую доску, карту перемещений, и счёт """
		newBoard = [] #Новая доска
		#Скопировать доску
		for i in range(self.mode):
			tempDict = []
			for j in range(self.mode):
				tempDict.append(self.board[i][j])
			newBoard.append(tempDict)

		newScore = self.score
		cellMoves = [] # Все передвижения клеток для анимации. Ужасный трёхмерный массив

		#Массив где указано расположение всех клеток после перемещения
		cellPlace = []
		for i in range(self.mode):
			tempDict = []
			for j in range(self.mode):
				tempDict.append([str(i)+str(j)]) 
			cellPlace.append(tempDict)

		### Перемещение по кнопке вверх ###
		if up:
			for col in range(self.mode):
				base = 0; #базовая строка
				row = 1;  #строка проверки
				while row < self.mode:
					noMove = True #Не помещать в карту передвижений
					#Если проверяемая строка 0, то проверять следующую
					if newBoard[row][col] == 0:
						row += 1
						noMove = False # не перемещать

					#Если в базе 0, а в проверяемой число, сдвинуть число в базу
					elif newBoard[base][col] == 0 and newBoard[row][col] != 0:
						newBoard[base][col] = newBoard[row][col]
						newBoard[row][col] = 0
						cellPlace[base][col][0] = cellPlace[row][col][0]
						cellPlace[row][col][0] = 0
						row += 1

					#Если база и проверка совпадают, сложить, сместить, проверять следующие строки
					elif newBoard[base][col] == newBoard[row][col]:
						newBoard[base][col] += newBoard[row][col]
						newBoard[row][col] = 0
						newScore += newBoard[base][col] # обновить счет
						cellPlace[base][col].append(cellPlace[row][col][0])
						cellPlace[row][col][0] = 0
						base += 1
						row += 1

					#Если база и проверка - не равны и не 0, проверяемый назад если там 0
					#либо проверять следующие
					elif newBoard[base][col] != newBoard[row][col] and (newBoard[base][col] != 0 and newBoard[row][col] != 0):
						if newBoard[row-1][col] == 0:
							newBoard[row-1][col] = newBoard[row][col]
							newBoard[row][col] = 0
							cellPlace[row-1][col][0] = cellPlace[row][col][0]
							cellPlace[row][col][0] = 0
							row -= 1
						else:
							base +=1
							row += 1
							noMove = False # не перемещать

		### Перемещение по кнопке вниз ###
		elif down:
			for col in range(self.mode):
				base = self.mode-1; #базовая строка
				row = self.mode-2;  #строка проверки
				while row > -1:
					noMove = True #Не помещать в карту передвижений
					if newBoard[row][col] == 0:
						row -= 1
						noMove = False # не перемещать

					elif newBoard[base][col] == 0 and newBoard[row][col] != 0:
						newBoard[base][col] = newBoard[row][col]
						newBoard[row][col] = 0
						cellPlace[base][col][0] = cellPlace[row][col][0]
						cellPlace[row][col][0] = 0
						row -= 1

					elif newBoard[base][col] == newBoard[row][col]:
						newBoard[base][col] += newBoard[row][col]
						newBoard[row][col] = 0
						newScore += newBoard[base][col] # обновить счет
						cellPlace[base][col].append(cellPlace[row][col][0])
						cellPlace[row][col][0] = 0
						base -= 1
						row -= 1

					elif newBoard[base][col] != newBoard[row][col] and (newBoard[base][col] != 0 and newBoard[row][col] != 0):
						if newBoard[row+1][col] == 0:
							newBoard[row+1][col] = newBoard[row][col]
							newBoard[row][col] = 0
							cellPlace[row+1][col][0] = cellPlace[row][col][0]
							cellPlace[row][col][0] = 0
							row += 1
						else:
							base -=1
							row -= 1
							noMove = False # не перемещать

		### Перемещение по кнопке налево ###
		elif left:
			for col in range(self.mode):
				base = 0; #базовая строка
				row = 1;  #строка проверки
				while row < self.mode:
					noMove = True #Не помещать в карту передвижений
					if newBoard[col][row] == 0:
						row += 1
						noMove = False # не перемещать

					elif newBoard[col][base] == 0 and newBoard[col][row] != 0:
						newBoard[col][base] = newBoard[col][row]
						newBoard[col][row] = 0
						cellPlace[col][base][0] = cellPlace[col][row][0]
						cellPlace[col][row][0] = 0
						row += 1

					elif newBoard[col][base] == newBoard[col][row]:
						newBoard[col][base] += newBoard[col][row]
						newBoard[col][row] = 0
						newScore += newBoard[col][base] # обновить счет
						cellPlace[col][base].append(cellPlace[col][row][0])
						cellPlace[col][row][0] = 0
						base += 1
						row += 1

					elif newBoard[col][base] != newBoard[col][row] and (newBoard[col][base] != 0 and newBoard[col][row] != 0):
						if newBoard[col][row-1] == 0:
							newBoard[col][row-1] = newBoard[col][row]
							newBoard[col][row] = 0
							cellPlace[col][row-1][0] = cellPlace[col][row][0]
							cellPlace[col][row][0] = 0
							row -= 1
						else:
							base +=1
							row += 1
							noMove = False # не перемещать

		### Перемещение по кнопке направо ###
		elif right:
			for col in range(self.mode):
				base = self.mode-1; #базовая строка
				row = self.mode-2;  #строка проверки
				while row > -1:
					noMove = True #Не помещать в карту передвижений
					if newBoard[col][row] == 0:
						row -= 1
						noMove = False # не перемещать

					elif newBoard[col][base] == 0 and newBoard[col][row] != 0:
						newBoard[col][base] = newBoard[col][row]
						newBoard[col][row] = 0
						cellPlace[col][base][0] = cellPlace[col][row][0]
						cellPlace[col][row][0] = 0
						row -= 1

					elif newBoard[col][base] == newBoard[col][row]:
						newBoard[col][base] += newBoard[col][row]
						newBoard[col][row] = 0
						newScore += newBoard[col][base] # обновить счет
						cellPlace[col][base].append(cellPlace[col][row][0])
						cellPlace[col][row][0] = 0
						base -= 1
						row -= 1

					elif newBoard[col][base] != newBoard[col][row] and (newBoard[col][base] != 0 and newBoard[col][row] != 0):
						if newBoard[col][row+1] == 0:
							newBoard[col][row+1] = newBoard[col][row]
							newBoard[col][row] = 0
							cellPlace[col][row+1][0] = cellPlace[col][row][0]
							cellPlace[col][row][0] = 0
							row += 1
						else:
							base -=1
							row -= 1
							noMove = False # не перемещать
		else:
			return False

		#Cоздание карты перемещений
		for i in range(self.mode):
			for j in range(self.mode):
				if not cellPlace[i][j][0]: continue
				#если первая клетка не на своём месте, она подвинулась, записать в карту
				if cellPlace[i][j][0] != str(i)+str(j):
					cellIndex = cellPlace[i][j][0]
					start = [int(cellIndex[0]), int(cellIndex[1])]
					end = [i, j]
					cellMoves.append([start, end])
				#Если в массиве указаны две клетки, значит вторая переместилась из другого места, записать её в карту
				if len(cellPlace[i][j]) > 1:
					cellIndex = cellPlace[i][j][1]
					start = [int(cellIndex[0]), int(cellIndex[1])]
					end = [i, j]
					cellMoves.append([start, end])

		return newBoard, cellMoves, newScore #Новая доска, Карта перемещений, счет

	def update(self, cellObjects, textObjects, moveMap):
		""" Обновляет доску после нажатия на кнопку """
		if not self.startMove or self.keyDown == "":
			print("Ошибка. Движение не началось")
			return False

		moveEnd = True #все клктки перемещены
		for val in moveMap:
			#Координаты начала и конца движения клетки в виде [1, 1]...
			fromCoor = [val[0][0], val[0][1]]
			toCoor = [val[1][0], val[1][1]]
			#Перевести координаты в пиксели
			fromPx = [GAME_BEGIN_Y + CELL_SIZE*fromCoor[0] + CELL_IND*fromCoor[0],
					  GAME_BEGIN_X + CELL_SIZE*fromCoor[1] + CELL_IND*fromCoor[1]]
			toPx = [GAME_BEGIN_Y + CELL_SIZE*toCoor[0] + CELL_IND*toCoor[0],
					GAME_BEGIN_X + CELL_SIZE*toCoor[1] + CELL_IND*toCoor[1]]

			index = str(fromCoor[0]) + '.' + str(fromCoor[1]) #ключ текущего объекта
			if self.keyDown == "up":
				#Если координаты текущей клетки НЕ равны её конечной позиции
				#то продолжаем движение

				if cellObjects[index].rect.y >= toPx[0]+4:
					cellObjects[index].rect.y -= 4 #Двигаем вверх
					textObjects[index].rect.y -= 4 #Двигаем вверх
					moveEnd = False #Движение не закончено

			if self.keyDown == "down":
				#Двигаем если клетка не на месте
				if cellObjects[index].rect.y <= toPx[0]-4:
					cellObjects[index].rect.y += 4 #Двигаем вниз
					textObjects[index].rect.y += 4 #Двигаем вниз
					moveEnd = False #Движение не закончено

			if self.keyDown == "left":
				#Двигаем если клетка не на месте
				if cellObjects[index].rect.x >= toPx[1]+4:
					cellObjects[index].rect.x -= 4 #Двигаем влево
					textObjects[index].rect.x -= 4 #Двигаем влево
					moveEnd = False #Движение не закончено

			if self.keyDown == "right":
				#Двигаем если клетка не на месте
				if cellObjects[index].rect.x <= toPx[1]-4:
					cellObjects[index].rect.x += 4 #Двигаем влево
					textObjects[index].rect.x += 4 #Двигаем влево
					moveEnd = False #Движение не закончено

		return moveEnd


	def drowCellBack(self, screen, x, y):
		""" Рисует пустые клетки в которых будут размещаться числа """
		i=j=0
		for i in range(self.mode):
			for j in range(self.mode):
				cellX = x + CELL_SIZE*i + CELL_IND*i
				cellY = y + CELL_SIZE*j + CELL_IND*j
				screen.blit(self.drowFreeCell, (cellX,cellY))

	def drowFullCells(self, cellGroup, textGroup):
		""" Рисует заполненные клетки """
		cellSprites = {}
		textSprites = {}
		for i in range(self.mode):
			for j in range(self.mode):
				if self.board[i][j]:
					#Считает позицию клеток
					cellPosY = GAME_BEGIN_Y + CELL_SIZE*i + CELL_IND*i
					cellPosX = GAME_BEGIN_X + CELL_SIZE*j + CELL_IND*j
					cellPos = str(i)+'.'+str(j)
					#Создает спрайты
					cellSprites[cellPos] = cell.Cell(cellPosX, cellPosY, self.board[i][j])
					cellGroup.add(cellSprites[cellPos])
					textSprites[cellPos] = text.Text(cellPosX, cellPosY, self.board[i][j])
					textGroup.add(textSprites[cellPos])
		return cellSprites, textSprites

	def winner(self, board):
		""" Победил ли пользователь """
		win = False
		for i in range(self.mode):
			for j in range(self.mode):
				if board[i][j] == 2048:
					win = True
		return win

	def isMove(self, board):
		""" Проверяет есть ли ещё ходы """
		lose = False
		newBoard1, cellMoves1, newScore1 = self.move(1,0,0,0)
		newBoard2, cellMoves2, newScore2 = self.move(0,1,0,0)
		newBoard3, cellMoves3, newScore3 = self.move(0,0,1,0)
		newBoard4, cellMoves4, newScore4 = self.move(0,0,0,1)

		#Если все ходы возвращают пустую карту перемещений, значит пользователь проиграл
		if len(cellMoves1) == 0 and \
		   len(cellMoves2) == 0 and \
		   len(cellMoves3) == 0 and \
		   len(cellMoves4) == 0:
			lose = True

		return lose

	def newGame(self):
		""" Настройка новой игры """
		self.board = []
		for i in range(self.mode):
			tempDict = []
			for j in range(self.mode):
				tempDict.append(0)
			self.board.append(tempDict)

		self.board = self.totalCell(self.board)
		self.board = self.totalCell(self.board)
		self.newBoard = self.board
		self.score = 0

	def getKeyDown(self):
		""" Выводит нажатую кнопку """
		return self.keyDown

	def setKeyDown(self, value):
		""" Изменяет нажатую кнопку """
		self.keyDown = value

	def getBoard(self):
		""" Возвращает доску """
		return self.board

	def setBoard(self, newBoard):
		""" Изменяет доску """
		self.board = []
		#Скопировать доску
		for i in range(self.mode):
			tempDict = []
			for j in range(self.mode):
				tempDict.append(newBoard[i][j])
			self.board.append(tempDict)

	def getMode(self):
		""" Возвращает размер доски """
		return self.mode

	def getScore(self):
		""" Возвращает счет """
		return self.score

	def setScore(self, newScore):
		""" Изменяет счет """
		self.score = newScore

	def getBest(self):
		""" Возвращает лучший счет """
		return self.best

	def setBest(self, newBest):
		""" Изменяет лучший счет """
		self.best = newBest

	def getStartMove(self):
		""" Возвращает: Индикатор начала движения """
		return self.startMove

	def setStartMove(self, newStartMove):
		""" Изменяет: Индикатор начала движения """
		self.startMove = newStartMove

	def getBoardMove(self):
		""" Возвращает: Передвинута ли доска """
		return self.boardMove

	def setBoardMove(self, newBoardMove):
		""" Изменяет: Передвинута ли доска """
		self.boardMove = newBoardMove

	def getNewBoard(self):
		""" Возвращают новую доску """
		return self.newBoard

	def setNewBoard(self, board):
		""" Изменяет новую доску """
		self.newBoard = board

	def getMoveMap(self):
		""" Возвращает карту перемещений """
		return self.moveMap

	def setMoveMap(self, newMoveMap):
		""" Изменяет карту перемещений """
		self.moveMap = newMoveMap

	def getNewScore(self):
		""" Возвращает новый счет """
		return self.newScore

	def setNewScore(self, score):
		""" Изменяет новый счет """
		self.newScore = score


