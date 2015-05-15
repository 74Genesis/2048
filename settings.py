import os
import pickle
import shelve

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
		if not self.__openFile():
			open(FILE_NAME + ".dat", 'w', encoding="utf-8")
			#Записать в него дефолтные настройки
			if self.__openFile():
				self.settFile["Settings"] = DEFAULT_SETTINGS
				self.settFile.sync()
				self.settFile.close()


	def __openFile(self):
		""" Открывает файл настроек """
		if os.path.exists(FILE_NAME + ".dat"):
			try:
				self.settFile = shelve.open(FILE_NAME, "c")
				return True
			except:
				print("Ошибка открытия файла")
				return False
		else:
			return False

	def getOption(self, option):
		""" Возвращает одну опцию из списка настроек """
		self.option = option
		if self.__openFile(): #Если настройки открылись
			#Вернуть опцию
			if self.option in self.settFile["Settings"]:
				result = self.settFile["Settings"][option]
				self.settFile.sync()
				self.settFile.close()
				return result
			else:
				return False

	def getSettings(self):
		""" Возвращает одну опцию из списка настроек """
		if self.__openFile(): #Если настройки открылись
			result = self.settFile["Settings"]
			self.settFile.sync()
			self.settFile.close()
			return result
		else:
			return False

	def changeOption(self, option, var):
		""" Изменяет значение опции """
		self.option = option
		self.var = var
		if self.__openFile():
			if self.option in self.settFile["Settings"]:
				self.settFile["Settings"].update({self.option: self.var})
				#Сразу не меняется, поэтому передать в переменную, потом заного присвоить
				tempDict = self.settFile["Settings"]; 
				tempDict.update({self.option: self.var}) #Обновить опцию
				self.settFile["Settings"] = tempDict

				self.settFile.sync()
				self.settFile.close()
				return True
			else:
				return False
		else:
			return False




# test = Settings()
# print(test.getSettings())