import pygame
import sys

# 初始化 Pygame
pygame.init()

# 游戏设置
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Code Odyssey")

# 设置游戏窗口名称
icon = pygame.image.load("icon\head.png")  # 设置游戏窗口图标
pygame.display.set_icon(icon)
pygame.mixer.init()  # 加载和播放声音
my_sound = pygame.mixer.Sound('music\music.mp3')
my_sound.play(-1)  # 无限循环播放
my_sound.set_volume(0.2)

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
player_image = pygame.transform.scale(player_image, (30, 30))

# 加载红色爱心图像
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))

# 设置速度和跳跃高度为 1
player_speed = 0.6
jump_speed = 2.5
gravity = 0.03

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
coin_x = 20
coin_y = 60
coin_spacing = 40

# 主角金币数和金币图像加载
coins = 0
coins_icon = pygame.image.load("coin.png")
coins_icon = pygame.transform.scale(coins_icon, (30, 30))

# 加载菜单背景图像
menu_background = pygame.image.load("menu.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

# 加载开始和退出按钮
start_button = pygame.image.load("start.png")
start_button = pygame.transform.scale(start_button, (200, 150))
exit_button = pygame.image.load("exit.png")
exit_button = pygame.transform.scale(exit_button, (200, 200))

# 设置按钮位置
start_button_pos = (WIDTH // 2 - 100, HEIGHT // 2 - 40)
exit_button_pos = (WIDTH // 2 - 100, HEIGHT // 2 + 60)

# 标志，用于指示游戏是在菜单还是进行中
in_menu = True

# 加载商店图标
store_icon = pygame.image.load("store_icon.png")
store_icon = pygame.transform.scale(store_icon, (100, 100))
store_icon_pos = (WIDTH - 100, 0)

# 商店背景和按钮
store_background = pygame.image.load("store.png")
store_background = pygame.transform.scale(store_background, (300, 500))
store_close_button = pygame.image.load("store_close_button.png")
store_close_button = pygame.transform.scale(store_close_button, (84, 63))
store_close_button_pos = (480, 530)
in_store = False

# 故事框相关设置
story_box_background = pygame.image.load("story_box_background.png")
story_box_background = pygame.transform.scale(story_box_background, (600, 400))
subtitle_font = pygame.font.SysFont(None, 30)
subtitle_timer = pygame.time.get_ticks()
subtitle_delay = 2000  # 2秒显示一个字幕
story_text = [
    "Once upon a time, in the world of algorithms and code...",
    "You, a bright and ambitious computer science student, embarked on a journey",
    "to explore the vast landscape of programming and software development.",
    "",
    "As you entered the university, you were greeted by the binary whispers of",
    "the computers and the rhythmic hum of servers in the distance.",
    "",
    "Your first challenge was to unravel the mysteries of programming languages.",
    "You dived into the realms of Python, Java, and C++, each line of code",
    "bringing you closer to the power of turning logic into reality.",
    "",
    "With each passing semester, you faced new quests - algorithms, data structures,",
    "and the enchanted world of artificial intelligence.",
    "",
    "Late nights were spent debugging, and the glow of your screen became a beacon",
    "in the silent halls of the computer labs.",
    "",
    "You forged alliances with fellow coders, engaging in epic coding battles",
    "and collaborative quests to conquer challenging assignments.",
    "",
    "As you delved deeper, you discovered the magical repositories of open source",
    "and contributed to the collective knowledge of the programming realm.",
    "",
    "Now, as you stand on the brink of graduation, you reflect on the incredible",
    "adventure that your programming journey has been.",
    "",
    "The code scrolls before your eyes, and you realize that this is just",
    "the beginning of an endless quest for knowledge and innovation.",
    "",
    "And so, with your keyboard as your sword and your IDE as your shield,",
    "you step into the world, ready to write your own code odyssey."
]

current_story_index = 0
story_box_open = False
story_box_pos = (300, 150)


# 故事框按钮
story_box_button = pygame.image.load("story_box_button.png")
story_box_button = pygame.transform.scale(story_box_button, (50, 50))
story_box_button_pos = (WIDTH - 80, store_icon_pos[1] + store_icon.get_height() + 10)  # 放置在商店图标下方

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # 检查鼠标点击是否在开始按钮上
            if start_button_pos[0] < mouse_pos[0] < start_button_pos[0] + 200 \
                    and start_button_pos[1] < mouse_pos[1] < start_button_pos[1] + 150:
                in_menu = False

            # 检查鼠标点击是否在退出按钮上
            elif exit_button_pos[0] < mouse_pos[0] < exit_button_pos[0] + 200 \
                    and exit_button_pos[1] < mouse_pos[1] < exit_button_pos[1] + 200:
                running = False

            # 检查鼠标点击是否在商店图标上
            elif store_icon_pos[0] < mouse_pos[0] < store_icon_pos[0] + 100 \
                    and store_icon_pos[1] < mouse_pos[1] < store_icon_pos[1] + 100:
                in_store = not in_store

            # 检查鼠标点击是否在故事框按钮上
            elif story_box_button_pos[0] < mouse_pos[0] < story_box_button_pos[0] + 50 \
                    and story_box_button_pos[1] < mouse_pos[1] < story_box_button_pos[1] + 50:
                story_box_open = not story_box_open
                if story_box_open:
                    subtitle_timer = pygame.time.get_ticks()  # 重新设置计时器

    if in_menu:
        # 渲染菜单背景
        SCREEN.blit(menu_background, (0, 0))

        # 渲染开始和退出按钮
        SCREEN.blit(start_button, start_button_pos)
        SCREEN.blit(exit_button, exit_button_pos)

    pygame.display.update()

    if not in_menu:
        if in_store:
            # 渲染商店页面
            SCREEN.blit(store_background, (450, 100))
            SCREEN.blit(store_close_button, (480, 530))

            # 检测商店中的鼠标点击
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # 检查鼠标点击是否在退出按钮上
                if store_close_button_pos[0] < mouse_pos[0] < store_close_button_pos[0] + 84 \
                        and store_close_button_pos[1] < mouse_pos[1] < store_close_button_pos[1] + 63:
                    in_store = False
                    running = True

        if not in_store:
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
                    jump_velocity = jump_speed
            else:
                if player_y < player_ground or jump_velocity == jump_speed:
                    player_y -= jump_velocity
                    jump_velocity -= gravity
                else:
                    is_jumping = False
                    jump_velocity = 0

            # 应用下降重力效果
            if player_y < player_ground and not is_jumping:
                player_y -= jump_velocity
                jump_velocity -= gravity

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

            # 渲染金币指示器
            for i in range(coins):
                SCREEN.blit(coins_icon, (coin_x + i * coin_spacing, coin_y))

            # 渲染商店图标
            SCREEN.blit(store_icon, store_icon_pos)

            # 渲染故事框按钮
            SCREEN.blit(story_box_button, story_box_button_pos)

            # 如果故事框打开，渲染故事文本
            if story_box_open:
                SCREEN.blit(story_box_background, story_box_pos)
                elapsed_time = pygame.time.get_ticks() - subtitle_timer
                if elapsed_time < subtitle_delay * len(story_text):
                    current_index = elapsed_time // subtitle_delay
                    rendered_text = story_text[:current_index + 1]
                    for i, line in enumerate(rendered_text):
                        text_surface = subtitle_font.render(line, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=(story_box_pos[0] + 300, story_box_pos[1] + 50 + i * 30))
                        SCREEN.blit(text_surface, text_rect)
                else:
                    # 当字幕全部显示完毕后，重新开始循环
                    subtitle_timer = pygame.time.get_ticks()

            pygame.display.update()

# 游戏结束
pygame.quit()
sys.exit()
