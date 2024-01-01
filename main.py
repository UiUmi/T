import pygame
import sys

# 初始化 Pygame
pygame.init()
FPS = 60
clock = pygame.time.Clock()
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
    pygame.image.load("player_run1.png"),
    pygame.image.load("player_run2.png"),
    pygame.image.load("player_run3.png")
]
current_frame = 0
player_image = run_frames[current_frame]
player_image = pygame.transform.scale(player_image, (60, 60))

# 加载红色爱心图像
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))

# 加载map图像
map = pygame.image.load("map.png")
map = pygame.transform.scale(map, (700, 600))
map_pos=(250,50)
# 加载map_icon图像
map_icon = pygame.image.load("map_icon.png")
map_icon = pygame.transform.scale(map_icon, (100, 100))
map_icon_pos=(-10,150)
# 设置速度和跳跃高度为 1
normal_speed=4.6
player_speed = normal_speed

jump_speed = 7
gravity = 0.3

# attack变量
player_is_attacking = False
player_attack_duration = 0.3
player_attack_timer = 0.0
player_attack_animation = pygame.image.load("player_attack_animation.png")  # 替换为你的攻击动画图片
player_attack_animation = pygame.transform.scale(player_attack_animation, (60, 60))

#人物撞击伤害
player_damage=1

# 定义主角的位置和朝向
player_x = 50
player_y = HEIGHT - 240
is_facing_right = True

# 跳跃状态
is_jumping = False
jump_velocity = 0

##################跳跃
# 在你的初始化部分定义以下变量
original_jump_speed=7
is_jump_potion_active = False
jump_potion_duration = 0.0

# 奔跑状态
is_running = False

#是否有Monster
is_monster_exit=False

#是否在主城
is_in_main=True

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
Title = pygame.transform.scale(Title, (1000, 730))
start_button = pygame.image.load("start.png")
start_button = pygame.transform.scale(start_button, (200, 150))
exit_button = pygame.image.load("exit.png")
exit_button = pygame.transform.scale(exit_button, (200, 150))

# 设置按钮位置
start_button_pos = (WIDTH // 2 - 100, HEIGHT // 2 - 20)
exit_button_pos = (WIDTH // 2 - 100, HEIGHT // 2 + 80)
Title_pos=(WIDTH//2-450,HEIGHT//2-420)

# 标志，用于指示游戏是在菜单还是进行中
in_menu = True
in_map = False
# 加载商店图标
store_icon = pygame.image.load("store_icon.png")
store_icon = pygame.transform.scale(store_icon, (100, 100))
store_icon_pos = (WIDTH - 100, 0)

# 商店背景和按钮
current_store_page = 0
store_background = pygame.image.load("store.png")
store_background = pygame.transform.scale(store_background, (300, 500))
store_last_button = pygame.image.load("store_last_button.png")
store_last_button = pygame.transform.scale(store_last_button, (84, 63))
store_last_button_pos = (480, 530)
store_next_button = pygame.image.load("store_next_button.png")
store_next_button = pygame.transform.scale(store_next_button, (84, 63))
store_next_button_pos = (630, 530)
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
# 保存玩家数据
def save_player_data():
    with open("player_data.txt", "w") as file:
        file.write(str(coins) + "\n")
        for item in player_inventory.items:
            file.write(item.name + "\n")

# 在购买商品时的逻辑
def buy_product(product):
    global coins
    global player_inventory

    if coins >= product.price:
        coins -= product.price
        player_inventory.add_item(product.name)
        print(f"You bought {product.name} for {product.price} coins!")

        # Check if the product is a player character before updating the player image
        if product.name.startswith("player"):
            change_player_image(product)
    else:
        print("Not enough coins!")



def change_player_image(product):
    # Check if the product is a player character before updating the player image
    if product.name.startswith("player"):
        # Load animation frames only for player characters
        run_frames = [
            pygame.image.load(f"{product.name}_run1.png"),
            pygame.image.load(f"{product.name}_run2.png"),
            pygame.image.load(f"{product.name}_run3.png")
        ]

        # Change to the new animation frames
        global current_frame
        current_frame = 0
        global player_image
        player_image = run_frames[current_frame]
        player_image = pygame.transform.scale(player_image, (60, 60))





# 在其他地方更新显示玩家的金币数量和背包
def update_display():
    # 更新金币数量的显示
    # SCREEN.blit(coins_icon, (coin_x + i * coin_spacing, coin_y))
    # pygame.display.update()

    # 更新背包的显示
    for i, item in enumerate(player_inventory):
        print(f"Item {i + 1}: {item.name}")

class Product:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (70, 70))
product1 = Product("health_potion", 10, "health_potion.png")
product2 = Product("speed_potion", 5, "speed_potion.png")
product3 = Product("jump_potion", 5, "jump_potion.png")
product4= Product("ak_potion", 15, "ak_potion.png")
product5= Product("player1", 30, "player1.png")
product6= Product("player2", 15, "player2.png")
product7= Product("weapon1", 0, "weapon1.png")
product8= Product("player", 0, "player.png")


# 创建商品列表
products = [product1, product2, product3,product4,product5,product6,product7,product8]
num_of_products=8

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




# 在游戏循环之前定义变量
is_speed_boost_active = False
speed_boost_end_time = 0


# 游戏循环
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
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
            #map选择
            elif map_pos[0] < mouse_pos[0] < map_pos[0] + 100 and map_pos[1] < mouse_pos[1] < map_pos[1] + 100:
                in_map=not in_map

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
            SCREEN.blit(store_last_button, store_last_button_pos)
            SCREEN.blit(store_next_button, store_next_button_pos)
            # 渲染商品
            start_index = current_store_page * 6
            end_index = min((current_store_page + 1) * 6,num_of_products)
            for i, product in enumerate(products[start_index:end_index]):
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

                # 检查鼠标点击是否在上一页按钮上
                if store_last_button_pos[0] < mouse_pos[0] < store_last_button_pos[0] + 84 \
                        and store_last_button_pos[1] < mouse_pos[1] < store_last_button_pos[1] + 63:
                    #切换到上一页
                    current_store_page = max(0, current_store_page - 1)
                    running = True
                elif store_next_button_pos[0] < mouse_pos[0] < store_next_button_pos[0] + 84 \
                        and store_next_button_pos[1] < mouse_pos[1] < store_next_button_pos[1] + 63:
                    #切换到下一页
                    current_store_page = min((len(products) - 1) // 6, current_store_page + 1)
                    running = True
                else:
                    # 检查商品是否被点击
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                    for i in range(num_of_products):
                        l=i%2
                        c=i//2
                        if 480 +l*118< mouse_pos[0] < 480+70 +l*118 and 220 + 101*c < mouse_pos[1] < 220 + 70 + 101*c:
                            buy_product(products[i+current_store_page*6])
                            pygame.time.delay(500)




        if not in_store :
            # 角色移动
            keys = pygame.key.get_pressed()
            if not in_store:
                # 角色移动和攻击
                keys = pygame.key.get_pressed()
                if keys[pygame.K_j]:
                    player_is_attacking = True

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




            if player_is_attacking:
                if is_facing_right:
                    # 攻击动作
                    player_x += 10  # 向右快速移动

                    # 渲染攻击动画
                    SCREEN.blit(player_attack_animation, (player_x + 60, player_y))

                else:
                    # 攻击动作
                    player_x -= 10  # 向右快速移动
                    flipped_player_attack_animation = pygame.transform.flip(player_attack_animation, True, False)
                    SCREEN.blit(flipped_player_attack_animation, (player_x - 60, player_y))

                player_attack_timer += dt
                # 攻击动画持续0.2s
                if player_attack_timer >= player_attack_duration:
                    player_is_attacking = False
                    player_attack_timer = 0.0


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
                    # Check if the jump potion is active
                    if is_jump_potion_active:
                        jump_velocity = jump_speed  # Use the modified jump speed
                    else:
                        jump_velocity = original_jump_speed  # Use the original jump speed
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
            # 渲染map图标
            SCREEN.blit(map_icon, map_icon_pos)
            # 渲染故事框按钮
            SCREEN.blit(story_box_button, story_box_button_pos)
            # 渲染音乐框按钮
            SCREEN.blit(music_box_button, music_box_button_pos)
            # 渲染背包框
            SCREEN.blit(inventory_box_button, inventory_box_button_pos)
            #渲染规则框
            SCREEN.blit(rule_button, rule_button_pos)
            if player_is_attacking:
                if is_facing_right:
                    # 攻击动作
                    player_x += 4  # 向右快速移动

                    # 渲染攻击动画
                    SCREEN.blit(player_attack_animation, (player_x + 60, player_y))

                else:
                    # 攻击动作
                    player_x -= 4  # 向右快速移动
                    flipped_player_attack_animation = pygame.transform.flip(player_attack_animation, True, False)
                    SCREEN.blit(flipped_player_attack_animation, (player_x - 60, player_y))

                player_attack_timer += dt
                # 攻击动画持续0.2s
                if player_attack_timer >= player_attack_duration:
                    player_is_attacking = False
                    player_attack_timer = 0.0
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
            if in_map:
                SCREEN.blit(map, map_pos)


            if inventory_box_open:
                SCREEN.blit(inventory_box_background, inventory_box_pos)

                item_spacing = 60
                items_per_row = 3  # 每行显示的物品数量

                for i, item in enumerate(player_inventory.items):
                    row = i // items_per_row  # 计算行数
                    col = i % items_per_row  # 计算列数

                    item_image = pygame.image.load(f"{item.name}.png")  # 假设物品图片文件名与物品名相匹配
                    item_image = pygame.transform.scale(item_image, (50, 50))
                    x = inventory_box_pos[0] + 50 + col * 100  # 100 是每个物品之间的横向间隔
                    y = inventory_box_pos[1] + 150 + row * item_spacing
                    SCREEN.blit(item_image, (x, y))

                    # 显示物品数量
                    quantity_text = f"x {item.quantity}"
                    quantity_surface = font.render(quantity_text, True, (255, 255, 255))
                    SCREEN.blit(quantity_surface, (x + 70, y + 20))
                    # 检查鼠标点击是否在背包中的物品上
                    for i, item in enumerate(player_inventory.items):
                        row = i // items_per_row
                        col = i % items_per_row
                        x = inventory_box_pos[0] + 50 + col * 100
                        y = inventory_box_pos[1] + 150 + row * item_spacing
                        item_rect = pygame.Rect(x, y, 50, 50)

                        if item_rect.collidepoint(mouse_pos):  # 检查鼠标是否点击了某个物品
                            # 获取被点击的商品对象
                            clicked_item = player_inventory.items[i]

                            # 根据商品对象更新主角形象
                            for product in products:
                                if product.name == clicked_item.name:
                                    # 检查商品是否是主角形象
                                    if product.name.startswith("player"):
                                        # 检查奔跑动画帧是否存在
                                        run_frames_exist = all(
                                            pygame.image.get_extended() for _ in range(3)  # Check for three frames
                                        )
                                        if run_frames_exist:
                                            # 更新奔跑动画帧
                                            run_frames = [
                                                pygame.image.load(f"{product.name}_run1.png"),
                                                pygame.image.load(f"{product.name}_run2.png"),
                                                pygame.image.load(f"{product.name}_run3.png")
                                            ]

                                            # 切换到新的奔跑动画
                                            current_frame = 0
                                            player_image = run_frames[current_frame]
                                            player_image = pygame.transform.scale(player_image, (60, 60))
                                        else:
                                            print(f"Run frames not found for {product.name}")
                                        # 在这里可以执行购买商品的逻辑
                                    if product.name == "health_potion":
                                        # 增加爱心的数量
                                        player_health += 1
                                        # 从背包中移除药水
                                        player_inventory.remove_item("health_potion")
                                    elif product.name == "speed_potion":
                                        # 增加主角的移动速度
                                        player_speed += 5
                                        # 启动加速状态
                                        is_speed_boost_active = True
                                        speed_boost_duration = 800000  # 10秒，以毫秒为单位
                                        speed_boost_timer = pygame.time.get_ticks()
                                        player_inventory.remove_item("speed_potion")
                                    # 在你的物品使用逻辑中添加 jump_potion
                                    elif product.name == "jump_potion" and not is_jump_potion_active:
                                        # Store the original jump speed for later restoration
                                        original_jump_speed = jump_speed

                                        # Triple the jump speed
                                        jump_speed *= 2

                                        # Remove the jump potion from the player's inventory
                                        player_inventory.remove_item("jump_potion")

                                        # Set a flag to indicate that a jump potion is active
                                        is_jump_potion_active = True

                                        # Set the duration for the jump potion effects (adjust as needed)
                                        jump_potion_duration = 7.0  # 7 seconds, for example

                                        # Add visual feedback, such as a glowing effect or particle system
                                        # Example: player.activate_jump_visual_feedback()
                                    elif product.name == "ak_potion":
                                        player_damage+=1

                    # 在主循环中检查是否仍然处于加速状态
            if is_speed_boost_active:
                if speed_boost_duration > 0:
                    # 更新主角的位置时使用增加后的速度
                    speed_boost_duration -= (pygame.time.get_ticks() - speed_boost_timer)
                else:
                    # 加速状态结束，重置速度
                    is_speed_boost_active = False
                    player_speed -= 5
                    speed_boost_end_time = pygame.time.get_ticks()

                    # 使用正常速度

            if is_jump_potion_active:
                jump_potion_duration -= dt  # dt is the time since the last frame, adjust as needed
                if jump_potion_duration <= 0:
                    is_jump_potion_active = False
                    jump_speed = original_jump_speed  # Restore the original jump speed



                pygame.display.update()


# 游戏结束
pygame.quit()
sys.exit()


