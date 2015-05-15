import os
import pickle

DEFAULT_SETTINGS = {
	"Score": 0, # счет
	"Best": 0, # лучший счет
	"StartGame": True, # определяет начало игры
	"Board": [[0, 0, 0, 0], #доска
			  [0, 0, 0, 0],
			  [0, 0, 0, 0],
			  [0, 0, 0, 0]],
	"Mode": 4 # размер доски
}
FILE_NAME = "Settings"

class Settings():
	""" Настройки игры """
	def __init__(self):
		self.settFile = None #Если всё ок, файл будет передаваться этой переменной

		#Если файл не открывается, создать новый
		self.__openFile()
			# f = open(FILE_NAME + ".dat", 'wb')
			# pickle.dump(DEFAULT_SETTINGS, f)
			# f.close()
			#Записать в него дефолтные настройки
			# if self.__openFile():
			# 	pickle.dump(DEFAULT_SETTINGS, self.settFile)
			# 	self.settFile.close()


	def __openFile(self):
		""" Открывает файл настроек """
		try:
			f = open(FILE_NAME + ".dat", "rb")
			self.settFile = pickle.load(f)
			f.close()
			return True
		except:
			f = open(FILE_NAME + ".dat", 'wb')
			pickle.dump(DEFAULT_SETTINGS, f)
			f = open(FILE_NAME + ".dat", "rb")
			self.settFile = pickle.load(f)
			f.close()
			return True
			

	def getOption(self, option):
		""" Возвращает одну опцию из списка настроек """
		self.__openFile()
		if option in self.settFile:
			return self.settFile[option]
		else:
			return False

	def getSettings(self):
		""" Возвращает все настройки """
		self.__openFile()
		return self.settFile

	def changeOption(self, option, var):
		""" Изменяет значение опции """
		self.__openFile()
		if option not in self.settFile:
			return False

		self.settFile[option] = var
		f = open(FILE_NAME + ".dat", 'wb')
		pickle.dump(self.settFile, f)
		f.close()



# test = Settings()
# # print(test.settFile)
# print(test.getOption("Mode"))
# print(test.changeOption("Mode", 8))
# print(test.getOption("Mode"))
