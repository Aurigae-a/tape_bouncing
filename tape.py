
class Tape:
    """
    这个类实现了胶带
    """
    def __init__(self, init_pos, init_radius):
        """
        构造函数
        """
        # 玩家的编号
        self.playerNO = 0
        # 胶带的半径
        self.radius = init_radius
        # 胶带的位置
        self.pos = []
        self.pos.append(init_pos[0])
        self.pos.append(init_pos[1])
        # 胶带的速度
        self.velocity = [0,0]
        # 胶带是否运动
        self.moving = False
    
    def setVelocity(self, givenVelo):
        """
        从玩家激励中获得速度
        """
        self.velocity[0] = givenVelo[0]
        self.velocity[1] = givenVelo[1]
    
    def simulation(self, boundary, playerList, obstacleList):
        """
        模拟小球的运动过程
        """
        # 判断小球是否到达了静止过程
        if abs(self.velocity[0]) <= 0.1 and abs(self.velocity[1]-0.0) <= 0.1:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.moving = False
            return
        # 小球的速度不为0
        else:
            self.moving = True

            # 计算摩擦力
            currFric = self.friction()
            # 更新速度
            self.velocity[0] += currFric[0]
            self.velocity[1] += currFric[1]
            # 更新位置
            self.pos[0] += self.velocity[0]
            self.pos[1] += self.velocity[1]

            # 检查与边框的碰撞
            boundary.checkCollision(self)
            
            # 检查胶带与障碍物之间的碰撞
            for obstacle in obstacleList:
                obstacle.checkCollision(self)

            # 检查胶带与胶带之间的碰撞
            for player in playerList:
                # 如果该胶带与另一个胶带不属于同一个玩家，才会进行碰撞检测
                if player.playerNO != self.player.playerNO:
                    self.checkCollision(player.myTape)
            
            # 检查玩家是否已经超出了边界
            if self.pos[0] < 0 or self.pos[0] > boundary.windowWidth or self.pos[1] < 0 or self.pos[1] > boundary.windowHeight: 
                self.velocity[0] = 0
                self.velocity[1] = 0
                self.moving = False
                self.player.isPlaying = False

            



    def friction(self):
        """
        滑动摩擦力
        """
        # 计算速度的大小
        speed = pow((pow(self.velocity[0],2)+pow(self.velocity[1],2)),0.5)
        
        # 如果速度非常小的话，可以认为滑动摩擦力为0
        if speed < 0.1:
            return 0.0, 0.0
        else:
            # 计算当前运动的方向
            sin_theta = self.velocity[1] / pow((pow(self.velocity[0],2)+pow(self.velocity[1],2)),0.5)
            cos_theta = self.velocity[0] / pow((pow(self.velocity[0],2)+pow(self.velocity[1],2)),0.5)
            coeff = 0.1
            return (-1.0)*coeff*cos_theta, (-1.0)*coeff*sin_theta

    def checkCollision(self, otherTape):
        """
        这个函数用来检查该胶带是否和其他胶带发生碰撞
        """
        # 获得另一个胶带的中心位置
        other_tape_pos = otherTape.pos
        # 计算另一个胶带的中心位置和本胶带的中心位置之间的距离
        distance = pow(pow(other_tape_pos[0]-self.pos[0],2) + pow(other_tape_pos[1]-self.pos[1],2), 0.5)

        # 判断两胶带的中心距离是否大于两半径之和
        if distance < (self.radius + otherTape.radius):
            # 如果小于，则说明发生了碰撞
            # 获得另一个球的速度
            other_tape_vel = otherTape.velocity
            # 计算球心连线与水平轴的夹角
            sin_theta = (other_tape_pos[1] - self.pos[1]) / distance
            cos_theta = (other_tape_pos[0] - self.pos[0]) / distance
            # 计算另一个球沿着球心连线方向的切向和法向速度
            vn1 = other_tape_vel[0] * cos_theta + other_tape_vel[1] * sin_theta
            vt1 = other_tape_vel[0] * (-1.0)*sin_theta + other_tape_vel[1] * cos_theta
            # 计算本球沿着球心连线方向的切向和法向速度
            vn2 = self.velocity[0] * cos_theta + self.velocity[1] * sin_theta
            vt2 = self.velocity[0] * (-1.0)*sin_theta + self.velocity[1] * cos_theta
            # 交换两球的法向速度
            tempVn = vn1
            vn1    = vn2
            vn2    = tempVn
            # 计算另一个球碰撞后的x、y方向的速度
            otherTape.velocity[0] = vn1 * cos_theta - vt1 * sin_theta
            otherTape.velocity[1] = vn1 * sin_theta + vt1 * cos_theta
            # 计算本球碰撞后的x、y方向的速度
            self.velocity[0] = vn2 * cos_theta - vt2 * sin_theta
            self.velocity[1] = vn2 * sin_theta + vt2 * cos_theta
            # 将另一胶带的中心手动的放置在胶带之外
            otherTape.pos[0] = self.pos[0] + (self.radius+otherTape.radius + 0.1) * cos_theta
            otherTape.pos[1] = self.pos[1] + (self.radius+otherTape.radius + 0.1) * sin_theta
