import pygame
import copy


# 地图
class GameBackground:
    image1 = None
    image2 = None
    main_scene = None
    y1 = None
    y2 = None

    # 初始化地图
    def __init__(self, scene):
        # 加载相同张图片资源,做交替实现地图滚动
        self.image1 = pygame.image.load("images/plane/map.jpg")
        self.image2 = copy.copy(self.image1)
        # 保存场景对象
        self.main_scene = scene
        # 辅助移动地图
        self.y1 = 0
        self.y2 = -self.main_scene.size[1]

    # 计算地图图片绘制坐标
    def action(self):
        self.y1 = self.y1 + 1
        self.y2 = self.y2 + 1
        if self.y1 >= self.main_scene.size[1]:
            self.y1 = 0
        if self.y2 >= 0:
            self.y2 = -self.main_scene.size[1]

    # 绘制地图的两张图片
    def draw(self):
        self.main_scene.scene.blit(self.image1, (0, self.y1))
        self.main_scene.scene.blit(self.image2, (0, self.y2))


# 主场景
class MainScene:
    size = None
    scene = None
    bg = None
    plane = None
    timer = None
    running = True

    # 初始化主场景
    def __init__(self):
        # 场景尺寸
        self.size = (458, 752)
        # 场景对象
        self.scene = pygame.display.set_mode([self.size[0], self.size[1]])
        # 设置标题
        pygame.display.set_caption("雷霆战机")
        # 创建clock对象控制帧数
        self.timer = pygame.time.Clock()
        # 创建地图对象
        self.bg = GameBackground(self)


    # 绘制
    def draw_elements(self):
        self.bg.draw()

    # 计算元素坐标及生成元素
    def action_elements(self):
        self.bg.action()

    # 处理事件
    def handle_event(self):
        for event in pygame.event.get():
            # 检测到事件为退出时
            if event.type == pygame.QUIT:
                self.running = False

    # 碰撞检测
    def detect_collision(self):
        pass

    # 处理帧数
    def set_fps(self):
        # 刷新显示
        pygame.display.update()
        # 设置帧率为60fps
        self.timer.tick(60)

    # 主循环,主要处理各种事件
    def run_scene(self):

        while self.running:
            # 计算元素坐标及生成元素
            self.action_elements()
            # 绘制元素图片
            self.draw_elements()
            # 处理事件
            self.handle_event()
            # 碰撞检测
            self.detect_collision()
            # 更新画布设置fps
            self.set_fps()

# 创建主场景
mainScene = MainScene()
# 开始游戏
mainScene.run_scene()