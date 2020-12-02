import sys, pygame
from pygame.locals import *

#import images

player_anims = {
"idle":[pygame.image.load("images/art1.png"), pygame.image.load("images/art3.png")],
"run":[pygame.image.load("images/art1.png"), pygame.image.load("images/art2.png")],
"cannon_up_idle":[pygame.image.load("images/art4.png"), pygame.image.load("images/art6.png")],
"looking_up_run":[pygame.image.load("images/art4.png"), pygame.image.load("images/art5.png")],
"jump":[pygame.image.load("images/art2.png"), pygame.image.load("images/art2.png")],
"looking_up_jump":[pygame.image.load("images/art5.png"), pygame.image.load("images/art5.png")],
}

grass_tiles = {"default_grass":pygame.image.load("images/art8.png"), "top_grass":pygame.image.load("images/art9.png"), "top_grass_squashed":pygame.image.load("images/art10.png")}


clock = pygame.time.Clock()
pygame.init()

WIN_SIZE = (1000, 600)

pygame.display.set_caption("game")
win = pygame.display.set_mode((WIN_SIZE), 0, 32)

display = pygame.Surface((500, 300))

moving_left = False
moving_right = False

player = pygame.Rect(250, 0, 8, 15)

# declare colours
yellow = pygame.Color("#ffAB5E")
orange = pygame.Color("#ff7844")
red = pygame.Color("#a64942")
blue = pygame.Color("#23425f")

font = pygame.font.SysFont(None, 15)
bullet_image = pygame.image.load("images/art7.png")

map = [
"....v............o....................",
"...v#v.............vvvvv........oo....",
"..v###v............#####..............",
".v#####v.vvvvvvvv.....................",
".#######.########.....vvv.............",
"......vv..............###.....vvvv....",
"......##......vv.........v....####....",
"......vvvv....##.........#vv.......o..",
"..vv..####...............###..........",
"v.##....##.....................vvvvvv.",
"#v.................vvvvvvvvvvvv######v",
"##vvvvvvvvvvvvvvvvv###################",
"######################################",
"######################################",
"######################################",
]

SPEED = 3
y_velocity = 0
x_velocity = 0
BULLET_SPEED = 5
jump_height = 8

cam_x = 0
coyote_timer = 0
dir = "right"
bullets = []
looking_up = False
tile_width = 16

frame = 0
current_anim = "idle"
time_since_last_frame = 0
last_x = 0

class enemy:
    def __init__ (self, rect, type = "fodder"):
        self.type = type
        self.rect = rect
        self.y_velocity = 0
        self.x_velocity = 0
        enemies.append(self)
    def update(self):
        if self.type == "fodder":
            self.rect.top += self.y_velocity

            for tile in tiles:
                if self.rect.colliderect(tile):
                    if self.y_velocity > 0:
                        self.rect.bottom = tile.top
                    else:
                        self.rect.top = tile.bottom
                    self.y_velocity = 0

            self.y_velocity += 0.5
            if self.y_velocity > 15:
                self.y_velocity = 15
    def draw(self):
        rect = self.rect
        pygame.draw.rect(display, red, (rect.x - cam_x, rect.y, rect.width, rect.height))
        pygame.draw.rect(display, blue, (rect.x - cam_x + 5, rect.y + 10, 5, 5))
        pygame.draw.rect(display, blue, (rect.right - cam_x - 10, rect.y + 10, 5, 5))

def on_ground(col_rect, col):
    for tile in col:
        if col_rect.colliderect(tile):
            return True
    return False

def create_bullet():
    bullet = {"size": 6, "x": player.left + 4, "y": player.top + 1, "x_velocity": 0, "y_velocity": 0}
    if looking_up:
        vel = y_velocity
        if vel > 0 :
            vel = 0
        bullet["y_velocity"] = -BULLET_SPEED + vel
    elif dir == "right":
        bullet["x_velocity"] = BULLET_SPEED + x_velocity
    elif dir == "left":
        bullet["x_velocity"] = -BULLET_SPEED + x_velocity
    bullets.append(bullet)

enemies = []

for y in range(0, len(map)):
    for x in range(0, len(map[y])):
        if map[y][x] == "o":
            new_enemy = enemy(pygame.Rect(x * tile_width, y * tile_width, 40, 20))
            enemies.append(new_enemy)

tiles = []
foreground = []

for y in range(0, len(map)):
    for x in range(0, len(map[y])):
        if map[y][x] == "#":
            rect = pygame.Rect(x * tile_width, y * tile_width, tile_width, tile_width)
            tiles.append(rect)
        elif map[y][x] == "v":
            rect = pygame.Rect(x * tile_width, y * tile_width, tile_width, tile_width)
            foreground.append(rect)
        elif map[y][x] == "o":
            new_enemy = enemy(pygame.Rect(x * tile_width, y * tile_width, 40, 20))
            enemies.append(new_enemy)


while True:
    delta_time = clock.get_time() / 20
    display.fill(yellow) # cls

    test_rect = pygame.Rect(player.x, player.y, player.width, player.height + 1)
    grounded = on_ground(test_rect, tiles)

    if grounded:
        coyote_timer = 0
    else:
        coyote_timer += 1

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = True
                dir = "right"
            if event.key == K_LEFT or event.key == K_a:
                moving_left = True
                dir = "left"
            if event.key == K_x:
                create_bullet()
            if event.key == K_z and coyote_timer < 10:
                coyote_timer = 10
                y_velocity = -jump_height
            if event.key == K_w or event.key == K_UP:
                looking_up = True

        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = False
            if event.key == K_LEFT or event.key == K_a:
                moving_left = False
            if event.key == K_w or event.key == K_UP:
                looking_up = False

    x_velocity = 0
    if moving_right:
        x_velocity = SPEED
    if moving_left:
        x_velocity = -SPEED
    movement = round(x_velocity) * delta_time
    player.move_ip(movement, 0)

    for tile in tiles:
        if player.colliderect(tile):
            if x_velocity > 0:
                player.right = tile.left
            if x_velocity < 0:
                player.left = tile.right

    cam_target = player.centerx - display.get_size()[0] / 2
    cam_x += (cam_target - cam_x) * 0.1

    player.move_ip(0, y_velocity * delta_time)

    for tile in tiles:
        if player.colliderect(tile):
            if y_velocity > 0:
                player.bottom = tile.top
            else:
                player.top = tile.bottom
            y_velocity = 0


    y_velocity += 0.5 * delta_time

    if y_velocity > 15:
        y_velocity = 15

    for bullet in bullets[:]:
        bullet["x"] += bullet["x_velocity"] * delta_time
        bullet["y"] += bullet["y_velocity"] * delta_time
        bullet_rect = pygame.Rect(bullet["x"], bullet["y"], bullet["size"], bullet["size"])

        if bullet_rect.left < 0 + cam_x or bullet_rect.right > display.get_size()[0] + cam_x:
            bullets.remove(bullet)
            break

        for tile in tiles:
            if bullet_rect.colliderect(tile):
                bullets.remove(bullet)
                break


        display.blit(bullet_image, (bullet_rect.x - 5 - cam_x, bullet_rect.y-5, bullet_rect.width + 10, bullet_rect.height + 10))


    '''for enemy in enemies:
        enemy.update()
        enemy.draw()'''

    time_since_last_frame += clock.get_time()
    if time_since_last_frame >= 150:
        frame += 1
        if frame == len(player_anims[current_anim]):
            frame = 0
        time_since_last_frame = 0

    if looking_up:
        current_anim = "cannon_up_idle"
        if not grounded:
            current_anim = "looking_up_jump"
        elif moving_right or moving_left:
            current_anim = "looking_up_run"
    else:
        current_anim = "idle"
        if not grounded:
            current_anim = "jump"
        elif moving_right or moving_left:
            current_anim = "run"

    if dir == "right":
        display.blit(player_anims[current_anim][frame], (player.x - 4 - cam_x, player.y - 1, player.width, player.height))
    if dir == "left":
        display.blit(pygame.transform.flip(player_anims[current_anim][frame], True, False), (player.x - 4 - cam_x, player.y - 1, player.width, player.height))

    for tile in tiles:
        display.blit(grass_tiles["default_grass"], (tile.x - cam_x, tile.y, tile.width, tile.height))
    for foliage in foreground:
        if not foliage.colliderect(player):
            display.blit(grass_tiles["top_grass"], (foliage.x - cam_x, foliage.y, foliage.width, foliage.height))
        if foliage.colliderect(player):
            display.blit(grass_tiles["top_grass_squashed"], (foliage.x - cam_x, foliage.y, foliage.width, foliage.height))

    win.blit(pygame.transform.scale(display, WIN_SIZE), (0,0))

    last_x = player.x
    pygame.display.update()
    clock.tick(60)
