# coding=gbk

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
        # print(map_y)
        self.main_scene.scene.blit(self.image1, (self.x1, map_y))
        self.main_scene.scene.blit(self.image2, (self.x2, map_y))

# 主场景
class MainScene:
    running = True
    size = None
    scene = None
    bg = None

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

    # 绘制
    def draw_elements(self):
        self.scene.fill((255, 255, 255)) # 填充背景色为白色
        self.bg.draw()                   # 绘制背景

    # 计算元素坐标及生成元素
    def action_elements(self):
        # 地图
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

    # 处理按键
    def key_pressed(self):
        pass

    # 处理帧数
    def set_fps(self):
        # 刷新显示
        pygame.display.update()
        # 设置帧率为60fps
        self.timer.tick(1)

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