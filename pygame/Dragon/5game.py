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
        self.image1 = pygame.image.load("D://Desktop//pygame//Dragon//images//dragon//map.png")
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

# 恐龙
class Dragon:
    speed = 10
    image = None
    x = None
    y = None
    width = None
    height = None
    index = 0
    main_scene = None
    ret = 1
    style = 0 # 0：站立，1：蹲下
    jump = 0 # 0: 未起跳，1：开始上升，2：开始下降
    jump_y_add = 0
    is_hit = 0

    def __init__(self, x, y, image, main_scene):
        self.x = x
        self.y = y
        self.image = image
        self.main_scene = main_scene

    def set_jump(self):
        if self.style == 0 and self.jump == 0:
            self.jump = 1
            # 播放声音
            self.main_scene.jump_sound.play()

    def move(self):
        # 匀速上升
        if self.jump == 1:
            self.y -= 10
            self.jump_y_add += 10
            if self.jump_y_add == 200:
                self.jump = 2

        # 匀速下降
        if self.jump == 2:
            self.y += 10
            self.jump_y_add -= 10
            if self.jump_y_add == 0:
                self.jump = 0

    def draw(self):
        if self.ret <= 5:
            if self.style == 0:
                self.index = 0
            else:
                self.index = 2
        else:
            if self.style == 0:
                self.index = 1
            else:
                self.index = 3

        if self.ret == 10:
            self.ret = 0

        image = self.image[self.index]
        self.width = image.get_width()
        self.height = image.get_height()
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

    dragon = None
    dragon_images = []

    gameover_image = None
    restart_image = None
    restart_x = None
    restart_y = None
    score = 0.0

    jump_sound = None
    gameover_sound = None

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
        self.cloud_image = pygame.image.load("D://Desktop//pygame//Dragon//images//dragon//cloud.png")
        self.create_cloud()

        # 创建仙人掌
        for n in range(7):
            self.item_images.append(pygame.image.load("D://Desktop//pygame//Dragon//images//dragon//item_" + str(n+1) + ".png"))

        # 创建鸟
        self.bird_images.append(pygame.image.load("D://Desktop//pygame//Dragon//images//dragon//bird_1.png"))
        self.bird_images.append(pygame.image.load("D://Desktop//pygame//Dragon//images//dragon//bird_2.png"))

        # 创建恐龙
        for n in range(4):
            self.dragon_images.append(pygame.image.load("D://Desktop//pygame//Dragon//images//dragon//dragon_" + str(n+1) + ".png"))

        d_x = 50
        d_y = self.size[1] - self.dragon_images[0].get_height()
        self.dragon = Dragon(d_x, d_y, self.dragon_images, self)

        # gameover
        self.gameover_image = pygame.image.load("D://Desktop//pygame//Dragon//images//dragon//gameover.png")
        self.restart_image = pygame.image.load("D://Desktop//pygame//Dragon//images//dragon//restart.png")

        # 音效加载
        self.jump_sound = pygame.mixer.Sound("D://Desktop//pygame//Dragon//sounds//dragon//jump.wav")
        self.gameover_sound = pygame.mixer.Sound("D://Desktop//pygame//Dragon//sounds//dragon//gameover.wav")

    #  生成两朵云
    def create_cloud(self):
        self.clouds.append(Cloud(350, 30, self.cloud_image))
        self.clouds.append(Cloud(650, 100, self.cloud_image))

    # 绘制
    def draw_elements(self):
        if self.dragon.is_hit == 1:
            g_x = self.size[0] // 2 - self.gameover_image.get_width() // 2
            self.scene.blit(self.gameover_image, (g_x, 120))

            self.restart_x = self.size[0] // 2 - self.restart_image.get_width() // 2
            self.restart_y = 170
            self.scene.blit(self.restart_image, (self.restart_x, self.restart_y))
            return

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

        # 绘制恐龙
        self.dragon.draw()

        # 绘制跑动距离
        self.score += 0.1
        font = pygame.font.Font(None, 30)
        text = font.render(str(int(self.score)) + "m", True, (83, 83, 83))
        text_rect = text.get_rect()
        text_rect.right = self.size[0] - 10
        text_rect.top = 10
        self.scene.blit(text, text_rect)

    # 计算元素坐标及生成元素
    def action_elements(self):
        if self.dragon.is_hit == 1:
            return

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
        if int(self.score) > 100:
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

        # 恐龙
        self.dragon.move()

    # 处理事件
    def handle_event(self):
        for event in pygame.event.get():
            # 检测松开键盘事件
            if event.type == pygame.KEYUP:
                if event.key == K_DOWN:
                    if self.dragon.style == 1:
                        self.dragon.style = 0
                        self.dragon.y -= 34

            # 检测按下鼠标事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.dragon.is_hit == 1:
                        pos = event.pos # 点击位置坐标

                        # 判断点击范围是否是重启图片上
                        x1 = self.restart_x
                        x2 = self.restart_x + self.restart_image.get_width()

                        y1 = self.restart_y
                        y2 = self.restart_y + self.restart_image.get_height()

                        if pos[0] >= x1 and pos[0] <= x2 and pos[1] >= y1 and pos[1] <= y2:
                            self.dragon.is_hit = 0
                            self.score = 0
                            self.items.clear()
                            self.birds.clear()


            # 检测到事件为退出时
            if event.type == pygame.QUIT:
                self.running = False

    # 碰撞检测
    def detect_collision(self):
        if self.dragon.is_hit == 0:
            # 是否碰到仙人掌
            for i in self.items[:]:
                if self.collision(self.dragon, i) or self.collision(i, self.dragon):
                    self.dragon.is_hit = 1
                    break

            # 是否碰到鸟
            for b in self.birds[:]:
                if self.collision(self.dragon, b) or self.collision(b, self.dragon):
                    self.dragon.is_hit = 1
                    break

            if self.dragon.is_hit == 1:
                self.gameover_sound.play()

    # 验证是否碰撞
    def collision(self, a, b):
        offset = 30 # 增加20误差，降低难度
        temp1 = (b.x + offset <= a.x + a.width <= b.x + offset + b.width)
        temp2 = (b.y + offset <= a.y + a.height <= b.y + offset + b.height)
        return temp1 and temp2

    # 处理按键
    def key_pressed(self):
        # 获取按下按键信息
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_DOWN]:
            if self.dragon.jump == 0:
                if self.dragon.style == 0:
                    self.dragon.style = 1
                    self.dragon.y += 34

        if key_pressed[K_SPACE]:
            self.dragon.set_jump()

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