import pygame
import os

# pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH = 1100
HEIGHT = 700
FPS = 75
velocity = 5
bullete_velocity=3
SHIP_WIDTH = 55
SHIP_HEIGHT = 40

clock = pygame.time.Clock()
font=pygame.font.SysFont('comicsans',40)
WINNER_FONT=pygame.font.SysFont('comicsans',100)

BLACK = (0, 0, 0)
YELLOW=(255,255,0)
RED=(255,0,0)
WHITE=(255,255,255)

RED_HIT_EVENT=pygame.USEREVENT+1
RED_HIT=pygame.event.Event(RED_HIT_EVENT,message="red got hit")

YELLOW_HIT_EVENT=pygame.USEREVENT+2
YELLOW_HIT=pygame.event.Event(YELLOW_HIT_EVENT,message="yellow got hit")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first game")

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)),
                                           90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270)

BACKGOUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

shoot=pygame.mixer.Sound("Assets/Gun+Silencer.mp3")

hit=pygame.mixer.Sound("Assets/Grenade+1.mp3")


def draw(red, yellow,red_bulletes,yellow_bulletes,red_health,yellow_health):
    WIN.blit(BACKGOUND, (0, 0))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(red_health,(BORDER.x+BORDER.width+5,10))
    WIN.blit(yellow_health,(BORDER.x-yellow_health.get_width()-5,10))
    for bullete in yellow_bulletes:
        pygame.draw.rect(WIN,YELLOW,bullete)
        if bullete.colliderect(red):
            pygame.event.post(RED_HIT)
            yellow_bulletes.remove(bullete)
        elif bullete.x>=WIDTH:
            yellow_bulletes.remove(bullete)
    for bullete in red_bulletes:
        pygame.draw.rect(WIN,RED,bullete)
        if bullete.colliderect(yellow):
            pygame.event.post(YELLOW_HIT)
            red_bulletes.remove(bullete)
        elif bullete.x<=0:
            red_bulletes.remove(bullete)
    pygame.display.update()

def wins(text):

    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()


def MOVE_YELLOW(KEY_PRESSED, yellow):
    if KEY_PRESSED[pygame.K_a] and yellow.x - velocity >= 0:  # LEFT
        yellow.x -= velocity
    if KEY_PRESSED[pygame.K_w] and yellow.y - velocity >= 0:  # UP
        yellow.y -= velocity
    if KEY_PRESSED[pygame.K_d] and yellow.x + yellow.width + velocity <= BORDER.x:  # RIGHT
        yellow.x += velocity
    if KEY_PRESSED[pygame.K_s] and yellow.y + velocity + yellow.height <= HEIGHT:  # DOWN
        yellow.y += velocity


def MOVE_RED(KEY_PRESSED, red):
    if KEY_PRESSED[pygame.K_LEFT] and red.x - velocity >= BORDER.x + BORDER.width:  # LEFT
        red.x -= velocity
    if KEY_PRESSED[pygame.K_UP] and red.y - velocity >= 0:  # UP
        red.y -= velocity
    if KEY_PRESSED[pygame.K_RIGHT] and red.x + red.width + velocity <= WIDTH:  # RIGHT
        red.x += velocity
    if KEY_PRESSED[pygame.K_DOWN] and red.y + red.height + velocity <= HEIGHT:  # DOWN
        red.y += velocity

def MOVE_RED_BULLETE(red_bullete):
    for bullete in red_bullete:
        bullete.x-=bullete_velocity

def MOVE_YELLOW_BULLETE(yellow_bullete):
    for bullete in yellow_bullete:
        bullete.x+=bullete_velocity

def main():
    yellow = pygame.Rect(300, 300, SHIP_HEIGHT, SHIP_WIDTH)
    red = pygame.Rect(600, 300, SHIP_HEIGHT, SHIP_WIDTH)
    yellow_bullete=[]
    red_bullete=[]
    RED_HEALTH=10
    YELLOW_HEALTH=10
    WINNER_TEXT=""
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullete)<3:
                    bullete=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,5,5)
                    yellow_bullete.append(bullete)
                    shoot.play()
                if event.key == pygame.K_RCTRL and len(red_bullete)<3:
                    bullete = pygame.Rect(red.x, red.y + red.height // 2 - 1, 5, 5)
                    red_bullete.append(bullete)
                    shoot.play()
            if event.type==RED_HIT_EVENT:
                RED_HEALTH-=1
                # print(event.message)
                hit.play()

            if event.type==YELLOW_HIT_EVENT:
                YELLOW_HEALTH-=1
                hit.play()

        if YELLOW_HEALTH<=0:
            WINNER_TEXT="Red Wins!"
        elif RED_HEALTH<=0:
            WINNER_TEXT="Yellow WIns!"
        text=WINNER_FONT.render(WINNER_TEXT,True,WHITE)

        KEY_PRESSED = pygame.key.get_pressed()
        MOVE_YELLOW(KEY_PRESSED, yellow)
        MOVE_RED(KEY_PRESSED, red)
        MOVE_YELLOW_BULLETE(yellow_bullete)
        MOVE_RED_BULLETE(red_bullete)
        YELLOW_TEXT=font.render("HEALTH: "+str(YELLOW_HEALTH),True,WHITE)
        RED_TEXT=font.render("HEALTH: "+str( RED_HEALTH),True,WHITE)
        draw(red, yellow,red_bullete,yellow_bullete,RED_TEXT,YELLOW_TEXT)
        if WINNER_TEXT != "":
            wins(text)
            break

    pygame.quit()


if __name__ == '__main__':
    main()
