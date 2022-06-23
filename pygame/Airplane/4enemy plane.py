import pygame
from pygame.locals import *
import random
import time
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

# 子弹
class Bullet:
    speed = 10
    x = None
    y = None
    width = None
    hieght = None

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def move(self):
        self.y -= self.speed

# 敌机子弹
class EnemyBullet:
    speed = None
    x = None
    y = None
    width = None
    hieght = None

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.speed = random.randint(7, 15)

    def move(self):
        self.y += self.speed

# 飞机
class Plane:
    x = None
    y = None
    image = []
    main_scene = None
    speed = 8
    style = 0
    width = None
    height = None
    shoot_frequency = 0
    bullet_image = None
    bullets = []

    def __init__(self, scene):
        # 加载飞机外观图片
        self.image.append(pygame.image.load("images/plane/plane.png"))
        self.image.append(pygame.image.load("images/plane/plane_left.png"))
        self.image.append(pygame.image.load("images/plane/plane_right.png"))

        # 加载飞机子弹图片
        self.bullet_image = pygame.image.load("images/plane/bullet.png")

        self.main_scene = scene
        self.x = self.main_scene.size[0] / 2 - self.image[self.style].get_width() / 2
        self.y = 600
        self.width = self.image[self.style].get_width()
        self.height = self.image[self.style].get_height()

    # 发射子弹
    def shoot(self):
        if self.shoot_frequency % 15 == 0:
            bullet_x = self.x + self.image[self.style].get_width() // 2 - self.bullet_image.get_width() // 2
            bullet_y = self.y - self.bullet_image.get_height() + 10
            b_w = self.bullet_image.get_width()
            b_h = self.bullet_image.get_height()
            self.bullets.append(Bullet(bullet_x, bullet_y, b_w, b_h))
        self.shoot_frequency += 1
        if self.shoot_frequency >= 15:
            self.shoot_frequency = 0

    # 绘制子弹
    def drawBullets(self):
        for b in self.bullets[:]:
            b.move()
            if b.y < 0:
                self.bullets.remove(b)
            self.main_scene.scene.blit(self.bullet_image, (b.x, b.y))

    # 向上
    def moveUp(self):
        if self.y > 0:
            self.y -= self.speed

    # 向下
    def moveDown(self):
        if self.y + self.image[self.style].get_height() < self.main_scene.size[1]:
            self.y += self.speed

    # 向左
    def moveLeft(self):
        if self.x > 0:
            self.x -= self.speed

    # 向右
    def moveRight(self):
        if self.x + self.image[self.style].get_width() < self.main_scene.size[0]:
            self.x += self.speed

    # 绘制飞机
    def draw(self):
        self.main_scene.scene.blit(self.image[self.style], (self.x, self.y))

# 敌机
class Enemy:
    image = None
    x = None
    y = None
    speed = 5
    width = None
    hieght = None

    def __init__(self, image, init_pos):
        self.image = image
        self.x = init_pos[0]
        self.y = init_pos[1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self):
        self.y += self.speed

# 主场景
class MainScene:
    size = None
    scene = None
    bg = None
    plane = None
    timer = None
    running = True

    enemy_images = []
    enemies = []
    enemy_bullet = None
    enemy_bullets = []
    enemy_frequency = 0

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
        # 创建飞机对象
        self.plane = Plane(self)
        # 加载敌机外形图片
        for n in range(4):
            self.enemy_images.append(pygame.image.load("images/plane/enemy/e_" + str(n + 1) + ".png"))
        # 加载敌机子弹图片
        self.enemy_bullet = pygame.image.load("images/plane/enemy_bullet.png")
        # 缩小敌机子弹图片为原来的一半
        new_size = (self.enemy_bullet.get_width() // 2, self.enemy_bullet.get_height() // 2)
        self.enemy_bullet = pygame.transform.scale(self.enemy_bullet, new_size)

    # 绘制
    def draw_elements(self):
        self.bg.draw()           # 绘制背景
        self.plane.draw()        # 绘制飞机
        self.plane.drawBullets() # 绘制飞机子弹

        # 绘制敌机移动
        for e in self.enemies:
            self.scene.blit(e.image, (e.x, e.y))

        # 绘制敌机子弹移动
        for eb in self.enemy_bullets:
            self.scene.blit(self.enemy_bullet, (eb.x, eb.y))

    # 计算元素坐标及生成元素
    def action_elements(self):
        self.bg.action()

        # 生成敌机，需要控制生成频率
        if self.enemy_frequency % 50 == 0:
            enemy_image = self.enemy_images[random.randint(0, len(self.enemy_images) - 1)]
            # 缩小敌机图片为原来的一半
            new_size = (enemy_image.get_width() // 2, enemy_image.get_height() // 2)
            enemy_image = pygame.transform.scale(enemy_image, new_size)
            # 设置敌机随机外观
            enemy_pos = [random.randint(0, self.size[0] - enemy_image.get_width()), 0]
            enemy = Enemy(enemy_image, enemy_pos)
            self.enemies.append(enemy)

            # 生成敌机子弹，需要控制生成频率
            ret = random.randint(1, 100)
            if ret >= 1 and ret <= 65: # 65%概率发射子弹
                w = self.enemy_bullet.get_width()
                h = self.enemy_bullet.get_height()
                b_x = enemy.x + enemy.width // 2 - w // 2
                b_y = enemy.y + enemy.height
                self.enemy_bullets.append(EnemyBullet(b_x, b_y, w, h))
        self.enemy_frequency += 1
        if self.enemy_frequency >= 100:
            self.enemy_frequency = 0

        # 计算敌机坐标
        for e in self.enemies[:]:
            e.move()
            if e.y > self.size[1]:
                self.enemies.remove(e)

        # 计算敌机子弹坐标
        for eb in self.enemy_bullets[:]:
            eb.move()
            if eb.y > self.size[1]:
                self.enemy_bullets.remove(eb)

    # 处理事件
    def handle_event(self):
        for event in pygame.event.get():
            # 检测松开键盘事件
            if event.type == pygame.KEYUP:
                # 检测松开的按键是否是方向键左
                if event.key == K_LEFT or event.key == K_RIGHT:
                    self.plane.style = 0

            # 检测到事件为退出时
            if event.type == pygame.QUIT:
                self.running = False

    # 碰撞检测
    def detect_collision(self):
        pass

    # 处理按键
    def key_pressed(self):
        # 获取按下按键信息
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_UP]:
            self.plane.moveUp()
        if key_pressed[K_DOWN]:
            self.plane.moveDown()
        if key_pressed[K_LEFT]:
            self.plane.style = 1
            self.plane.moveLeft()
        if key_pressed[K_RIGHT]:
            self.plane.style = 2
            self.plane.moveRight()
        if key_pressed[K_SPACE]:
            self.plane.shoot()

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