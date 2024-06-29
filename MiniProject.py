import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

wid=770
hei=740

screen = pygame.display.set_mode((wid,hei))
pygame.display.set_caption('Flappy Bird')

font = pygame.font.SysFont('Bauhaus 93',60)
white = (149,53,83)

#var
g_scroll = 0
s_speed = 4
fly = False
g_over = False
p_gap = 150
p_fre = 1800 #millisec
last_pipe = pygame.time.get_ticks() - p_fre
score = 0
p_pass = False

#img
bg = pygame.image.load('img/bg.jpg')
ground = pygame.image.load('img/ground.png')
start = pygame.image.load('img/p_again.png')

def text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))
    
def reset():
    p_group.empty()
    flappy.rect.x = 80
    flappy.rect.y = int(hei/2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/bird.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
    def update(self):
        #gravity
        if fly == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 600:
                self.rect.y += int(self.vel)
        #jump
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -8
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
            
class pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #1 is top, -1 is bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - int(p_gap/2)]
        if position == -1:
            self.rect.topleft = [x,y+int(p_gap/2)]
    
    def update(self):
        self.rect.x -= s_speed
        if self.rect.right < 0:
            self.kill()
            
            
class btn():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        
    def draw(self):
        action = False
        
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
        return action
        
b_group = pygame.sprite.Group()
p_group = pygame.sprite.Group()

flappy = Bird(80, int(hei/2))

b_group.add(flappy)

button = btn(wid//2 - 50,hei//2 - 100,start)

run = True
while run:
    
    clock.tick(fps)
    
    screen.blit(bg,(0,0))
    b_group.draw(screen)
    b_group.update()
    p_group.draw(screen)
    
    screen.blit(ground,(g_scroll,600))
    
    #score
    if len(p_group) > 0:
        if b_group.sprites()[0].rect.left > p_group.sprites()[0].rect.left\
            and b_group.sprites()[0].rect.right < p_group.sprites()[0].rect.right\
            and p_pass == False:
                p_pass = True
        if p_pass == True:
            if b_group.sprites()[0].rect.left > p_group.sprites()[0].rect.right:
                score += 1
                p_pass = False
                
    text(str(score), font, white, int(wid/2), 20)
    
    #pipe hit
    if pygame.sprite.groupcollide(b_group, p_group,False,False) or flappy.rect.top <0:
        g_over = True
        
        
    #game over
    if flappy.rect.bottom >= 600:
        g_over = True
        fly = False
    
    if g_over == False and fly== True:
        #generate pipe
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > p_fre:
            p_hei = random.randint(-100, 100)
            btm_pipe = pipe(wid, int(hei/2) + p_hei,-1)
            top_pipe = pipe(wid, int(hei/2)+ p_hei,1)
            p_group.add(btm_pipe)
            p_group.add(top_pipe)
            last_pipe = time_now
        
        
        #ground
        g_scroll -= s_speed
        if abs(g_scroll) >120:
            g_scroll = 0
            
        p_group.update()
    
    #reset
    if g_over == True:
        if button.draw() == True:
            g_over = False
            score = reset()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and fly == False and g_over == False:
            fly = True
    
    pygame.display.update()
    
pygame.quit()