import pygame
from pygame.locals import *
import random
import time

# 地图
class GameBackground:
    image1 = None
    image2 = None
    main_scene = None
    speed = 8 # 滚动速度
    x1 = None
    x2 = None

    # 初始化地图
    def __init__(self, scene):
        # 加载相同张图片资源,做交替实现地图滚动
        self.image1 = pygame.image.load("images/dragon/map.png")
        self.image2 = self.image1
        # 保存场景对象
        self.main_scene = scene
        # 辅助移动地图
        self.x1 = 0
        self.x2 = self.main_scene.size[0]

    # 计算地图图片绘制坐标
    def action(self):
        self.x1 = self.x1 - self.speed
        self.x2 = self.x2 - self.speed
        if self.x1 <= -self.main_scene.size[0]:
            self.x1 = 0
        if self.x2 <= 0:
            self.x2 = self.main_scene.size[0]

    # 绘制地图的两张图片
    def draw(self):
        map_y = self.main_scene.size[1] - self.image1.get_height()
        self.main_scene.scene.blit(self.image1, (self.x1, map_y))
        self.main_scene.scene.blit(self.image2, (self.x2, map_y))

# 云
class Cloud:
    speed = 1
    image = None
    x = None
    y = None

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def move(self):
        self.x -= self.speed

# 仙人掌
class Cactus:
    speed = 8
    image = None
    x = None
    y = None
    width = None
    height = None

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

    def move(self):
        self.x -= self.speed

# 鸟
class Bird:
    speed = 10
    image = None
    x = None
    y = None
    width = None
    height = None
    index = 0
    main_scene = None
    ret = 1

    def __init__(self, x, y, image, main_scene):
        self.x = x
        self.y = y
        self.image = image
        self.main_scene = main_scene
        image = self.image[self.index]
        self.width = image.get_width()
        self.height = image.get_height()

    def move(self):
        self.x -= self.speed

    def draw(self):
        if self.ret <= 8:
            self.index = 0
        else:
            self.index = 1

        if self.ret == 16:
            self.ret = 0

        image = self.image[self.index]
        self.main_scene.scene.blit(image, (self.x, self.y))
        self.ret += 1

# 主场景
class MainScene:
    running = True
    size = None
    scene = None
    bg = None

    clouds = []
    cloud_image = None

    items = []
    item_images = []
    item_ret= 1
    item_ret_num = 100

    bird_images = []
    birds = []
    bird_ret= 1
    bird_ret_num = 150

    # 初始化主场景
    def __init__(self):
        # 初始化 pygame，使用自定义字体必须用到
        pygame.init()
        # 场景尺寸
        self.size = (800, 350)
        # 场景对象
        self.scene = pygame.display.set_mode([self.size[0], self.size[1]])
        # 设置标题
        pygame.display.set_caption("恐龙跑酷")
        # 创建clock对象控制帧数
        self.timer = pygame.time.Clock()

        # 创建地图对象
        self.bg = GameBackground(self)

        # 创建云
        self.cloud_image = pygame.image.load("images/dragon/cloud.png")
        self.create_cloud()

        # 创建仙人掌
        for n in range(7):
            self.item_images.append(pygame.image.load("images/dragon/item_" + str(n+1) + ".png"))

        # 创建鸟
        self.bird_images.append(pygame.image.load("images/dragon/bird_1.png"))
        self.bird_images.append(pygame.image.load("images/dragon/bird_2.png"))

    #  生成两朵云
    def create_cloud(self):
        self.clouds.append(Cloud(350, 30, self.cloud_image))
        self.clouds.append(Cloud(650, 100, self.cloud_image))

    # 绘制
    def draw_elements(self):
        self.scene.fill((255, 255, 255)) # 填充背景色为白色
        self.bg.draw()                   # 绘制背景

        # 绘制云
        for c in self.clouds[:]:
            self.scene.blit(c.image, (c.x, c.y))

        # 绘制仙人掌
        for i in self.items[:]:
            self.scene.blit(i.image, (i.x, i.y))

        # 绘制鸟
        for b in self.birds[:]:
            b.draw()

    # 计算元素坐标及生成元素
    def action_elements(self):
        # 地图
        self.bg.action()

        # 云
        for c in self.clouds[:]:
            c.move()

            if c.x < - self.cloud_image.get_width():
                self.clouds.remove(c)

        if len(self.clouds) == 0:
            self.create_cloud()

        # 仙人掌
        if self.item_ret % self.item_ret_num == 0:
            image = self.item_images[random.randint(0, len(self.item_images) - 1)]
            x = self.size[0]
            y = self.size[1] - image.get_height()
            self.items.append(Cactus(x, y, image))
        self.item_ret += 1
        if self.item_ret == self.item_ret_num:
            self.item_ret = 0
            self.item_ret_num = random.randint(60, 110)

        for i in self.items[:]:
            i.move()

            if i.x < -i.width:
                self.items.remove(i)

        # 鸟
        if self.bird_ret % self.bird_ret_num == 0:
            x = self.size[0]
            y = 210
            self.birds.append(Bird(x, y, self.bird_images, self))
        self.bird_ret += 1
        if self.bird_ret == self.bird_ret_num:
            self.bird_ret = 0
            self.bird_ret_num = random.randint(150, 300)

        for b in self.birds[:]:
            b.move()

            if b.x < -b.width:
                self.birds.remove(b)

    # 处理事件
    def handle_event(self):
        for event in pygame.event.get():
            # 检测到事件为退出时
            if event.type == pygame.QUIT:
                self.running = False

    # 碰撞检测
    def detect_collision(self):
        pass # 表示没有任何逻辑

    # 处理按键
    def key_pressed(self):
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
            # 按键处理
            self.key_pressed()
            # 更新画布设置fps
            self.set_fps()

# 创建主场景
mainScene = MainScene()

# 开始游戏
mainScene.run_scene()