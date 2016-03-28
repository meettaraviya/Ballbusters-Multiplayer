import sys, pygame, math

pygame.init()


class Ball:
    def __init__(self, a, center):
        self.image = pygame.image.load(a)
        self.rect = self.image.get_rect()
        self.rect.x = center[0]
        self.rect.y = center[1]
        self.prsd = [False, False, False, False]
        self.speed = [0, 0]
        self.acc = [0, 0]

    def update(self, key, keys):
        self.prsd = [key[keys[0]], key[keys[1]], key[keys[2]], key[keys[3]]]
        if key[pygame.K_q]: sys.exit()
        self.acc = [0, 0]
        if self.prsd[0]: self.acc[1] -= 1
        if self.prsd[1]: self.acc[0] -= 1
        if self.prsd[2]: self.acc[1] += 1
        if self.prsd[3]: self.acc[0] += 1
        if self.acc[0] != 0 and self.acc[1] != 0:
            self.acc[0] /= 1.414
            self.acc[1] /= 1.414

    def display(self, screen):
        screen_w = screen.get_width()
        screen_h = screen.get_height()
        self.speed[0] = 0.99 * self.speed[0] + 0.03 * self.acc[0]
        self.speed[1] = 0.99 * self.speed[1] + 0.03 * self.acc[1]
        if self.speed[0] != 0 and self.speed[1] != 0:
            self.rect = self.rect.move(2.828 * self.speed[0], 2.828 * self.speed[1])
        else:
            self.rect = self.rect.move(4 * self.speed[0], 4 * self.speed[1])
        # if self.rect.left < 0 or self.rect.right > screen_w or self.rect.top < 0 or self.rect.bottom > screen_h:
        #     if self.rect.right > screen_w and self.rect.left < screen_w: screen.blit(self.image,
        #                                                                              [self.rect.left - screen_w,
        #                                                                               self.rect.top])
        #     if self.rect.left > screen_w: self.rect = self.rect.move(-screen_w, 0)
        #     if self.rect.left < 0 < self.rect.right: screen.blit(self.image,
        #                                                          [self.rect.left + screen_w, self.rect.top])
        #     if self.rect.right < 0: self.rect = self.rect.move(screen_w, 0)
        #     if self.rect.bottom > screen_h > self.rect.top: screen.blit(self.image, [self.rect.left,
        #                                                                              self.rect.top - screen_h])
        #     if self.rect.top > screen_h: self.rect = self.rect.move(0, -screen_h)
        #     if self.rect.top < 0 < self.rect.bottom: screen.blit(self.image,
        #                                                          [self.rect.left, self.rect.top + screen_h])
        #     if self.rect.bottom < 0: self.rect = self.rect.move(0, screen_h)
        screen.blit(self.image, self.rect)

    def dist(self, b2):
        return math.sqrt((self.rect.x - b2.rect.x) * (self.rect.x - b2.rect.x) + (self.rect.y - b2.rect.y) * (
            self.rect.y - b2.rect.y))

def arenacolor(b, g):
    if abs(g-b)<6:
        return (0,25*(g-b+5), 25*(b-g+5))
    elif g>b:
        return (0, 255, 0)
    else:
        return (0, 0, 255)

wkeys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
ukeys = [pygame.K_u, pygame.K_h, pygame.K_j, pygame.K_k]
upkeys = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
n8keys = [pygame.K_KP8, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6]

winsound = pygame.mixer.Sound('victory.wav')
bgmusic = pygame.mixer.Sound('bg.wav')
collidesound = pygame.mixer.Sound('collision.wav')
bgmusic.play(-1)
screen_h = 768
screen_w = 1366
screen = pygame.display.set_mode([screen_w, screen_h], pygame.FULLSCREEN)
center = [400, screen_h / 2]
radius = 380
pradius = 20
# bg = pygame.image.load('bg.png')
ball1 = Ball('ballblue.png', [center[0] - 300 - 32, center[1]])
ball2 = Ball('ballgreen.png', [center[0] + 300 - 32, center[1]])
ball1.display(screen)
ball2.display(screen)
scoreg = 0
scoreb = 0
pygame.draw.circle(screen, arenacolor(scoreg,scoreb), center, radius, 0)
pygame.display.flip()
pygame.draw.circle(screen, [0, 255, 0], [1000, 250], 100, 0)
pygame.draw.circle(screen, [0, 0, 255], [1000, 518], 100, 0)

pygame.font.init()
l1 = pygame.font.SysFont("comicsansms", 50)

n=0



while True:
    screen.fill([0, 0, 0])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            key = pygame.key.get_pressed()

            ball1.update(key, wkeys)
            ball2.update(key, upkeys)
    mdx = ball1.dist(ball2)
    if mdx < (ball1.rect.width + ball2.rect.width) / 2:
        pygame.draw.circle(screen, (255,0,0), center, radius, 0)
        screen.blit(ball2.image, ball2.rect)
        screen.blit(ball1.image, ball1.rect)
        pygame.display.flip()
        pygame.time.delay(20)
        collidesound.play(0)
        dx = [ball1.rect.x - ball2.rect.x, ball1.rect.y - ball2.rect.y]
        dv = (dx[0] * (ball1.speed[0] - ball2.speed[0]) + dx[1] * (ball1.speed[1] - ball2.speed[1])) / mdx
        ball2.speed[0] += dv * dx[0] / mdx
        ball2.speed[1] += dv * dx[1] / mdx
        ball1.speed[0] -= dv * dx[0] / mdx
        ball1.speed[1] -= dv * dx[1] / mdx
        pygame.draw.circle(screen, arenacolor(scoreg,scoreb), center, radius, 0)
        screen.blit(ball2.image, ball2.rect)
        screen.blit(ball1.image, ball1.rect)
        pygame.display.flip()
    r1 = math.sqrt(
            (ball1.rect.x - center[0] + ball1.rect.width / 2) * (ball1.rect.x - center[0] + ball1.rect.width / 2) + (
                ball1.rect.y + ball1.rect.height / 2 - center[1]) * (ball1.rect.y + ball1.rect.height / 2 - center[1]))
    r2 = math.sqrt(
            (ball2.rect.x - center[0] + ball2.rect.width / 2) * (ball2.rect.x - center[0] + ball2.rect.width / 2) + (
                ball2.rect.y + ball2.rect.height / 2 - center[1]) * (ball2.rect.y + ball2.rect.height / 2 - center[1]))
    if r2>radius>r1:
        scoreg += 1
        winsound.play(0)
        for i in range(8):
            pygame.draw.circle(screen, [0, 0, 0], [1000, 518], 100, 0)
            b = l1.size(str(scoreg))
            screen.fill([0,0,0])
            screen.blit(l1.render(str(scoreg), True, (255, 255, 255)), (1000 - b[0] / 2, 518 - b[1] / 2))
            pygame.display.flip()
            pygame.time.delay(100)
            pygame.draw.circle(screen, [0, 0, 128], [1000, 518], 100, 0)
            b = l1.size(str(scoreg))
            screen.blit(l1.render(str(scoreg), True, (255, 255, 255)), (1000 - b[0] / 2, 518 - b[1] / 2))
            pygame.display.flip()
            pygame.time.delay(100)
        ball1 = Ball('ballblue.png', [center[0] - 300 - 32, center[1]])
        ball2 = Ball('ballgreen.png', [center[0] + 300 - 32, center[1]])
    elif r2 < radius and r1 > radius:
        scoreb += 1
        winsound.play(0)
        for i in range(8):
            pygame.draw.circle(screen, [0, 0, 0], [1000, 250], 100, 0)
            b = l1.size(str(scoreb))
            screen.fill([0,0,0])
            screen.blit(l1.render(str(scoreb), True, (255, 255, 255)), (1000 - b[0] / 2, 250 - b[1] / 2))
            pygame.display.flip()
            pygame.time.delay(100)
            pygame.draw.circle(screen, [0, 128, 0], [1000, 250], 100, 0)
            b = l1.size(str(scoreb))
            screen.blit(l1.render(str(scoreb), True, (255, 255, 255)), (1000 - b[0] / 2, 250 - b[1] / 2))
            pygame.display.flip()
            pygame.time.delay(100)
        ball1 = Ball('ballblue.png', [center[0] - 300 - 32, center[1]])
        ball2 = Ball('ballgreen.png', [center[0] + 300 - 32, center[1]])
    # elif 0<n%1500<800 and r2<pradius:
    #     v = ball2.speed
    #     mv = math.sqrt(v[0]*v[0]+v[1]*v[1])
    #     ball2.rect.centerx=-v[0]*pradius/mv
    #     ball2.rect.centery=-v[1]*pradius/mv
    # elif 0<n%1500<800 and r1<pradius:
    #     v = ball2.speed
    #     mv = math.sqrt(v[0]*v[0]+v[1]*v[1])
    #     ball2.rect.centerx=-v[0]*pradius/mv
    #     ball2.rect.centery=-v[1]*pradius/mv

    pygame.draw.circle(screen, arenacolor(scoreg,scoreb), center, radius, 0)

    pygame.draw.circle(screen, [0, 0, 128], [1000, 518], 100, 0)
    pygame.draw.circle(screen, [0, 128, 0], [1000, 250], 100, 0)
    a = l1.size(str(scoreg))
    b = l1.size(str(scoreb))
    screen.blit(l1.render(str(scoreb), True, (255, 255, 255)), (1000 - a[0] / 2, 250 - a[1] / 2))
    screen.blit(l1.render(str(scoreg), True, (255, 255, 255)), (1000 - b[0] / 2, 518 - b[1] / 2))
    ball1.display(screen)
    ball2.display(screen)
    pygame.display.flip()
    if(scoreg==10 or scoreb==10):
        break
    n += 1

pygame.draw.circle(screen, arenacolor(scoreg,scoreb), center, radius, 0)
if(scoreg==10):
    a = str("BLUE WINS")
else:
    a = str("GREEN WINS")
b = l1.size(a)
screen.blit(l1.render(a, True, (255, 255, 255)), [center[0]-b[0]/2, center[1]-b[1]/2])
pygame.display.flip()
winsound.play(1)
pygame.time.delay(3000)
