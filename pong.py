import pygame
from sys import exit
import random
class Pong(pygame.sprite.Sprite):
    def __init__(self, surface, colour, player, dimensions):
        super().__init__()
        self.image = surface
        self.image.fill(colour)
        self.colour = colour
        self.player = player
        self.dimensions = dimensions
        if self.player == 1:
            self.rect = self.image.get_rect(midleft=(0,int(dimensions[1]/2)))
        else:
            self.rect = self.image.get_rect(midright=(dimensions[0],int(dimensions[1]/2)))
    def movement(self):
        keys = keys = pygame.key.get_pressed()
        if self.player == 1:
            if keys[pygame.K_w]:
                self.rect.y -= 10
            elif keys[pygame.K_s]:
                self.rect.y += 10
        else:
            if keys[pygame.K_UP]:
                self.rect.y -= 10
            elif keys[pygame.K_DOWN]:
                self.rect.y += 10
    def check_limits(self):
        if self.rect.bottom >= self.dimensions[1]:
            self.rect.bottom = self.dimensions[1]
        elif self.rect.top < 0:
            self.rect.top = 0
    def update(self):
        self.movement()
        self.check_limits()

class Ball():
    def __init__(self, dimensions, r, colour, screen):
        super().__init__()
        self.r = r
        self.colour = colour
        self.screen = screen
        self.dimensions = dimensions
        self.pong_sound = pygame.mixer.Sound('Pong/sounds/pong_ricochet.mp3')
        self.pong_sound.set_volume(0.5)
        self.wall_sound = pygame.mixer.Sound('Pong/sounds/wall_ricochet.mp3')
        self.wall_sound.set_volume(0.5)
        self.goal_sound = pygame.mixer.Sound('Pong/sounds/goal.mp3')
        self.goal_sound.set_volume(0.5)
        self.initial_direction()
    
    def draw(self):
        self.rect = pygame.draw.circle(self.screen, self.colour, [self.x, self.y], self.r)

    
    def movement(self):
        self.x += round(self.x_multiplier*2*self.x_direction)
        self.y += round(self.y_multiplier*2*self.y_direction)
    
    def initial_direction(self):
        self.x = self.dimensions[0]//2
        self.y = self.dimensions[1]//2
        directions = (1,-1)
        self.x_multiplier = 1
        self.y_multiplier = random.randint(0,1)
        self.x_direction = directions[random.randint(0,1)]
        self.y_direction = directions[random.randint(0,1)]
    
    def reverse(self,object):
        if object == 'pong':
            self.x_direction *= -1
        else:
            self.y_direction *= -1
        if self.x_multiplier >= 12:
            self.multipler = 12
        else:
            self.x_multiplier += 0.4
            self.y_multiplier += 0.4

    def score(self, score_dictionary):
        if self.x > self.dimensions[0]:
            self.goal_sound.play()
            score_dictionary['Red'] = score_dictionary.get('Red') + 1
            self.initial_direction()
            self.colour = 'White'
        if self.x < 0:
            self.goal_sound.play()
            score_dictionary['Blue'] = score_dictionary.get('Blue') + 1
            self.initial_direction()
            self.colour = 'White'
        return score_dictionary

def initialise(dimensions):
    pygame.init()
    screen_dimensions = dimensions
    pong_width = 10
    pong_length = int(screen_dimensions[0]/4)
    screen = pygame.display.set_mode(screen_dimensions)
    pygame.display.set_caption('Pong')
    score_font = pygame.font.Font('Pong/font/ARCADE_N.TTF', 40)
    clock = pygame.time.Clock()
    players = pygame.sprite.Group()
    background = pygame.Surface(screen_dimensions)
    top_wall = pygame.draw.line(background, 'Black', (0,0), (screen_dimensions[0],0), 1)
    bottom_wall = pygame.draw.line(background, 'Black', (0,screen_dimensions[1]-1), (screen_dimensions[0],screen_dimensions[1]-1), 1)
    walls = (top_wall,bottom_wall)
    pong_red = pygame.Surface([pong_width,pong_length])
    pong_blue = pygame.Surface([pong_width,pong_length])
    player1 = Pong(pong_red, 'Red', 1, screen_dimensions)
    player2 = Pong(pong_blue, 'Blue', 2, screen_dimensions)
    players.add(player1, player2)
    ball = Ball(screen_dimensions, 10, 'White', screen)
    return screen, clock, background, walls, players, ball, score_font

def checkcollision(walls, players, ball):
    for player in players.sprites():
        if player.rect.colliderect(ball.rect):
            ball.reverse('pong')
            ball.colour = player.colour
            ball.pong_sound.play()
    for wall in walls:
        if wall.colliderect(ball.rect):
            ball.reverse('wall')
            ball.wall_sound.play()

def display_score(screen, score, score_font, dimensions):
    score_surf = score_font.render(f"{score['Red']} - {score['Blue']}", False,(64,64,64))
    score_rect = score_surf.get_rect(center = (dimensions[0]//2,50))
    screen.blit(score_surf, score_rect)

def check_score(score, game_active):
    if abs(score['Blue']-score['Red']) > 1 or max(score.values()) == 3:
        maxkey = max(score, key=score.get)
        win_msg = f"{maxkey} wins"
        game_active = 2
        return win_msg, game_active
    else:
        return None, game_active

def display_message(screen, score_font, win_msg, dimensions):
    message_surf = score_font.render(win_msg, False,(64,64,64))
    message_rect = message_surf.get_rect(center = (dimensions[0]//2,dimensions[1]//2))
    screen.blit(message_surf, message_rect)

def run():
    screen, clock, background, walls, players, ball, score_font = initialise((800,800))
    score = {'Red':0, 'Blue':0}
    title_font = pygame.font.Font('Pong/font/ARCADE_N.TTF', 40)
    game_active = 0
    while True:
        if game_active == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            game_active = 1
            screen.blit(background,(0,0))
            display_message(screen, title_font, f'Pong', ball.dimensions)
            pygame.display.update()
            clock.tick(10)
        elif game_active==1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            players.clear(screen,background)
            screen.blit(background,(0,0))
            players.draw(screen)
            ball.draw()
            checkcollision(walls, players, ball)
            ball.movement()
            players.update()
            score = ball.score(score)
            display_score(screen, score, score_font, ball.dimensions)
            win_msg, game_active = check_score(score, game_active)
            pygame.display.update()
            clock.tick(120)

        elif game_active == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        run()
            players.clear(screen,background)
            screen.blit(background,(0,0))
            display_message(screen, score_font, win_msg, ball.dimensions)
            pygame.display.update()
            clock.tick(10)
if __name__  == "__main__":
    run()       