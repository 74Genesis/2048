cellMode = 4 #Размер поля

CELL_SIZE = 60 #Размер клетки

ELEM_IND = 15 #Отступ между элементами окна 
CELL_IND = 10 #Отступ между клетками
BUT_HEIGHT = 50 #Высота кнопок/полей с информацией

#Фон доски = отступ клеток * кол-во клеток+1 + кол-во клеток * размер клетки
BOARD_SIZE = CELL_IND*(cellMode+1) + cellMode*CELL_SIZE

#Координаты начала и конца игрового поля
GAME_BEGIN_X = ELEM_IND + CELL_IND
GAME_BEGIN_Y = ELEM_IND*2 + BUT_HEIGHT + CELL_IND
# GAME_END_X = GAME_BEGIN_X + (BOARD_SIZE - CELL_IND*2)
# GAME_END_Y = GAME_BEGIN_Y + (BOARD_SIZE - CELL_IND*2)