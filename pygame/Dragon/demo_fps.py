# coding=gbk

import pygame
from pygame.locals import *
import random
import time

# ��ͼ
class GameBackground:
    image1 = None
    image2 = None
    main_scene = None
    speed = 8 # �����ٶ�
    x1 = None
    x2 = None

    # ��ʼ����ͼ
    def __init__(self, scene):
        # ������ͬ��ͼƬ��Դ,������ʵ�ֵ�ͼ����
        self.image1 = pygame.image.load("images/dragon/map.png")
        self.image2 = self.image1
        # ���泡������
        self.main_scene = scene
        # �����ƶ���ͼ
        self.x1 = 0
        self.x2 = self.main_scene.size[0]

    # �����ͼͼƬ��������
    def action(self):
        self.x1 = self.x1 - self.speed
        self.x2 = self.x2 - self.speed
        if self.x1 <= -self.main_scene.size[0]:
            self.x1 = 0
        if self.x2 <= 0:
            self.x2 = self.main_scene.size[0]

    # ���Ƶ�ͼ������ͼƬ
    def draw(self):
        map_y = self.main_scene.size[1] - self.image1.get_height()
        # print(map_y)
        self.main_scene.scene.blit(self.image1, (self.x1, map_y))
        self.main_scene.scene.blit(self.image2, (self.x2, map_y))

# ������
class MainScene:
    running = True
    size = None
    scene = None
    bg = None

    # ��ʼ��������
    def __init__(self):
        # ��ʼ�� pygame��ʹ���Զ�����������õ�
        pygame.init()
        # �����ߴ�
        self.size = (800, 350)
        # ��������
        self.scene = pygame.display.set_mode([self.size[0], self.size[1]])
        # ���ñ���
        pygame.display.set_caption("�����ܿ�")
        # ����clock�������֡��
        self.timer = pygame.time.Clock()

        # ������ͼ����
        self.bg = GameBackground(self)

    # ����
    def draw_elements(self):
        self.scene.fill((255, 255, 255)) # ��䱳��ɫΪ��ɫ
        self.bg.draw()                   # ���Ʊ���

    # ����Ԫ�����꼰����Ԫ��
    def action_elements(self):
        # ��ͼ
        self.bg.action()

    # �����¼�
    def handle_event(self):
        for event in pygame.event.get():
            # ��⵽�¼�Ϊ�˳�ʱ
            if event.type == pygame.QUIT:
                self.running = False

    # ��ײ���
    def detect_collision(self):
        pass

    # ������
    def key_pressed(self):
        pass

    # ����֡��
    def set_fps(self):
        # ˢ����ʾ
        pygame.display.update()
        # ����֡��Ϊ60fps
        self.timer.tick(1)

    # ��ѭ��,��Ҫ��������¼�
    def run_scene(self):

        while self.running:
            # ����Ԫ�����꼰����Ԫ��
            self.action_elements()
            # ����Ԫ��ͼƬ
            self.draw_elements()
            # �����¼�
            self.handle_event()
            # ��ײ���
            self.detect_collision()
            # ��������
            self.key_pressed()
            # ���»�������fps
            self.set_fps()

# ����������
mainScene = MainScene()

# ��ʼ��Ϸ
mainScene.run_scene()