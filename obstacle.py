class Obstacle:
    """
    这个类实现障碍物
    """
    def __init__(self, init_number, init_x, init_y, init_radius):
        """
        构造函数
        """
        # 编号
        self.number = init_number
        # 生命值
        self.lifeTime = 3
        # 障碍物中心坐标位置
        self.pos = []
        self.pos.append(init_x)
        self.pos.append(init_y)
        # 障碍物的半径
        self.radius = init_radius
    
    def checkCollision(self, checkedTape):
        """
        用来检测碰撞的函数
        """
        # 只有当生命值大于0的时候，才进行检查，否则说明这个障碍物已经消失
        if self.lifeTime > 0:
            # 获得待查胶带的位置
            tape_pos = checkedTape.pos
            # 计算障碍物中心到待查胶带之间的距离
            dx = tape_pos[0] - self.pos[0]
            dy = tape_pos[1] - self.pos[1]
            distance = pow(pow(dx,2) + pow(dy,2) , 0.5)
            # 如果距离小于两者半径之和，则说明发生了碰撞
            if distance < (self.radius + checkedTape.radius):
                # 障碍物的生命值-1
                self.lifeTime -= 1
                # 计算两圆心连线与水平方向的夹角
                sin_theta = dy / distance
                cos_theta = dx / distance
                # 获得胶带的
                tape_vel = checkedTape.velocity
                # 计算胶带速度沿着球心连线的切向和法向的速度
                vn = tape_vel[0] * cos_theta + tape_vel[1] * sin_theta
                vt = (-1.0) * tape_vel[0] * sin_theta + tape_vel[1] * cos_theta
                # 法向速度反相
                vn = (-0.9) * vn
                # 计算胶带碰撞后的水平和竖直速度
                checkedTape.velocity[0] = vn * cos_theta - vt * sin_theta
                checkedTape.velocity[1] = vn * sin_theta + vt * cos_theta
                # 将胶带的中心手动的放置在障碍物之外
                checkedTape.pos[0] = self.pos[0] + (self.radius+checkedTape.radius + 0.1) * cos_theta
                checkedTape.pos[1] = self.pos[1] + (self.radius+checkedTape.radius + 0.1) * sin_theta


    

