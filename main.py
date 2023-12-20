import os
import time
import sys
import pygame
from pygame.locals import *
from sys import exit
#游戏界面



screen_width=1000
screen_height=500
back_color=pygame.Color(0,0,0)
pygame.display.init()
window=pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption("The Code Odyssey") #设置游戏窗口名称
icon=pygame.image.load("icon\head.png")  #设置游戏窗口图标
pygame.display.set_icon(icon)
pygame.mixer.init() #加载和播放声音
my_sound=pygame.mixer.Sound('music\music.mp3')
my_sound.play(-1) #无限循环播放
my_sound.set_volume(0.2)
while True:
    window.fill(back_color)
    pygame.display.flip()
    evenList=pygame.event.get()
    for event in evenList:
        if event.type==pygame.QUIT:
            exit()


# 人物
person1=pygame.image.load("icon\person1.png")
person1=pygame.transform.scale(person1, (20, 40))
person1= pygame.transform.flip(person1, True, False)#在水平方向上翻转，数竖直方向不翻转
person1_sword=pygame.image.load("icon\Sword.png")
person1_sword=pygame.transform.scale(person1_sword, (100, 50))
person1_sword = pygame.transform.flip(person1_sword, True, False)
person1_face=1 #初始化人物是朝右边走的
class CharacterPosition:
    def __init__(self):
        self.lupx = 30
        self.lupy = 30

    #描述人物占据空间 （20,40）的矩形
    def renew(self):
        self.rupx = self.lupx + 20    # 右上角 x 坐标
        self.rupy = self.lupy         # 右上角 y 坐标
        self.ldownx = self.lupx         # 左下角 x 坐标
        self.ldowny = self.lupy + 40    # 左下角 y 坐标
        self.rdownx = self.rupx         # 右下角 x 坐标
        self.rdowny = self.ldowny         # 右下角 y 坐标

# 创建 CharacterPosition 类的实例对象
person1_pos = CharacterPosition()

# 调用 renew 方法更新人物位置信息
person1_pos.renew()

# sword
class SwordPosition:
    def __init__(self):
        self.lupx=person1_pos.rupx-10
        self.face=1
        self.lupy=person1.pos.rupy
    def renew(self):
        self.face=person1_face
        if (self.face==1):
            self.lupx=person1.rupx-30
            self.lupx=person1_pos.rupy
            self.rupx=self.lupx+120
            self.rupy=self.lupy
            self.ldownx=self.lupx
            self.ldpwny=self.lupy+60


