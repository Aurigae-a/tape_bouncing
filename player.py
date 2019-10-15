from tape import Tape

class Player:
	"""
	这个类用来实现玩家
	"""
	def __init__(self, NO): 
		"""
		构造函数
		"""
		# 玩家的编号
		self.playerNO = NO

		# 表示玩家是否在游戏的flag
		self.isPlaying = True

	def bindTape(self, myTape):
		"""
		给玩家绑定胶带
		"""
		# 玩家的胶带
		self.myTape = myTape
		myTape.player = self

