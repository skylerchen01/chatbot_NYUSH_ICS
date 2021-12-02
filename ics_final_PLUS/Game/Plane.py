import pygame, sys

# from chat import mysend, myrecv
from chat_client_class import *
from chat_utils import *
# import chat_cmdl_client
# import chat_group
# import chat_server

# import client_state_machine
# import encrypt
# import indexer
# import login
# import roman2num



pathgame = sys.path[0]

bulletimage = pathgame + '/Game/bullet.png'
planeimage = pathgame + '/Game/plane.png'
musicpath = pathgame + '/Game/ZHANG JUN - 未来纪元 (Original Mix) (mp3cut.net).mp3'



class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_img = bullet_img
        self.image = pygame.image.load(bulletimage).convert()
        self.rect = self.bullet_img.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.is_hit = False
        self.life = 300

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)


    def moveUp(self):
        if self.rect.top <= 0:
           self.rect.top = 0
        else:
            self.rect.top -= self.speed


    def moveDown(self):
        if self.rect.top >= 700 - self.rect.height:
            self.rect.top = 700 - self.rect.height
        else:
            self.rect.top += self.speed


    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed


    def moveRight(self):
        if self.rect.left >= 500 - self.rect.width:
            self.rect.left = 500 - self.rect.width
        else:
            self.rect.left += self.speed

class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_img = bullet_img
        self.image = pygame.image.load(bulletimage).convert()
        self.rect = self.bullet_img.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10
        self.life = 300


    def move(self):
        self.rect.top += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []  # 用来存储玩家飞机图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]  # 初始化图片所在的矩形
        self.rect.topleft = init_pos  # 初始化矩形的左上角坐标
        self.speed = 8  # 初始化玩家飞机速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()  # 玩家飞机所发射的子弹的集合
        self.is_hit = False  # 玩家是否被击中
        self.life = 200


    def reassign_position(self,socket):
        l = json.loads(myrecv(socket))['position']
        if l:
            x,y = l
            x = 500-x
            y = 700-y
            print('position: ',x,y)
            self.rect.bottomright = [x,y]


    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed


    def moveRight(self):
        if self.rect.left >= 500 - self.rect.width:
            self.rect.left = 500 - self.rect.width
        else:
            self.rect.left += self.speed



    def shoot(self, bullet_img):
        bullet = Enemy_Bullet(bullet_img, self.rect.midbottom)
        self.bullets.add(bullet)

# class run_game():
#     def __init__(self, ):

class gameinit():
    def __init__(self, socket):
        self.socket = socket




    def run(self):
        pygame.init()


        # RED = pygame.Color('red')
        # GOLD = 251, 251, 0
        # WHITE = 255, 255, 255
        # GREEN = pygame.Color('green')

        size = widths, heights = 500, 700
        screen = pygame.display.set_mode(size)  # 还有FULLSCREEN
        pygame.display.set_caption('Universe Fighting Objects')

        plane = pygame.image.load(planeimage).convert_alpha()  # surface对象

        pygame.display.set_icon(plane)  # 图标
        width, height = plane.get_size()
        plane = pygame.transform.scale(plane, (width // 2, height // 2))
        plane_rect = plane.get_rect()




        #player
        player_rect = []
        player_rect.append(plane_rect)
        player_init_position = [widths//2-50, heights-100]
        player = Player(plane, player_rect, player_init_position)

        #enemy
        enemy = pygame.image.load(planeimage).convert_alpha()  # surface对象
        enemy = pygame.transform.scale(enemy, (width // 2, height // 2))
        enemy = pygame.transform.flip(enemy, False, True)
        enemyrect = enemy.get_rect()
        enemy_rect = []
        enemy_rect.append(enemyrect)
        enemy_init_position = [widths//2-50, 100]
        enemy = Enemy(enemy, enemy_rect, enemy_init_position)


        bullet_img = pygame.image.load(bulletimage)
        bullet_rect = bullet_img.get_rect()
        # bullet_rect = pygame.Rect(10, 10, 10, 10)
        # bullet_img = plane.subsurface(bullet_rect)

        pygame.mixer.init()
        pygame.mixer.music.load(musicpath)
        pygame.mixer.music.play(-1)

        framerate = 30
        fclock = pygame.time.Clock()
        running = True
        shoot_frequency = 0
        position_frequency = 0



        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # mysend(self.socket, json.dumps({'action':'play', 'position': [0,0], 'state': False}))

                    sys.exit()


        #old moving function

            # if not right:
            #     enemy.moveLeft()
            # else:
            #     enemy.moveRight()
            # if enemy.rect.left == 0:
            #     right = True
            # elif enemy.rect.right == widths:
            #     right = False

            if not player.is_hit:
                if shoot_frequency % 15 == 0:
                    player.shoot(bullet_img)
                shoot_frequency += 1
                if shoot_frequency >= 15:
                    shoot_frequency = 0


            if not enemy.is_hit:
                if shoot_frequency % 15 == 0:
                    enemy.shoot(bullet_img)
                shoot_frequency += 1
                if shoot_frequency >= 15:
                    shoot_frequency = 0




            key_pressed = pygame.key.get_pressed()
            #
            if key_pressed[pygame.K_UP] or key_pressed[pygame.K_UP]:
                player.moveUp()
            if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                player.moveDown()
            if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                player.moveLeft()
            if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                player.moveRight()

            for bullet in player.bullets:
                # 以固定速度移动子弹
                bullet.move()
                # 移动出屏幕后删除子弹
                if bullet.rect.bottom < 0:
                    player.bullets.remove(bullet)
                if pygame.sprite.collide_rect(bullet, enemy):
                    enemy.life -= 1

            for bullet in enemy.bullets:
                bullet.move()
                if bullet.rect.bottom < 0:
                    player.bullets.remove(bullet)
                if pygame.sprite.collide_rect(bullet, player):
                    player.life -= 1

            screen.fill((0, 0, 0))

            if player.life <= 0:
                player.is_hit = True
            enemy.is_hit = True if enemy.life < 0 else False
            if not player.is_hit:
                screen.blit(player.image[0], player.rect)
            if not enemy.is_hit:
                screen.blit(enemy.image[0], enemy.rect)

            player.bullets.draw(screen)
            enemy.bullets.draw(screen)

            if position_frequency % 30 == 0:
                # send the player's position to the server!-----------------------------------------

                # msg_2_server = {'action': 'play', 'position': player.rect.topleft, 'state': True}
                msg_2_server = {'action': 'play', 'position': player.rect.topleft}

                mysend(self.socket, json.dumps(msg_2_server))
                enemy.reassign_position(self.socket)
            position_frequency += 1
            if position_frequency >= 30:
                position_frequency = 0

            # if not json.loads(myrecv(self.socket))['state']:
            #     sys.exit()

            #refresh the screen
            pygame.display.update()
            fclock.tick(framerate)

if __name__ == '__main__':
    gameinit.run()
