import pygame
import sys

# 初始化 Pygame
pygame.init()

# 游戏设置
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("aad")

# 加载游戏背景图像
background_image = pygame.image.load("bgp1.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# 加载主角奔跑动画帧
run_frames = [
    pygame.image.load("run1.png"),
    pygame.image.load("run2.png"),
    pygame.image.load("run3.png")
]
current_frame = 0
player_image = run_frames[current_frame]
player_image = pygame.transform.scale(player_image, (60, 60))


# 加载红色爱心图像
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))

# 设置速度和跳跃高度为 1
player_speed = 0.25
jump_height = 50
gravity_up = 0.01
gravity_down = 0.4

# 定义主角的位置和朝向
player_x = 50
player_y = HEIGHT - 240
is_facing_right = True

# 跳跃状态
is_jumping = False
jump_velocity = 0

# 奔跑状态
is_running = False

# 玩家血量
player_health = 5

# 主角和怪物的地面高度
player_ground = HEIGHT - 180


# 血量指示器位置和间距
heart_x = 20
heart_y = 20
heart_spacing = 40

# 菜单设置
menu_font = pygame.font.Font(None, 36)
menu_color = (255, 255, 255)
menu_options = ["Start", "Exit"]
current_option = 0

# 菜单循环
in_menu = True
while in_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = False
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                current_option = (current_option - 1) % len(menu_options)
            elif event.key == pygame.K_s:
                current_option = (current_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if current_option == 0:  # 开始游戏
                    in_menu = False
                elif current_option == 1:  # 退出游戏
                    in_menu = False
                    running = False

    # 渲染菜单
    SCREEN.blit(background_image, (0, 0))
    for i, option in enumerate(menu_options):
        text = menu_font.render(option, True, menu_color)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
        SCREEN.blit(text, text_rect)

    pygame.display.update()
# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 角色移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
        is_running = True
        is_facing_right = False  # 左移时朝向左
    elif keys[pygame.K_d]:
        player_x += player_speed
        is_running = True
        is_facing_right = True  # 右移时朝向右
    else:
        is_running = False

    # 切换奔跑动画帧
    if is_running:
        current_frame = (current_frame + 1) % len(run_frames)
        player_image = run_frames[current_frame]
        player_image = pygame.transform.scale(player_image, (60, 60))

    # 跳跃
    if not is_jumping:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_y == player_ground:
            is_jumping = True
            jump_velocity = 1.5
    else:
        if player_y < player_ground or jump_velocity == 1.5:
            player_y -= jump_velocity
            jump_velocity -= gravity_up
        else:
            is_jumping = False
            jump_velocity = 0

    # 应用下降重力效果
    if player_y < player_ground and not is_jumping:
        player_y += gravity_down


    # 限制主角在窗口范围内
    player_x = max(0, min(player_x, WIDTH - 30))
    player_y = max(0, min(player_y, player_ground))



    # 渲染背景
    SCREEN.blit(background_image, (0, 0))
    # 根据朝向渲染角色
    if is_facing_right:
        SCREEN.blit(player_image, (player_x, player_y))
    else:
        flipped_player_image = pygame.transform.flip(player_image, True, False)
        SCREEN.blit(flipped_player_image, (player_x, player_y))
    # 渲染血量指示器
    for i in range(player_health):
        SCREEN.blit(heart_image, (heart_x + i * heart_spacing, heart_y))

    pygame.display.update()

# 游戏结束
pygame.quit()
sys.exit()
