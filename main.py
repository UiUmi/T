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

pygame.mixer.music.load('music\music.mp3')  # 加载音乐文件，确保文件路径正确
my_sound = pygame.mixer.Sound('music\music.mp3')
#my_sound.play(-1)  # 无限循环播放
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
player_speed = 2.6
jump_speed = 7
gravity = 0.3

# 定义主角的位置和朝向
player_x = 50
player_y = HEIGHT - 240
is_facing_right = True

# 跳跃状态
is_jumping = False
jump_velocity = 0

# 奔跑状态
is_running = False

#是否有Monster
is_monster_exit=False

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


# 主角金币数和金币图像加载
coins_icon = pygame.image.load("coin.png")
coins_icon = pygame.transform.scale(coins_icon, (30, 30))

# 加载菜单背景图像
menu_background = pygame.image.load("menu.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

# 加载开始和退出按钮以及title
Title = pygame.image.load("Title.png")
Title = pygame.transform.scale(Title, (800, 130))
start_button = pygame.image.load("start.png")
start_button = pygame.transform.scale(start_button, (200, 150))
exit_button = pygame.image.load("exit.png")
exit_button = pygame.transform.scale(exit_button, (200, 150))

# 设置按钮位置
start_button_pos = (WIDTH // 2 - 100, HEIGHT // 2 - 20)
exit_button_pos = (WIDTH // 2 - 100, HEIGHT // 2 + 80)
Title_pos=(WIDTH//2-400,HEIGHT//2-250)

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
class InventoryItem:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class PlayerInventory:
    def __init__(self):
        self.items = []

    def add_item(self, item_name, quantity=1):
        # 检查物品是否已经存在于背包中
        for item in self.items:
            if item.name == item_name:
                item.quantity += quantity
                return

        # 如果物品不存在，添加新的物品
        new_item = InventoryItem(name=item_name, quantity=quantity)
        self.items.append(new_item)

    def remove_item(self, item_name, quantity=1):
        # 从背包中移除指定数量的物品
        for item in self.items:
            if item.name == item_name:
                item.quantity -= quantity
                if item.quantity <= 0:
                    self.items.remove(item)
                return

    def get_item_quantity(self, item_name):
        # 获取背包中指定物品的数量
        for item in self.items:
            if item.name == item_name:
                return item.quantity
        return 0

# 创建主角的背包
player_inventory = PlayerInventory()


# 金币数量
coins = 100
# 设置字体和变量
font_size = 36
font = pygame.font.Font(None, font_size)  # 使用默认字体
num_of_coins = f"x {coins}"
# 渲染文本到 Surface
coins_surface = font.render(num_of_coins, True, (255, 255, 255))  # 文本颜色为黑色

# 获取 Surface 的矩形对象
coins_rect = coins_surface.get_rect()

# 设置文本位置
coins_rect.center = (90, 75)

# 保存玩家数据
def save_player_data():
    with open("player_data.txt", "w") as file:
        file.write(str(coins) + "\n")
        for item in player_inventory:
            file.write(item.name + "\n")

# 加载玩家数据
def load_player_data():
    global coins
    global player_inventory
    try:
        with open("player_data.txt", "r") as file:
            lines = file.readlines()
            coins = int(lines[0].strip())
            inventory = [Product(name.strip(), 0) for name in lines[1:]]
    except FileNotFoundError:
        # 如果文件不存在，使用默认值
        coins = 100
        player_inventory = []

# 在购买商品时的逻辑
def buy_product(product):
    global coins
    if coins >= product.price:
        coins -= product.price
        player_inventory.add_item(product)
        print(f"You bought {product.name} for {product.price} coins!")

    else:
        print("Not enough coins!")

# 在其他地方更新显示玩家的金币数量和背包
def update_display():
    # 更新金币数量的显示
    # SCREEN.blit(coins_icon, (coin_x + i * coin_spacing, coin_y))
    # pygame.display.update()

    # 更新背包的显示
    for i, item in enumerate(inventory):
        print(f"Item {i + 1}: {item.name}")

class Product:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (70, 70))
product1 = Product("Health Potion", 10, "health_potion.png")
product2 = Product("Speed Potion", 5, "speed_potion.png")
product3 = Product("Jump Potion", 5, "jump_potion.png")
product4= Product("ak_potion", 15, "ak_potion.png")
product5= Product("character", 30, "player.png")

# 创建商品列表
products = [product1, product2, product3,product4,product5]
num_of_products=5

# 商品显示字体
product_font = pygame.font.SysFont(None, 30)

# 商品矩形列表，用于处理鼠标点击
product_rects = []

# 故事框相关设置
story_box_background = pygame.image.load("story_box_background.png")
story_box_background = pygame.transform.scale(story_box_background, (1100, 700))
subtitle_font = pygame.font.SysFont(None, 30)
subtitle_timer = pygame.time.get_ticks()
subtitle_delay = 2000  # 2秒显示一个字幕
story_text = [
    "Once upon a time, in the world of algorithms and code...",
    "You, a bright and ambitious computer science student, embarked on a journey",
    "to explore the vast landscape of programming and software development.",
    "",
    "Your first challenge was to unravel the mysteries of programming languages.",
    "You dived into the realms of Python, Java, and C++, each line of code",
    "bringing you closer to the power of turning logic into reality.",
    "",
    "With each passing semester, you faced new quests - algorithms, data structures,",
    "and the enchanted world of artificial intelligence.",
    "",
    "And so, with your keyboard as your sword and your IDE as your shield,",
    "you step into the world, ready to write your own code odyssey."
]

current_story_index = 0
story_box_open = False
story_box_pos = (WIDTH/2-550, -50)
music_box_open = False
music_box_pos = (300,150)

inventory_box_open=False
inventory_box_pos = ((WIDTH - 1100) // 2, 50)
# 背包内容
inventory_box_background = pygame.image.load("story_box_background.png")
inventory_box_background = pygame.transform.scale(story_box_background, (500, 500)) ###


rule_box_open = False
rule_box_pos = (WIDTH/2-550, -50)
rule_box_background = pygame.image.load("rule_box_background.png")
rule_box_background = pygame.transform.scale(rule_box_background, (1100, 700))

#######各个图标的建立
# 故事框按钮
story_box_button = pygame.image.load("story_box_button.png")
story_box_button = pygame.transform.scale(story_box_button, (100, 100))
story_box_button_pos = (WIDTH - 98, store_icon_pos[1] + store_icon.get_height() -8)  # 放置在商店图标下方

# 音乐框
music_box_button=pygame.image.load("music_box_button.png")
music_box_button = pygame.transform.scale(music_box_button, (70, 70))
music_box_button_pos = (WIDTH - 80, story_box_button_pos[1] + store_icon.get_height() -10)  # 放置在故事按钮框图标下方
##背包图标
inventory_box_button = pygame.image.load("inventory_button.png")
inventory_box_button = pygame.transform.scale(inventory_box_button, (80, 80))
inventory_box_button_pos = (0,90)
# 规则图标
rule_button = pygame.image.load("rule_button.png")
rule_button = pygame.transform.scale(rule_button, (110,95))
rule_button_pos= (WIDTH - 105, story_box_button_pos[1] + store_icon.get_height() +60)


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
            elif story_box_button_pos[0] < mouse_pos[0] < story_box_button_pos[0] + 100 \
                    and story_box_button_pos[1] < mouse_pos[1] < story_box_button_pos[1] + 100:
                story_box_open = not story_box_open
                if story_box_open:
                    subtitle_timer = pygame.time.get_ticks()  # 重新设置计时器
            elif music_box_button_pos[0] < mouse_pos[0] < music_box_button_pos[0] + 50 \
                    and music_box_button_pos[1] < mouse_pos[1] < music_box_button_pos[1] + 50:
                music_box_open = not music_box_open
                if music_box_open:
                    subtitle_timer = pygame.time.get_ticks()
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.play(-1)  # -1 表示无限循环播放
                else:
                    pygame.mixer.music.pause()
            elif inventory_box_button_pos[0]< mouse_pos[0] < inventory_box_button_pos[0]+100\
                    and inventory_box_button_pos[1] <mouse_pos[1]< inventory_box_button_pos[1]+100:

                inventory_box_open = not inventory_box_open
            elif rule_button_pos[0] < mouse_pos[0] < rule_button_pos[0] + 110 and rule_button_pos[1] < mouse_pos \
                [1] < rule_button_pos[1] + 95:

                rule_box_open = not rule_box_open




    if in_menu:
        # 渲染菜单背景
        SCREEN.blit(menu_background, (0, 0))

        # 渲染开始和退出按钮
        SCREEN.blit(Title, Title_pos)
        SCREEN.blit(start_button, start_button_pos)
        SCREEN.blit(exit_button, exit_button_pos)

    pygame.display.update()

    if not in_menu:
        if in_store:
            # 渲染商店页面
            SCREEN.blit(store_background, (450, 100))
            SCREEN.blit(store_close_button, (480, 530))

            # 渲染商品
            for i, product in enumerate(products):
                col = i % 2  # 每行最多显示2个商品

                x = 480 + col * 118  # 根据列数计算 x 坐标
                y = 220 + (i // 2) * 101  # 计算 y 坐标，每两个商品一行

                product_rect = SCREEN.blit(product.image, (x, y))
                product_rects.append(product_rect)

                # 渲染商品价格
                price_font = pygame.font.Font(None, 25)
                price_text = f"${product.price}"
                price_surface = price_font.render(price_text, True, (255, 255, 255))
                price_rect = price_surface.get_rect(midleft=(product_rect.right + 10, product_rect.centery))
                SCREEN.blit(price_surface, price_rect)

            # 检测商店中的鼠标点击
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # 检查鼠标点击是否在退出按钮上
                if store_close_button_pos[0] < mouse_pos[0] < store_close_button_pos[0] + 84 \
                        and store_close_button_pos[1] < mouse_pos[1] < store_close_button_pos[1] + 63:
                    in_store = False
                    running = True
                else:
                    # 检查商品是否被点击
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                    for i in range(num_of_products):
                        if 480 < mouse_pos[0] < 480+70 and 220 + 95*i < mouse_pos[1] < 220 + 70 + 95*i:
                            buy_product(products[i])
                            pygame.time.delay(500)

                            # 在这里可以执行购买商品的逻辑

                # 检查鼠标点击是否在退出按钮上


            # 在这里添加以下代码



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
            num_of_coins = f"x {coins}"
            coins_surface = font.render(num_of_coins, True, (255, 255, 255))
            SCREEN.blit(coins_icon, (coin_x, coin_y))
            SCREEN.blit(coins_surface, coins_rect)
            # 渲染商店图标
            SCREEN.blit(store_icon, store_icon_pos)

            # 渲染故事框按钮
            SCREEN.blit(story_box_button, story_box_button_pos)
            # 渲染音乐框按钮
            SCREEN.blit(music_box_button, music_box_button_pos)
            # 渲染背包框
            SCREEN.blit(inventory_box_button, inventory_box_button_pos)
            #渲染规则框
            SCREEN.blit(rule_button, rule_button_pos)
            # 如果故事框打开，渲染故事文本
            if story_box_open:
                SCREEN.blit(story_box_background, story_box_pos)
                elapsed_time = pygame.time.get_ticks() - subtitle_timer
                if elapsed_time < subtitle_delay * len(story_text):
                    current_index = elapsed_time // subtitle_delay
                    rendered_text = story_text[:current_index + 1]
                    for i, line in enumerate(rendered_text):
                        text_surface = subtitle_font.render(line, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=(story_box_pos[0] + 550, story_box_pos[1] + 250 + i * 30))
                        SCREEN.blit(text_surface, text_rect)
                else:
                    # 当字幕全部显示完毕后，重新开始循环
                    subtitle_timer = pygame.time.get_ticks()
            if rule_box_open:
                # 渲染 story_box_background.png 和相关文本
                SCREEN.blit(rule_box_background, rule_box_pos)
                # 其他渲染逻辑...
            if inventory_box_open :
                SCREEN.blit(inventory_box_background,inventory_box_pos)


            pygame.display.update()

# 游戏结束
pygame.quit()
sys.exit()


