import pygame
import sys




class Game:

    def __init__(self):
        # 初始化 Pygame
        pygame.init()

        # 游戏设置
        self.WIDTH, self.HEIGHT = 1200, 700
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("aad")

        # 加载游戏背景图像
        self.background_image = pygame.image.load("bgp1.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        # 加载主角奔跑动画帧
        self.run_frames = [
            pygame.image.load("run1.png"),
            pygame.image.load("run2.png"),
            pygame.image.load("run3.png")
        ]
        self.current_frame = 0
        self.player_image = self.run_frames[self.current_frame]
        self.player_image = pygame.transform.scale(self.player_image, (60, 60))

        # 加载血量图像
        self.heart_image = pygame.image.load("heart.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

        # 环境重力
        self.gravity = 0.4


        # 初始化玩家速度和跳跃高度
        self.player_speed = 4
        self.jump_height = 50

        # 玩家血量
        self.player_health = 5

        # 定义主角的位置和朝向
        self.player_x = 50
        self.player_y = self.HEIGHT - 240
        self.is_facing_right = True

        # 跳跃状态
        self.is_jumping = False
        self.jump_velocity = 0

        # 奔跑状态
        self.is_running = False



        # 主角的地面高度
        self.player_ground = self.HEIGHT - 180

        # 血量指示器位置和间距
        self.heart_x = 20
        self.heart_y = 20
        self.heart_spacing = 40

        # 游戏循环
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_player(self):
        # 角色移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_x -= self.player_speed
            self.is_running = True
            self.is_facing_right = False  # 左移时朝向左
        elif keys[pygame.K_d]:
            self.player_x += self.player_speed
            self.is_running = True
            self.is_facing_right = True  # 右移时朝向右
        else:
            self.is_running = False

        # 切换奔跑动画帧
        if self.is_running:
            self.current_frame = (self.current_frame + 1) % len(self.run_frames)
            self.player_image = self.run_frames[self.current_frame]
            self.player_image = pygame.transform.scale(self.player_image, (60, 60))

        # 跳跃
        if not self.is_jumping:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and self.player_y == self.player_ground:
                self.is_jumping = True
                self.jump_velocity = 6

        if self.player_y<self.player_ground or self.is_jumping:
            self.player_y -= self.jump_velocity
            self.jump_velocity -= self.gravity
        else:
            self.is_jumping = False
            self.jump_velocity = 0







    def render(self):
        # 渲染背景
        self.SCREEN.blit(self.background_image, (0, 0))

        # 根据朝向渲染角色
        if self.is_facing_right:
            self.SCREEN.blit(self.player_image, (self.player_x, self.player_y))
        else:
            flipped_player_image = pygame.transform.flip(self.player_image, True, False)
            self.SCREEN.blit(flipped_player_image, (self.player_x, self.player_y))

        # 渲染血量指示器
        for i in range(self.player_health):
            self.SCREEN.blit(self.heart_image, (self.heart_x + i * self.heart_spacing, self.heart_y))

        pygame.display.update()

    def run_game(self):
        # 游戏循环
        while self.running:
            self.handle_events()
            self.update_player()
            self.render()

        # 游戏结束
        pygame.quit()
        sys.exit()

# 创建游戏对象并运行游戏
game = Game()
game.run_game()
