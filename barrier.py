
class Barrier:
    """
    这个类实现边框障碍
    """
    def __init__(self, init_barrier_width, init_width, init_height):
        # 生命值
        self.lifeTime = 3
        # 游戏界面的大小
        self.windowWidth = init_width
        self.windowHeight = init_height
        # 边框的大小
        self.width = init_barrier_width

    def checkCollision(self, checkedTape):
        """
        检查是否碰到边界的函数，如果左右碰到，则返回1，如果上下碰到，则返回2，如果没碰到，则返回0
        """
        if self.lifeTime != 0:
            # 检察左边界
            if checkedTape.pos[0] <= self.width + checkedTape.radius:
                # 生命值-1
                self.lifeTime -= 1
                # 恢复胶带的中心坐标
                checkedTape.pos[0] = checkedTape.radius + self.width + 0.1
                # 胶带的水平速度取反
                checkedTape.velocity[0] *= (-1.0)
            # 检察右边界
            elif checkedTape.pos[0] >= self.windowWidth - self.width - checkedTape.radius:
                # 生命值-1
                self.lifeTime -= 1
                # 恢复胶带的中心坐标
                checkedTape.pos[0] = self.windowWidth - checkedTape.radius - self.width - 0.1
                # 胶带的水平速度取反
                checkedTape.velocity[0] *= (-1.0)
            # 检察上边界
            elif checkedTape.pos[1] <= self.width + checkedTape.radius:
                # 生命值-1
                self.lifeTime -= 1
                # 恢复胶带的中心坐标
                checkedTape.pos[1] = checkedTape.radius + self.width + 0.1
                # 胶带的竖直速度取反
                checkedTape.velocity[1] *= (-1.0)
            # 检察下边界
            elif checkedTape.pos[1] >= self.windowHeight - self.width - checkedTape.radius:
                # 生命值-1
                self.lifeTime -= 1
                # 恢复胶带的中心坐标
                checkedTape.pos[1] = self.windowHeight - checkedTape.radius - self.width - 0.1
                # 胶带的竖直速度取反
                checkedTape.velocity[1] *= (-1.0)
            
            else:
                return 0
        else:
            return 0

