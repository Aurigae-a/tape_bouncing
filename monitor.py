from player import Player
from tape import Tape
from barrier import Barrier
from obstacle import Obstacle
import pygame
from pygame.locals import *
import sys

class Monitor:
	"""
	这个类用来实现游戏的后台监控器
	"""
	def __init__(self):
		"""
		构造函数
		"""
		# 主窗体大小
		self.width  = 1280
		self.height = 720

		# 胶带的半径
		self.tapeRadius = 30

		# 边界的长度
		self.boundObstRadius = 30

		# 障碍物的长度
		self.obstacleRadius = 60

		# 标注游戏运行状态的label，0：第一次进入的画面 1：初始化询问状态、2：游戏状态、3:游戏后统计状态
		self.state = 0

		# 标注回合的状态的label，0～7，玩家输入状态，isSimulating表示是否在仿真
		self.turn 		  = 0
		self.isSimulating = False

		# 玩家的数量
		self.playersNumber = 0

		# 玩家列表
		self.playersList = []

		# 障碍物列表
		self.obstacleList = []

		# 玩家激励的上限
		self.maxForce = 20
		
		# 玩家激励显示格子的长度和最大高度
		self.forceBoxWidth = 40
		self.forceBoxMaxHeight = 100

		# 出生位置的字典
		self.initPositionDict = {0 : (self.width/2+90, self.height/2), 
								 1 : (self.width-self.tapeRadius-self.boundObstRadius-self.boundObstRadius-1, self.tapeRadius+self.boundObstRadius+1),
								 2 : (self.width/2, self.height/2+90), 
								 3 : (self.tapeRadius+self.boundObstRadius+1, self.tapeRadius+self.boundObstRadius+1),  
								 4 : (self.width/2-90, self.height/2), 
								 5 : (self.tapeRadius+self.boundObstRadius+1, self.height-self.tapeRadius-self.boundObstRadius-1), 
								 6 : (self.width/2, self.height/2-90), 
								 7 : (self.width-self.tapeRadius-self.boundObstRadius-1, self.height-self.tapeRadius-self.boundObstRadius-1) }
		
		# 不同数量的不同出生位置的字典
		self.initNO = {	2 : (0,4), 
						3 : (0,2,4), 
						4 : (0,2,4,6), 
						5 : (0,1,2,4,6), 
						6 : (0,1,2,3,4,6), 
						7 : (0,1,2,3,4,5,6), 
						8 : (0,1,2,3,4,5,6,7) }
		
		# 障碍物的位置的列表
		self.obstaclePos = [[100, 100], 
							[100, self.height/2], 
							[100, self.height-100], 
							[self.width/2, 100], 
							[self.width/2, self.height-100], 
							[self.width-100, 100], 
							[self.width-100, self.height/2], 
							[self.width-100, self.height-100]]
		
		# 初始化pygame
		pygame.init()

		# 游戏主窗口
		self.mainWindow = pygame.display.set_mode((self.width,self.height),0)
		# 设置主窗口标题
		pygame.display.set_caption('bouncer')
		# 设置刷新率
		self.videoClock = pygame.time.Clock()
		self.videoClock.tick(40)
		
		# 第一次登陆时候的界面
		self.firstPic = pygame.image.load('./pic/title.png').convert()
		self.firstPic = pygame.transform.scale(self.firstPic, (self.width, self.height))

		# 初始化询问界面需要用到的一些文字、文本输入框、按钮
		# 背景图片
		self.backgroundPic = pygame.image.load('./pic/title_1.png').convert()
		# 标题
		self.font0 = pygame.font.Font('./fonts/SEGOESCB.TTF',60)
		self.askingTitle = self.font0.render("Welcome to bouncer!", True, (255,255,0))
		# 询问数字的文字
		self.font1 = pygame.font.Font('./fonts/SEGOESCB.TTF',30)
		self.askingNumber = self.font1.render("How much players (2~4): ", True, (255,255,0))
		# 数字输入框
		self.askingInputStr = ""
		# 按钮
		self.askingButton = self.font1.render("OK", True, (255,255,0), (0,255,0))
		
		# 游戏阶段需要用到的一些图片
		# 球台背景照片
		self.playingBackground = pygame.image.load('./pic/table.png').convert_alpha()
		self.playingBackground = pygame.transform.scale(self.playingBackground, (self.width, self.height))
		# 胶带图片
		self.playingTapePic = pygame.image.load('./pic/tape_pic.png').convert_alpha()
		self.playingTapePic = pygame.transform.scale(self.playingTapePic, (2*self.tapeRadius, 2*self.tapeRadius))
		# 标注玩家编号的字体
		self.playingNOFont = pygame.font.Font(None,20)
		# 边框的三种形态的照片
		self.barrierPic1 = pygame.image.load('./pic/barrier.png').convert_alpha()
		self.barrierPic2 = pygame.image.load('./pic/barrier_crack1.png').convert_alpha()
		self.barrierPic3 = pygame.image.load('./pic/barrier_crack2.png').convert_alpha()
		# 障碍物的三种形态的照片
		self.obstaclePic1 = pygame.image.load('./pic/obstacle.png').convert_alpha()
		self.obstaclePic1 = pygame.transform.scale(self.obstaclePic1, (2*self.obstacleRadius, 2*self.obstacleRadius))
		self.obstaclePic2 = pygame.image.load('./pic/obstacle_crack1.png').convert_alpha()
		self.obstaclePic2 = pygame.transform.scale(self.obstaclePic2, (2*self.obstacleRadius, 2*self.obstacleRadius))
		self.obstaclePic3 = pygame.image.load('./pic/obstacle_crack2.png').convert_alpha()
		self.obstaclePic3 = pygame.transform.scale(self.obstaclePic3, (2*self.obstacleRadius, 2*self.obstacleRadius))

		# 游戏结束阶段需要用到的一些文字和按钮
		# 再来一局按钮
		self.finishedAgainButton = self.font1.render("Play again", True, (255,255,0), (0,255,0))
		# 结束按钮
		self.finishedQuitButton = self.font1.render("Quit", True, (255,255,0), (255,0,0))
		

	def mainLoop(self): 
		"""
		游戏的主循环体
		"""
		# 初始化用户询问界面结束的flag
		askingFinished = False

		while True:
			self.videoClock.tick(80)

			# 填充背景色
			self.mainWindow.fill((255,255,255))

			if self.state == 0:
				# 第一次进入的界面
				for event in pygame.event.get():
					# 退出事件
					if event.type == QUIT:
						pygame.quit()
						sys.exit()
					elif event.type == KEYDOWN or event.type == MOUSEBUTTONUP:
						self.state = 1
				
				self.mainWindow.blit(self.firstPic,(0,0))

			elif self.state == 1:
				# 初始化询问界面

				# 用户询问界面下的事件处理
				for event in pygame.event.get():
					# 退出事件
					if event.type == QUIT:
						pygame.quit()
						sys.exit()
					# 键盘按下事件
					if event.type == KEYDOWN:
						if event.key == 8 and len(self.askingInputStr) != 0: self.askingInputStr = self.askingInputStr[0:len(self.askingInputStr)-1] # 按键 Backspace
						elif event.key == 48 or event.key == 256:	self.askingInputStr += "0" # 按键 0
						elif event.key == 49 or event.key == 257:	self.askingInputStr += "1" # 按键 1
						elif event.key == 50 or event.key == 258:	self.askingInputStr += "2" # 按键 2
						elif event.key == 51 or event.key == 259:	self.askingInputStr += "3" # 按键 3
						elif event.key == 52 or event.key == 260:	self.askingInputStr += "4" # 按键 4
						elif event.key == 53 or event.key == 261:	self.askingInputStr += "5" # 按键 5
						elif event.key == 54 or event.key == 262:	self.askingInputStr += "6" # 按键 6
						elif event.key == 55 or event.key == 263:	self.askingInputStr += "7" # 按键 7
						elif event.key == 56 or event.key == 264:	self.askingInputStr += "8" # 按键 8
						elif event.key == 57 or event.key == 265:	self.askingInputStr += "9" # 按键 9
					# 鼠标左键按下事件
					elif event.type == MOUSEBUTTONDOWN and (pygame.mouse.get_pressed())[0] == 1:
						askingFinished = True
					# 鼠标左键抬起事件
					elif event.type == MOUSEBUTTONUP and askingFinished == True:
						# 获取鼠标的位置
						mouse_x = pygame.mouse.get_pos()[0]
						mouse_y = pygame.mouse.get_pos()[1]
						askingButtonRect = self.askingButton.get_rect()
						# 检查鼠标点击的位置是否在按键中
						if self.width/4+300 < mouse_x < self.width/4+300+askingButtonRect.width and (self.height)/2 < mouse_y < (self.height)/2+askingButtonRect.height:
							# 只有当数量在2到8之间的时候才通过
							if len(self.askingInputStr) != 0:	
								# 将字符串转化成数字
								playersNumber = int(self.askingInputStr)
								if 2 <= playersNumber <= 4:
									# 记录玩家的数量
									self.playersNumber = playersNumber
									# 初始分配位置元组
									initNO = self.initNO[self.playersNumber]
									# 创建玩家和胶带
									for m1 in range(self.playersNumber): 
										# 创建玩家
										self.playersList.append(Player(m1))
										# 创建胶带
										tempTape = Tape([self.initPositionDict[initNO[m1]][0], self.initPositionDict[initNO[m1]][1]], self.tapeRadius)
										# 绑定玩家和胶带
										self.playersList[m1].bindTape(tempTape)

									# 创建障碍物
									count = 0
									for tempPos in self.obstaclePos:
										count += 1
										self.obstacleList.append(Obstacle(count, tempPos[0], tempPos[1], self.obstacleRadius))

									self.state = 2
									# 初始化回合标记
									self.turn  = 0
									# 初始化玩家回合标记
									hasFinished = False
									# 初始化玩家激励label
									countingForce = False
									# 鼠标初始位置
									mouse_x = mouse_y = 0
									# 创建边框
									self.boundary = Barrier(self.boundObstRadius, self.width, self.height)
				
				# 画背景图片
				self.mainWindow.blit(self.backgroundPic,(0,0))
				# 画出标题
				self.mainWindow.blit(self.askingTitle,  (self.width/2-self.askingTitle.get_rect().width/2,(self.height)/4))
				# 画出数字询问文字
				self.mainWindow.blit(self.askingNumber, (self.width/4-self.askingNumber.get_rect().width/2,(self.height)/2))
				# 画出对话框
				textField = self.font1.render(self.askingInputStr, True, (255,255,0))
				self.mainWindow.blit(textField, (self.width/4-self.askingNumber.get_rect().width/2+self.askingNumber.get_rect().width,(self.height)/2))
				# 画出按钮
				self.mainWindow.blit(self.askingButton, (self.width/4+300,(self.height)/2))
			
			elif self.state == 2:
				if self.isSimulating:
					# 运动仿真状态
					for event in pygame.event.get():
						# 退出事件
						if event.type == QUIT:
							pygame.quit()
							sys.exit()

					# 所有小球是否都停止的标志
					allStop = True
					# 每个玩家的胶带挨个进行仿真
					for player in self.playersList:
						# 运动仿真
						player.myTape.simulation(self.boundary, self.playersList, self.obstacleList)

						# 检查是否停止
						if player.myTape.moving == True:	allStop = False
					
					if allStop == True:
						# 结束仿真
						self.isSimulating = False
						# 玩家回合结束回置为False
						hasFinished = False
				else:
					# 玩家输入状态
					
					# 统计玩家的数量
					currentPlayer = 0
					for player in self.playersList:
						if player.isPlaying == True:
							currentPlayer += 1
					# 如果玩家数量等于1，那么游戏结束
					if currentPlayer <= 1:
						self.state = 3
					
					# 玩家还未完成弹射操作
					if hasFinished == False:
						for event in pygame.event.get():
							# 退出事件
							if event.type == QUIT:
								pygame.quit()
								sys.exit()
							# 鼠标移动
							elif event.type == MOUSEMOTION:
								mouse_x = event.pos[0]
								mouse_y = event.pos[1]
							# 鼠标按下事件
							elif event.type == MOUSEBUTTONDOWN:
								countingForce = True
								playerForce   = 0.0
							# 鼠标松开事件
							elif event.type == MOUSEBUTTONUP:
								# 停止计力
								countingForce = False
								# 计算方向
								temp_pos = self.playersList[self.turn].myTape.pos
								temp_x = temp_pos[0] - mouse_x
								temp_y = temp_pos[1] - mouse_y
								temp_l = pow(pow(temp_x,2)+pow(temp_y,2), 0.5)
								sin_theta = temp_y / temp_l
								cos_theta = temp_x / temp_l
								# 将玩家激励作为初速度给胶带
								self.playersList[self.turn].myTape.setVelocity([playerForce*cos_theta, playerForce*sin_theta])
								# 玩家本回合操作结束
								hasFinished = True
						# 玩家激励计数
						if countingForce == True:
							playerForce += 0.5
							# 当超过力上限后，置0重新计数
							if playerForce >= self.maxForce:	playerForce = 0.0
					# 玩家已经完成弹射操作
					else:
						# 跳转至下一玩家，
						while True:
							self.turn += 1
							# 如果已经达到了玩家上线，则重新回到0
							if self.turn == self.playersNumber:		self.turn = 0
							# 判断是否是正在游戏的玩家
							if self.playersList[self.turn].isPlaying == True:
								# 进入仿真状态
								self.isSimulating = True
								break

				# 绘制球台背景
				self.mainWindow.blit(self.playingBackground,(0,0))

				# 绘制边框
				if self.boundary.lifeTime == 3:
					self.mainWindow.blit(self.barrierPic1, (0,0))
				elif self.boundary.lifeTime == 2:
					self.mainWindow.blit(self.barrierPic2, (0,0))
				elif self.boundary.lifeTime == 1:
					self.mainWindow.blit(self.barrierPic3, (0,0))

				# 绘制障碍物
				for obstacle in self.obstacleList:
					if obstacle.lifeTime == 3:
						self.mainWindow.blit(self.obstaclePic1, (obstacle.pos[0]-obstacle.radius,obstacle.pos[1]-obstacle.radius))
					elif obstacle.lifeTime == 2:
						self.mainWindow.blit(self.obstaclePic2, (obstacle.pos[0]-obstacle.radius,obstacle.pos[1]-obstacle.radius))
					elif obstacle.lifeTime == 1:
						self.mainWindow.blit(self.obstaclePic3, (obstacle.pos[0]-obstacle.radius,obstacle.pos[1]-obstacle.radius))

				# 如果玩家还未完成该回合，则需要进行划线
				if hasFinished == False:
					pygame.draw.line(self.mainWindow, (0,255,0), self.playersList[self.turn].myTape.pos, (mouse_x, mouse_y), 5)
				
				# 如果玩家正在计力，则需要画出计力格
				if countingForce == True:
					boxHeight = int(playerForce/self.maxForce*self.forceBoxMaxHeight)
					pygame.draw.rect(self.mainWindow, (0,0,0), (self.width-100, self.height-100-self.forceBoxMaxHeight, 
																  self.forceBoxWidth, self.forceBoxMaxHeight))
					pygame.draw.rect(self.mainWindow, (0,0,255), (self.width-100, self.height-100-boxHeight, 
																  self.forceBoxWidth, boxHeight), 0)

				# 绘制胶带
				for player in self.playersList:

					# 判断玩家是否在游戏
					if player.isPlaying:
						# 绘制胶带图形
						self.mainWindow.blit(self.playingTapePic,(int(player.myTape.pos[0])-self.tapeRadius, int(player.myTape.pos[1])-self.tapeRadius))
						# 绘制编号
						self.mainWindow.blit(self.playingNOFont.render(str(player.playerNO+1), True, (0,0,255)), player.myTape.pos)

			elif self.state == 3: 
				# 游戏结束状态，统计是谁获得了胜利
				
				# 绘制背景图
				self.mainWindow.blit(self.backgroundPic,(0,0))

				# 如果剩余玩家数量是0，则没有人获得胜利
				if currentPlayer == 0:
					# 生成表示没有人获得胜利的文字
					textField = self.font0.render("No one wins the game!", True, (255,255,0))
				else:
					# 生成获得胜利的玩家的文字
					for player in self.playersList:
						if player.isPlaying == True:
							winner = player
							break
					
					tempStr = "Player " + str(winner.playerNO+1) + " wins the game!"
					textField = self.font0.render(tempStr, True, (255,255,0))
				
				# 画出结果统计文字
				self.mainWindow.blit(textField, (self.width/2-textField.get_rect().width/2, self.height/4))
				# 画出按钮
				self.mainWindow.blit(self.finishedAgainButton, (self.width/4,3*self.height/4))
				self.mainWindow.blit(self.finishedQuitButton, (3*self.width/4,3*self.height/4))
				
				for event in pygame.event.get():
					# 退出事件
					if event.type == QUIT:
						pygame.quit()
						sys.exit()
					# 鼠标左键抬起事件
					elif event.type == MOUSEBUTTONUP:
						# 获取鼠标的位置
						mouse_x = pygame.mouse.get_pos()[0]
						mouse_y = pygame.mouse.get_pos()[1]
						finishedAgainButtonRect = self.finishedAgainButton.get_rect()
						finishedQuitButtonRect = self.finishedQuitButton.get_rect()
						# 检查鼠标点击的位置是否在再来一次按键中
						if self.width/4 < mouse_x < self.width/4+finishedAgainButtonRect.width and 3*self.height/4 < mouse_y < 3*self.height/4+finishedAgainButtonRect.height:
							# 回到玩家数量询问界面
							self.state = 1
							# 清空玩家列表和玩家数量
							self.playersList.clear()
							self.playersNumber = 0
							self.obstacleList.clear()
						# 检查鼠标点击的位置是否在退出按键中
						if 3*self.width/4 < mouse_x < 3*self.width/4+finishedQuitButtonRect.width and 3*self.height/4 < mouse_y < 3*self.height/4+finishedQuitButtonRect.height:
							pygame.quit()
							sys.exit()

			# 刷新屏幕
			pygame.display.update()

	

	# def initAskingWindow(self): 
	# 	"""
	# 	初始化用户询问界面
	# 	"""
	# 	render = 




m1 = Monitor()
m1.mainLoop()