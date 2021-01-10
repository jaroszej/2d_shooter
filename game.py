import pygame
import random

"""
CLASSES
"""
class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.bulletVelocity = 10 * facing

    def draw(self, screen):
        # circle bullet
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 2)


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 7
        self.isJump = False
        self.left = False
        self.right = False
        self.jumpCount = 10
        self.walkCount = 0
        self.hitbox = (self.x + 15, self.y + 12, 32, 50)

    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
                 pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
                 pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
                pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
    char = pygame.image.load('standing.png')

    # draw sprites
    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.left:
            screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            screen.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            screen.blit(self.char, (self.x, self.y))

        self.hitbox = (self.x + 15, self.y + 12, 32, 50)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


class Enemy(object):
    def __init__(self, x, y, width, height, end, health):
        self.health = health
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.velocity = 5
        self.hitbox = (self.x + 13, self.y + 3, 50, 55)

    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png')]

    # draw sprites
    def draw(self, screen):
        self.move()
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.velocity > 0:
            screen.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        # moving right (adding to velocity)
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.walkCount = 0
        # moving right (losing velocity)
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.walkCount = 0

        self.hitbox = (self.x + 12, self.y + 3, 50, 55)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def take_damage(self):
        quips = ["AARGH!", "OUCH!", "OOF!"]
        print(quips[random.randint(0, 2)])
        self.health -= 1
        if self.health < 1:
            print("Goblin slain!")

    #      self.death()
    #      self.respawn(rand.randint(300,1000))

    def death(self):
        # TODO
        # death animation and delete enemy
        # this may cause error, handle exception until respawn?

        # deletes enemy instance
        del self

    def respawn(self, delay):
        # TODO
        # spawn new enemy after /delay/ ms
        self.delay = delay
        pygame.time.set_timer(self.new_enemy, delay, True)

    # spawn new enemy with health between 10 and 50 hp in a random x location between 30 and 200
    # TODO: make x: 30 to x: 200 be goblin village in bg
    def new_enemy(self):
        goblin = Enemy(random.randint(30, 200), 407, 64, 64, 800, random.randint(10, 50))

"""
SETUP
"""

pygame.init()

# create screen, set size
windowWidth = 850
windowHeight = 480
screen = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption("2D PyShooter")

clock = pygame.time.Clock()

# globals
man = Player(400, 400, 64, 64)
goblin = Enemy(30, 407, 64, 64, 800, 10)
shooting = 0
bullets = []

"""
FUNCTIONS
"""

def refresh_game_window():
    # background img
    bg = pygame.image.load('bg.jpg')
    # draw background
    screen.blit(bg, (0, 0))
    man.draw(screen)
    goblin.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    # update screen
    pygame.display.update()


# MAIN
run = True
while run:
    # framerate
    clock.tick(27)

    # gets list of events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # read keyboard presses
    keys = pygame.key.get_pressed()

    # projectiles
    for bullet in bullets:
        # if bullet is within enemy hitbox y coords
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[
            1]:
            # if bullet is within enemy hitbox x coords
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                    goblin.hitbox[2]:
                # enemy takes damage and bullet delete
                goblin.take_damage()
                bullets.pop(bullets.index(bullet))

        if bullet.x < windowWidth and bullet.x > 0:
            bullet.x += bullet.bulletVelocity
        else:
            bullets.pop(bullets.index(bullet))

    # fire projectile
    # fire rate limiter
    if shooting > 0:
        shooting += 1
    if shooting > 4:
        shooting = 0
    # max 8 on screen
    if keys[pygame.K_LEFT] and shooting == 0:
        facing = -1
        if len(bullets) < 7:
            bullets.append(
                Projectile((round(man.x + man.width // 2)), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
            shooting = 1
    if keys[pygame.K_RIGHT] and shooting == 0:
        facing = 1
        if len(bullets) < 7:
            bullets.append(
                Projectile((round(man.x + man.width // 2)), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
            shooting = 1

    # move controls
    if keys[pygame.K_a] and man.x > man.velocity:
        man.x -= man.velocity
        man.left = True
        man.right = False
    elif keys[pygame.K_d] and man.x < (windowWidth - (man.width + 5)):
        man.x += man.velocity
        man.left = False
        man.right = True
    else:
        man.left = False
        man.right = False
        man.walkCount = 0

    # jump
    if not man.isJump:
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                # initiate gravity at peak of jump :)
                neg = -1
            # quadratic movement
            man.y -= (man.jumpCount ** 2) * 0.35 * neg
            man.jumpCount -= 1
        # done jumping
        else:
            man.isJump = False
            man.jumpCount = 10

    refresh_game_window()

# close app
pygame.quit()
