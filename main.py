import pygame
import cell # клетка
import settings # настройки
import board # доска
from const import * # константы

#Размер окна
WIN_WIDTH = ELEM_IND*2 + BOARD_SIZE
WIN_HEIGHT = ELEM_IND*3 + 50 + BOARD_SIZE


def main():
	global board, settings

	pygame.init()
	pygame.font.init()
	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	pygame.display.set_caption("2048 by 74Genesis")
	font = pygame.font.Font("font/ClearSans-Bold.ttf", 18)
	fontScore = pygame.font.Font("font/ClearSans-Bold.ttf", 13)

	#Основной "холст"
	mainSur = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
	mainSur.fill(pygame.Color("#faf8ef"))

	# Кнопка Новая игра
	restartBut = pygame.Surface((100, 50))
	restartBut.fill(pygame.Color("#8f7a66"))
	#текст New game
	nGame = font.render("New Game", True, (249,246,242))	

	# Счет
	score = pygame.Surface((80, 50))
	score.fill(pygame.Color("#bbada0"))
	#score
	scoreText = font.render("Score", True, (249,246,242))
	#score число
	scoreNum = None

	# Лучший счет
	bestScore = pygame.Surface((80, 50))
	bestScore.fill(pygame.Color("#bbada0"))
	bestText = font.render("Best", True, (249,246,242))

	#фон доски
	boardBg = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
	boardBg.fill(pygame.Color("#bbada0"))

	board = board.Board()
	# board.board = [[2, 256, 3, 7],
 #       		  	  [2, 128, 4, 8],
	#    		  	  [1024, 64, 5, 9],
	#    		  	  [1024, 32, 6, 34]]

	#Нарисовать заполненные клетки
	cellObjects, textObjects = board.drowFullCells(cellGroup, textGroup)

	pygame.key.set_repeat(1, 400)
	clock = pygame.time.Clock()
	scoreNumX = 0
	while 1:
		clock.tick(400)
		up=down=left=right=False
		#Закрыть окно
		for e in pygame.event.get():
			#Перед выходом сохранить в файл все настройки
			if e.type == pygame.QUIT:
				settings = settings.Settings()
				settings.changeOption("Score", board.getScore())
				settings.changeOption("Best", board.getBest())
				settings.changeOption("StartGame", False)
				settings.changeOption("Board", board.getBoard())
				raise SystemExit

			#Проверять нажатие клавиши только если не осуществляется движение доски
			if not board.startMove:
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_UP:
						up = True
					elif e.key == pygame.K_DOWN:
						down = True
					elif e.key == pygame.K_LEFT:
						left = True
					elif e.key == pygame.K_RIGHT:
						right = True
			if e.type == pygame.MOUSEBUTTONDOWN:
				mousePos = pygame.mouse.get_pos()
				if mousePos[0] > ELEM_IND and \
				   mousePos[0] < ELEM_IND+100 and \
				   mousePos[1] > ELEM_IND and \
				   mousePos[1] < ELEM_IND+50:
					board.newGame()
					#Удалить старые спрайты клеток и текста
					for key in cellObjects:
						cellGroup.remove(cellObjects[key])
					for key in textObjects:
						textGroup.remove(textObjects[key])
					cellObjects, textObjects = board.drowFullCells(cellGroup, textGroup) 


		#Если нажата кнопка управления полем
		if up or down or left or right:
			board.setStartMove(True) #начинаем передвижение
			board.setBoardMove(False) #Пересчитана ли доска
			#запоминаем нажатую кнопку
			if up: board.setKeyDown("up")
			if down: board.setKeyDown("down")
			if left: board.setKeyDown("left")
			if right: board.setKeyDown("right")

		#Пока активировано передвижение, изменяем доску
		if board.getStartMove():
			if board.getKeyDown() == "up": up = True
			if board.getKeyDown() == "down": down = True
			if board.getKeyDown() == "left": left = True
			if board.getKeyDown() == "right": right = True
			
			if not board.getBoardMove():
				nBoard, moveMap, nScore = board.move(up, down, left, right)
				board.setNewBoard(nBoard)
				board.setMoveMap(moveMap)
				board.setNewScore(nScore)

				board.setBoardMove(True)

			updateRes = board.update(cellObjects, textObjects, board.moveMap) #двигает клетки

			if updateRes: #Все клетки передвинуты
				board.setBoardMove(False)
				if len(board.getMoveMap()) > 0: # если ячейки двигались
					boardNewNum = board.totalCell(board.getNewBoard()) #добавить ещё одну цифру
					board.setBoard(boardNewNum) #сохранить новую доску
				
				#Удалить старые спрайты клеток и текста
				for key in cellObjects:
					cellGroup.remove(cellObjects[key])
				for key in textObjects:
					textGroup.remove(textObjects[key])

				cellObjects, textObjects = board.drowFullCells(cellGroup, textGroup) #Создать новые
				board.setStartMove(False) #Индикатор движения выключить

				board.setScore(board.getNewScore()) #Обновить счет

				#Если лучший счет меньше основного, обновить его
				if board.getBest() < board.getScore():
					board.setBest(board.getScore())

				#Проверяем не проиграл ли пользователь
				# if board.isMove(board.getNewBoard()):
				# 	print("Конец игры")

				#Победил ли пользователь
				# if board.winner(board.getNewBoard()):
				# 	print("Победитель !")

		#Создание числа "Счет" и "Лучший счет"
		scoreNum = fontScore.render(str(board.getScore()), True, (249,246,242))
		bestNum = fontScore.render(str(board.getBest()), True, (249,246,242))

		#Рисование всех элементов
		#Главный "Холст"
		screen.blit(mainSur, (0,0)) 
		#Новая игра
		screen.blit(restartBut, (ELEM_IND,ELEM_IND)) 
		#New game
		screen.blit(nGame, (ELEM_IND+7, ELEM_IND+11)) 
		#cчет
		screen.blit(score, (115+ELEM_IND,ELEM_IND)) 
		screen.blit(scoreText, (147, ELEM_IND)) #Текст score
		scoreNumX = numAlignCenter(str(board.getScore()), 115+ELEM_IND, 80) #позиция числа
		screen.blit(scoreNum, (scoreNumX, ELEM_IND+25)) #Число score
		#Лучший счет
		screen.blit(bestScore, (115+80+ELEM_IND*2,ELEM_IND)) 
		screen.blit(bestText, (115+80+ELEM_IND*2 + 23, ELEM_IND)) #Текст best
		bestNumX = numAlignCenter(str(board.getBest()), 115+80+ELEM_IND*2, 80) #позиция числа
		screen.blit(bestNum, (bestNumX, ELEM_IND+25)) #Число best
		#фон доски
		screen.blit(boardBg, (ELEM_IND,ELEM_IND*2 + 50)) 

		board.drowCellBack(screen, GAME_BEGIN_X, GAME_BEGIN_Y) #пустые клетки
			
		cellGroup.draw(screen)
		textGroup.draw(screen)
		pygame.display.update()


def numAlignCenter(num, startX, blockWidth):
	""" Возвращает координаты для размещения цифр счёта по центру """
	resX = 0
	num = len(num)
	if num == 1:
		resX = startX + blockWidth/2 - 5
	if num == 2:
		resX = startX + blockWidth/2 - 10
	if num == 3:
		resX = startX + blockWidth/2 - 14
	if num == 4:
		resX = startX + blockWidth/2 - 16
	if num == 5:
		resX = startX + blockWidth/2 - 20
	if num == 6:
		resX = startX + blockWidth/2 - 23
	if num == 7:
		resX = startX + blockWidth/2 - 27
	if num == 8:
		resX = startX + blockWidth/2 - 32
	return resX


cellGroup = pygame.sprite.Group()
textGroup = pygame.sprite.Group()

ent = pygame.sprite.Group()
ent2 = pygame.sprite.Group()
main()

