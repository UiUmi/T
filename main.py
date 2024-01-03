import pygame
import random
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
icon = pygame.image.load("head.png")  # 设置游戏窗口图标
pygame.display.set_icon(icon)
pygame.mixer.init()  # 加载和播放声音

pygame.mixer.music.load('music\music.mp3')  # 加载音乐文件，确保文件路径正确
my_sound = pygame.mixer.Sound('music\music.mp3')
#my_sound.play(-1)  # 无限循环播放
my_sound.set_volume(0.2)

# 加载游戏背景图像
background_image = pygame.image.load("city.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# 获取背景图像的宽度
bg_width = background_image.get_width()

# 定义背景滚动的速度
scroll_speed = 2
bgp_move=False
# 初始化背景的位置
bg_x1 = 0
bg_x2 = bg_width

# 加载主角奔跑动画帧
run_frames = [
    pygame.image.load("player_run1.png"),
    pygame.image.load("player_run2.png"),
    pygame.image.load("player_run3.png")
]
current_frame = 0
player_image = run_frames[current_frame]
player_image = pygame.transform.scale(player_image, (60, 60))


is_in_city=True

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
monster_attack_duration = 0.1
player_attack_timer = 0.0
monster_attack_timer = 0.0
player_attack_animation = pygame.image.load("player_attack_animation.png")  # 替换为你的攻击动画图片
player_attack_animation = pygame.transform.scale(player_attack_animation, (60, 60))
player_last_get_attack_time=pygame.time.get_ticks()
#人物撞击伤害
player_damage=1
current_level_start=True
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
is_monster_exist=False

#是否在主城
is_in_main=True

# 玩家血量
player_health = 20

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
selected_level=0
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


class LevelButton:
    def __init__(self, rect, level):
        self.rect = rect  # pygame.Rect 对象，表示按钮在屏幕上的位置和大小
        self.level = level  # 与按钮关联的关卡

# 在初始化部分或其他适当的地方创建关卡按钮对象并添加到 level_buttons 列表中
level_buttons = []

# 示例：创建两个关卡按钮，分别关联关卡 1 和关卡 2
button_rect1 = pygame.Rect(550, 280, 100, 100)  # 根据实际需求设置按钮位置和大小
button_rect2 = pygame.Rect(550, 280, 100, 100)
level_buttons.append(LevelButton(button_rect1, level=1))
level_buttons.append(LevelButton(button_rect2, level=2))



# 在其他地方更新显示玩家的金币数量和背包
def update_display():


    # 更新背包的显示
    for i, item in enumerate(player_inventory):
        print(f"Item {i + 1}: {item.name}")
player_attack_cooldown = 500
player_last_attack_time=pygame.time.get_ticks()
class Product:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (70, 70))
product1 = Product("health_potion", 15, "health_potion.png")
product2 = Product("speed_potion", 10, "speed_potion.png")
product3 = Product("jump_potion", 10, "jump_potion.png")
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
rule_box_pos = (WIDTH/2-550, -115)
rule_box_pos = (rule_box_pos[0], rule_box_pos[1] - 10)
rule_box_background = pygame.image.load("rule_box_background.png")
rule_box_background = pygame.transform.scale(rule_box_background, (1100, 1000))

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

class Monster:
    def __init__(self,name,health,speed,image_path,damage,size):
        self.name=name
        self.damage = damage
        self.size = size
        self.health=health
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.run_frames = [pygame.image.load(f"{name}_run{i + 1}.png") for i in range(3)]

monster1=Monster(name="monster1",health=10,speed=2,image_path="monster1.png",damage=1,size=(60,60))
monster2=Monster(name="monster2",health=5,speed=3,image_path="monster2.png",damage=2,size=(50,50))
Boss=Monster(name="Boss",health=100,speed=0,image_path="Boss.png",damage=3,size=(200, 400))

last_spawn_time=pygame.time.get_ticks()
class Exist_Monster:
    def __init__(self,name,pos,current_frame,is_facing_right,dect,move_counter,is_moving):
        self.current_frame = current_frame
        self.is_facing_right=is_facing_right
        self.is_moving=is_moving
        self.health = name.health
        self.damage = name.damage
        self.is_attacking=False
        self.jump_velocity = 0
        self.name=name
        self.move_counter=move_counter
        self.last_flip_time = pygame.time.get_ticks()  # 记录上次反转的时间
        self.last_attack_time = pygame.time.get_ticks()  # 记录上次反attack的时间
        self.pos = pos
        self.dect=dect
exist_monsters=[]

level1 = pygame.image.load("level1.png")
level1 = pygame.transform.scale(level1, (100, 100))
level1_pos = (450,280)
exist_monster1_0=Exist_Monster(name=monster1,pos=(700, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster1_1=Exist_Monster(name=monster1,pos=(750, HEIGHT - 240),current_frame=0,is_facing_right=1,dect=False,move_counter=0,is_moving=1)
exist_monster1_2=Exist_Monster(name=monster1,pos=(800, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster2_0=Exist_Monster(name=monster1,pos=(700, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster2_1=Exist_Monster(name=monster1,pos=(750, HEIGHT - 240),current_frame=0,is_facing_right=1,dect=False,move_counter=0,is_moving=1)
exist_monster2_2=Exist_Monster(name=monster1,pos=(800, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster2_3=Exist_Monster(name=monster1,pos=(200, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster2_4=Exist_Monster(name=monster1,pos=(250, HEIGHT - 240),current_frame=0,is_facing_right=1,dect=False,move_counter=0,is_moving=1)
exist_monster3_0=Exist_Monster(name=monster1,pos=(700, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster3_1=Exist_Monster(name=monster1,pos=(750, HEIGHT - 240),current_frame=0,is_facing_right=1,dect=False,move_counter=0,is_moving=1)
exist_monster3_2=Exist_Monster(name=monster1,pos=(800, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster3_3=Exist_Monster(name=monster1,pos=(200, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster3_4=Exist_Monster(name=monster2,pos=(800, HEIGHT - 440),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster3_5=Exist_Monster(name=monster2,pos=(750, HEIGHT - 440),current_frame=0,is_facing_right=1,dect=False,move_counter=0,is_moving=1)


level1_1_monsters=[exist_monster1_0,exist_monster1_1,exist_monster1_2]
level1_2_monsters=[exist_monster2_0,exist_monster2_1,exist_monster2_2,exist_monster2_3,exist_monster2_4]
level1_3_monsters=[exist_monster3_0,exist_monster3_1,exist_monster3_2,exist_monster3_3,exist_monster3_4,exist_monster3_5]



level2 = pygame.image.load("level2.png")
level2 = pygame.transform.scale(level2, (100, 100))
level2_pos = (546,280)


exist_Boss=Exist_Monster(name=Boss,pos=(900,HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster2__1=Exist_Monster(name=monster1,pos=(800, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster2__2=Exist_Monster(name=monster1,pos=(200, HEIGHT - 240),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster2__3=Exist_Monster(name=monster2,pos=(800, HEIGHT - 440),current_frame=0,is_facing_right=-1,dect=False,move_counter=0,is_moving=1)
exist_monster2__4=Exist_Monster(name=monster2,pos=(750, HEIGHT - 440),current_frame=0,is_facing_right=1,dect=False,move_counter=0,is_moving=1)


level2_monsters=[exist_monster2__1,exist_monster2__2,exist_monster2__3,exist_monster2__4,exist_Boss]

bullets=[]
bullet_image=pygame.image.load("Bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (30, 30))

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
                    and store_icon_pos[1] < mouse_pos[1] < store_icon_pos[1] + 100 :
                in_store = not in_store

            # 检查鼠标点击是否在故事框按钮上
            elif story_box_button_pos[0] < mouse_pos[0] < story_box_button_pos[0] + 100 \
                    and story_box_button_pos[1] < mouse_pos[1] < story_box_button_pos[1] + 100 and is_in_city:
                story_box_open = not story_box_open
                if story_box_open:
                    subtitle_timer = pygame.time.get_ticks()  # 重新设置计时器
            #map选择
            elif map_icon_pos[0] < mouse_pos[0] < map_icon_pos[0] + 100 and map_icon_pos[1] < mouse_pos[1] < map_icon_pos[1] + 100 and is_in_city:
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
                [1] < rule_button_pos[1] + 95 and is_in_city:

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

                x = 500 + col * 118  # 根据列数计算 x 坐标
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
                    current_time = pygame.time.get_ticks()
                    if current_time-player_last_attack_time>player_attack_cooldown:
                        player_is_attacking = True
                        player_last_attack_time=pygame.time.get_ticks()
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
            if is_monster_exist:
                for m in exist_monsters:
                    if m.is_moving==1:
                        m.current_frame = (m.current_frame + 1) % len(m.name.run_frames)
                        m.name.image = m.name.run_frames[m.current_frame]
                        m.name.image = pygame.transform.scale(m.name.image, (60, 60))
            # 跳跃
            if not is_jumping:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and player_y == player_ground:
                    is_jumping = True

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
            if (player_y < player_ground and not is_jumping)or jump_velocity!=0:
                player_y -= jump_velocity
                jump_velocity -= gravity





            if is_monster_exist :
                for m in exist_monsters:
                    if m.name==monster1:
                        if m.pos[1] < player_ground or m.jump_velocity!=0:
                            m.pos=(m.pos[0] ,m.pos[1]- m.jump_velocity)
                            m.jump_velocity -= gravity

            # 限制主角在窗口范围内
            player_x = max(0, min(player_x, WIDTH - 30))
            player_y = max(0, min(player_y, player_ground))
            if is_monster_exist:
                for m in exist_monsters:
                    if m.name==Boss:
                        m.pos = (max(0, min(m.pos[0], WIDTH - 30)),max(0, min(m.pos[1], player_ground-150)))
                    else:
                        m.pos = (max(0, min(m.pos[0], WIDTH - 30)), max(0, min(m.pos[1], player_ground)))

            # 渲染背景
            SCREEN.blit(background_image, (0, 0))

            if bgp_move:
                # 更新背景的位置
                bg_x1 -= scroll_speed
                bg_x2 -= scroll_speed
                # 如果第一张背景完全移出屏幕，将其放到第二张背景的后面
                if bg_x1 <= -bg_width:
                    bg_x1 = bg_width
                    bgp_move = False
                # 如果第二张背景完全移出屏幕，将其放到第一张背景的后面
                if bg_x2 <= -bg_width:
                    bg_x2 = bg_width
                    bgp_move = False
                player_x-=scroll_speed
            # 绘制背景
                SCREEN.blit(background_image, (bg_x1, 0))
                SCREEN.blit(background_image, (bg_x2, 0))
            # 根据朝向渲染
            if is_monster_exist:
                for m in exist_monsters:
                    if m.is_facing_right==-1:
                        flipped_m = pygame.transform.flip(m.name.image, True, False)
                        if m.name==Boss:
                            flipped_m=pygame.image.load("Boss.png")
                            flipped_m = pygame.transform.flip(flipped_m, True, False)
                            flipped_m=pygame.transform.scale(flipped_m, m.name.size)
                        SCREEN.blit(flipped_m, m.pos)
                    else:
                        if m.name==Boss:
                            m.name.image = pygame.image.load("Boss.png")
                            m.name.image=pygame.transform.scale(m.name.image, m.name.size)
                        SCREEN.blit(m.name.image, m.pos)
            if is_facing_right:
                SCREEN.blit(player_image, (player_x, player_y))
            else:
                flipped_player_image = pygame.transform.flip(player_image, True, False)
                SCREEN.blit(flipped_player_image, (player_x, player_y))
            # 渲染血量指示

            num_of_heart = f"x {player_health}"
            heart_surface = font.render(num_of_heart, True, (255, 255, 255))
            SCREEN.blit(heart_image, (coin_x-5, 5))
            SCREEN.blit(heart_surface, (50,8))
            # 渲染金币指示器
            num_of_coins = f"x {coins}"
            coins_surface = font.render(num_of_coins, True, (255, 255, 255))
            SCREEN.blit(coins_icon, (coin_x, coin_y))
            SCREEN.blit(coins_surface, coins_rect)
            # 渲染商店图标
            if is_in_city:

                # 渲染map图标
                SCREEN.blit(map_icon, map_icon_pos)
                # 渲染规则框
                SCREEN.blit(rule_button, rule_button_pos)
                # 渲染故事框按钮
                SCREEN.blit(story_box_button, story_box_button_pos)
            #在关卡内部和主城中都渲染商店
            SCREEN.blit(store_icon, store_icon_pos)
            # 渲染音乐框按钮
            SCREEN.blit(music_box_button, music_box_button_pos)
            # 渲染背包框
            SCREEN.blit(inventory_box_button, inventory_box_button_pos)
            if in_map:
                SCREEN.blit(map, map_pos)
                SCREEN.blit(level1, level1_pos)
                SCREEN.blit(level2, level2_pos)
                for level_button in level_buttons:
                    if level_button.rect.collidepoint(mouse_pos):
                        selected_level = level_button.level
                        # 执行关卡选择的逻辑
                        if selected_level==1:
                            background_image = pygame.image.load("level1_bgp.png")
                            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
                        elif selected_level==2:
                            background_image = pygame.image.load("level2_bgp.png")
                            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
                        is_in_city=False
                        in_map = False
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


                # 渲染 story_box_background.png 和相关文本
            if rule_box_open:


                SCREEN.blit(rule_box_background, rule_box_pos)

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
                                        player_health += 3
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
                                    # 在物品使用逻辑中添加 jump_potion
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

                                    elif product.name == "ak_potion":
                                        player_damage+=1
                                        # Remove the ak_potion from the player's inventory
                                        player_inventory.remove_item("ak_potion")
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
            if 1<=selected_level<2:
                # 生成怪物（在屏幕右侧固定位置生成）
                if selected_level==1 and current_level_start:
                    is_monster_exist=True
                    exist_monsters = level1_1_monsters.copy()
                    current_level_start=False
                elif selected_level==1.1 and not bgp_move and current_level_start:
                    is_monster_exist = True
                    exist_monsters = level1_2_monsters.copy()
                    current_level_start=False
                elif 1.19<selected_level<1.21 and not bgp_move and current_level_start:
                    is_monster_exist = True
                    exist_monsters = level1_3_monsters.copy()
                    current_level_start=False

                if len(exist_monsters)==0 and selected_level<=1.21 and not bgp_move and not current_level_start:
                    selected_level+=0.1
                    if selected_level<1.3:
                        bgp_move=True
                    current_level_start=True
                if 1.29<selected_level<1.31:
                    selected_level=0
                    player_health += 5
                    is_in_city=True
                    background_image = pygame.image.load("city.png")
                    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            elif selected_level==2:
                if current_level_start:
                    is_monster_exist = True
                    exist_monsters = level2_monsters.copy()
                    last_spawn_time = pygame.time.get_ticks()
                    current_level_start=False
                    last_spawn_time=pygame.time.get_ticks()

                current_time=pygame.time.get_ticks()
                is_Boss_exist = False
                for m in exist_monsters:
                    if m.name==Boss:
                        is_Boss_exist=True
                if  (current_time-last_spawn_time)>10000 and is_Boss_exist:
                    exist_monsters += level2_monsters.copy()
                    last_spawn_time = pygame.time.get_ticks()
                if len(exist_monsters)==0 and not current_level_start:
                    selected_level=0
                    is_in_city = True
                    player_health += 5
                    background_image = pygame.image.load("city.png")
                    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            for m in exist_monsters:
                if abs(player_x - m.pos[0])<200 and not m.dect:
                    m.dect=True
                if not m.dect:
                    m.move_counter+=m.name.speed
                    if m.move_counter > 300:
                        current_time = pygame.time.get_ticks()
                        m.move_counter = 0  # 重置计数器
                        m.is_moving = 0
                        m.last_flip_time=current_time

                if m.is_moving==0:
                    stay_time = pygame.time.get_ticks() - m.last_flip_time
                    if stay_time > 1000:
                        m.is_moving = 1
                        m.is_facing_right *= random.choice([-1, +1])  # 反转fangxiang
                if m.dect:
                    if player_x < m.pos[0]:  # 如果玩家在怪物的左边
                        m.is_facing_right = -1
                    elif player_x > m.pos[0]:  # 如果玩家在怪物的右边
                        m.is_facing_right = 1

                m.pos = (m.pos[0] + m.is_moving*m.is_facing_right * m.name.speed, m.pos[1])

                if abs(player_x - m.pos[0]) < 50 + 60 and pygame.time.get_ticks() - m.last_attack_time>1000:


                    m.is_attacking = True
                    if m.is_facing_right == 1:
                        # 攻击动作
                        if m.name==monster1:
                            m.pos = (m.pos[0] + 10, m.pos[1])
                        elif m.name == monster2:
                            if len(bullets) < 100:
                                bullets.append((m.pos[0],m.pos[1]))
                    else:
                        # 攻击动作
                        if m.name == monster1:
                            m.pos = (m.pos[0] - 10, m.pos[1])
                        elif m.name==monster2:
                            if len(bullets)<100:
                                bullets.append((m.pos[0],m.pos[1]))
                    monster_attack_timer += dt
                    # 攻击动画持续0.2s
                    if monster_attack_timer >= monster_attack_duration:
                        m._is_attacking = False
                        current_time = pygame.time.get_ticks()
                        m.last_attack_time=current_time
                        monster_attack_timer = 0.0

                if player_is_attacking:
                    if m.name==Boss:
                        if player_x -140 < m.pos[0] < player_x + 120 and player_y - 200 <= m.pos[1] <= player_y + 70:
                            m.jump_velocity = 3
                            m.health -= player_damage
                            if m.health <= 0:
                                exist_monsters.remove(m)
                                coins+=20
                    else:
                        if player_x + 60 < m.pos[0] < player_x + 120 and player_y - 10 <= m.pos[1] <= player_y + 70:
                            m.jump_velocity = 3
                            m.health -= player_damage
                            if m.health <= 0:
                                exist_monsters.remove(m)
                                coins += 20

                if not player_is_attacking and m.is_attacking and pygame.time.get_ticks()-player_last_get_attack_time>700:
                    if player_x  < m.pos[0] < player_x + 60 and player_y <= m.pos[1] <= player_y + 60:
                        player_health-=m.damage
                        jump_velocity = 5
                        current_time = pygame.time.get_ticks()
                        player_last_get_attack_time = current_time
            bullets_to_remove=[]
            for i, p in enumerate(bullets.copy()):
                if p[1] > player_ground+50:
                    bullets_to_remove.append(i)  # 如果子弹超出屏幕，从列表中移除
                if player_x-20<p[0]<player_x+50 and player_y<p[1]<player_y+50:
                    player_health-=2
                    bullets_to_remove.append(i)

            for i in reversed(bullets_to_remove):
                bullets.pop(i)

            for i, p in enumerate(bullets.copy()):
                bullets[i] = (p[0], p[1] + 5)
                SCREEN.blit(bullet_image, bullets[i])
            if player_health<=0:
                selected_level = 0
                is_in_city = True
                exist_monsters=[]
                player_health+=5
                current_level_start=True
                if player_health<5:
                    player_health=5
                background_image = pygame.image.load("city.png")
                background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    pygame.display.update()
# 游戏结束
pygame.quit()
sys.exit()


