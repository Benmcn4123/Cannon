import sys, pygame
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()

pygame.display.set_caption("game")
win = pygame.display.set_mode((1500, 700), 0, 32)

moving_left = False
moving_right = False

player = pygame.Rect(250, 250, 20, 30)

# declare colours
yellow = pygame.Color("#ffAB5E")
orange = pygame.Color("#ff7844")
red = pygame.Color("#a64942")
blue = pygame.Color("#23425f")

font = pygame.font.SysFont(None, 30)

map = [
".................o....................",
"................................oo....",
"...................#####..............",
"......................................",
".........########.....vvv.............",
".......v..............###........v....",
"......##......v...............####....",
"........o.....##.........#.........o..",
"......####...............###..........",
"..##....##............................",
"#..................vvvv...v...######..",
"##.....vvvv.v......###################",
"######################################",
"######################################",
"######################################",
]

SPEED = 5
y_velocity = 0
x_velocity = 0
BULLET_SPEED = 10


cam_x = 250
coyote_timer = 0
dir = "right"
bullets = []
looking_up = False
tile_width = 40

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

            self.y_velocity += 1
            if self.y_velocity > 15:
                self.y_velocity = 15
    def draw(self):
        rect = self.rect
        pygame.draw.rect(win, red, (rect.x - cam_x, rect.y, rect.width, rect.height))
        pygame.draw.rect(win, blue, (rect.x - cam_x + 5, rect.y + 10, 5, 5))
        pygame.draw.rect(win, blue, (rect.right - cam_x - 10, rect.y + 10, 5, 5))

def on_ground(col_rect, col):
    for tile in col:
        if col_rect.colliderect(tile):
            return True
    return False

def create_bullet():
    bullet = {"size": 12, "x": player.left + 10, "y": player.top + 11, "x_velocity": 0, "y_velocity": 0}
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

while True:
    delta_time = clock.get_time() / 20
    win.fill(yellow) # cls

    tiles = []
    foreground = []



    for y in range(0, len(map)):
        for x in range(0, len(map[y])):
            if map[y][x] == "#":
                tile_width = 40
                rect = pygame.Rect(x * tile_width, y * tile_width, tile_width, tile_width)
                pygame.draw.rect(win, blue, (rect.x - cam_x, rect.y, rect.width, rect.height))
                tiles.append(rect)
            elif map[y][x] == "v":
                foreground.append(((x * tile_width - cam_x, y * tile_width + tile_width), (x * tile_width - cam_x + tile_width - 1, y * tile_width + tile_width), (x * tile_width - cam_x + tile_width / 2, y * tile_width + tile_width / 2)))

    test_rect = pygame.Rect(player.left, player.top, 20, 31)
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
                y_velocity = -15
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
        x_velocity = SPEED# * (clock.get_time() / 10)
    if moving_left:
        x_velocity = -SPEED # * (clock.get_time() / 10)

    player.right += round(x_velocity) * delta_time

    for tile in tiles:
        if player.colliderect(tile):
            if x_velocity > 0:
                player.right = tile.left
            if x_velocity < 0:
                player.left = tile.right
            x_velocity = 0




    cam_target = player.centerx - win.get_size()[0] / 2
    cam_x  = cam_target #+= (cam_target - cam_x) * 0.1

    player.top += y_velocity * delta_time

    for tile in tiles:
        if player.colliderect(tile):
            if y_velocity > 0:
                player.bottom = tile.top
            else:
                player.top = tile.bottom
            y_velocity = 0


    y_velocity += 1 * delta_time

    if y_velocity > 15:
        y_velocity = 15

    pygame.draw.rect(win, red, (player.x - cam_x, player.y, player.width, player.height))
    if dir == "right" and not looking_up:
        pygame.draw.rect(win, blue, (player.left + 7 - cam_x, player.top + 5, 22, 12))
        pygame.draw.rect(win, blue, (player.left + 2 - cam_x, player.top + 2, 4, 4))
    elif dir == "left" and not looking_up:
        pygame.draw.rect(win, blue, (player.left - 9 - cam_x, player.top + 5, 22, 12))
        pygame.draw.rect(win, blue, (player.right - 6 - cam_x, player.top + 2, 4, 4))
    elif looking_up:
        pygame.draw.rect(win, blue, (player.left + 2 - cam_x, player.top - 18, 14, 18))
        pygame.draw.rect(win, blue, (player.right - 6 - cam_x, player.top + 2, 4, 4))

    new_bullets = bullets.copy()
    for bullet in bullets:
        bullet["x"] += bullet["x_velocity"] * delta_time
        bullet["y"] += bullet["y_velocity"] * delta_time
        bullet_rect = pygame.Rect(bullet["x"], bullet["y"], bullet["size"], bullet["size"])

        if bullet_rect.left < 0 + cam_x or bullet_rect.right > win.get_size()[0] + cam_x:
            new_bullets.remove(bullet)
            break

        for tile in tiles:
            if bullet_rect.colliderect(tile):
                new_bullets.remove(bullet)
                break


        pygame.draw.circle(win, red, (bullet_rect.x - cam_x, bullet_rect.y), bullet_rect.width/2, 0)

    bullets = new_bullets.copy()

    for enemy in enemies:
        enemy.update()
        enemy.draw()

    for foliage in foreground:
        pygame.draw.polygon(win, blue, foliage)

    text = font.render(str(clock.get_fps()), True, (0, 0, 0), (0, 0, 1))
    text.set_colorkey((0, 0, 1))
    text_rect = text.get_rect()
    text_rect
    win.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)
