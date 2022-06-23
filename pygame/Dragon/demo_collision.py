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
        self.main_scene.scene.blit(self.image1, (self.x1, map_y))
        self.main_scene.scene.blit(self.image2, (self.x2, map_y))

# ��
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

# ������
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

# ��
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

# ����
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
    style = 0 # 0��վ����1������
    jump = 0 # 0: δ������1����ʼ������2����ʼ�½�
    jump_y_add = 0
    is_hit = 0 # �Ƿ������ϰ�

    def __init__(self, x, y, image, main_scene):
        self.x = x
        self.y = y
        self.image = image
        self.main_scene = main_scene

    def set_jump(self):
        if self.style == 0 and self.jump == 0:
            self.jump = 1

    def move(self):
        if self.jump == 1:
            self.y -= 10
            self.jump_y_add += 10
            if self.jump_y_add == 200:
                self.jump = 2

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

# ������
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

        # ������
        self.cloud_image = pygame.image.load("images/dragon/cloud.png")
        self.create_cloud()

        # ����������
        for n in range(7):
            self.item_images.append(pygame.image.load("images/dragon/item_" + str(n+1) + ".png"))

        # ������
        self.bird_images.append(pygame.image.load("images/dragon/bird_1.png"))
        self.bird_images.append(pygame.image.load("images/dragon/bird_2.png"))

        # ��������
        for n in range(4):
            self.dragon_images.append(pygame.image.load("images/dragon/dragon_" + str(n+1) + ".png"))

        d_x = 50
        d_y = self.size[1] - self.dragon_images[0].get_height()
        self.dragon = Dragon(d_x, d_y, self.dragon_images, self)

    #  ����������
    def create_cloud(self):
        self.clouds.append(Cloud(350, 30, self.cloud_image))
        self.clouds.append(Cloud(650, 100, self.cloud_image))

    # ����
    def draw_elements(self):
        self.scene.fill((255, 255, 255)) # ��䱳��ɫΪ��ɫ
        self.bg.draw()                   # ���Ʊ���

        # ������
        for c in self.clouds[:]:
            self.scene.blit(c.image, (c.x, c.y))

        # ����������
        for i in self.items[:]:
            self.scene.blit(i.image, (i.x, i.y))

        # ������
        for b in self.birds[:]:
            b.draw()

        # ���ƿ���
        self.dragon.draw()

    # ����Ԫ�����꼰����Ԫ��
    def action_elements(self):
        # ��ͼ
        self.bg.action()

        # ��
        for c in self.clouds[:]:
            c.move()

            if c.x < - self.cloud_image.get_width():
                self.clouds.remove(c)

        if len(self.clouds) == 0:
            self.create_cloud()

        # ������
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

        # ��
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

        # ����
        self.dragon.move()

    # �����¼�
    def handle_event(self):
        for event in pygame.event.get():
            # ����ɿ������¼�
            if event.type == pygame.KEYUP:
                if event.key == K_DOWN:
                    if self.dragon.style == 1:
                        self.dragon.style = 0
                        self.dragon.y -= 34

            # ��⵽�¼�Ϊ�˳�ʱ
            if event.type == pygame.QUIT:
                self.running = False

    # ��ײ���
    def detect_collision(self):
        pass # ��ʾû���κ��߼�

    # ������
    def key_pressed(self):
        # ��ȡ���°�����Ϣ
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_DOWN]:
            if self.dragon.jump == 0:
                if self.dragon.style == 0:
                    self.dragon.style = 1
                    self.dragon.y += 34

        if key_pressed[K_SPACE]:
            self.dragon.set_jump()

    # ����֡��
    def set_fps(self):
        # ˢ����ʾ
        pygame.display.update()
        # ����֡��Ϊ60fps
        self.timer.tick(60)

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