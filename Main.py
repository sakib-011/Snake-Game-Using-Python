import pygame as pg
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROND_COLOR = (80, 168, 50)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pg.image.load("Resource/apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pg.display.flip()


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.back_ground_music()
        self.surface = pg.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def bg (self):
        b_g = pg.image.load("Resource/background.jpg").convert()
        self.surface.blit(b_g,(0,0))

    def draw_game_over(self):
        pg.mixer.music.pause()
        self.bg()
        font = pg.font.SysFont("arial",50)
        Score = font.render(f"Your Score : {self.snake.length-1}", True, (255,255,255))
        Game_over = font.render(f"GAME OVER", True, (255,255,255))
        Again_play = font.render("If You Want To Play Again prease Enter", True, (255,255,255))
        self.surface.blit(Again_play, (150,410))
        self.surface.blit(Game_over, (350,290))
        self.surface.blit(Score,(350,350))
        pg.display.flip()

    def play_sound_funtion(self,sound):
        sound1 = pg.mixer.Sound(sound)
        pg.mixer.Sound.play(sound1)

    def back_ground_music(self):
        pg.mixer.music.load("Resource/bg_music_1.mp3")
        pg.mixer.music.play(-1,0)

    def display_score(self):
        font = pg.font.SysFont("arial", 30)
        score = font.render(f"Score : {self.snake.length-1}", True, (250, 250, 250))
        self.surface.blit(score, (850, 10))

    def play(self):
        self.bg()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pg.display.flip()

        if self.is_collison(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y) :
            self.play_sound_funtion("Resource/ding.mp3")
            self.snake.increase_length()
            self.apple.move()

        # colaid with body :

        for i in range(2, self.snake.length, 1):
            if self.is_collison(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound_funtion("Resource/crash.mp3")
                time.sleep(0.5)
                raise("Game Over")


        if self.is_collison_with_wall(self.snake.x[0],self.snake.y[0]):
            self.play_sound_funtion("Resource/crash.mp3")
            time.sleep(0.5)
            raise ("Game Over")


        if self.snake.x[0]>=999 or self.snake.x[0]<=0:
            if self.snake.x[0]>=999:
                for i in range(0,self.snake.length,1):
                    self.snake.x[i] = 0
                    break
            elif self.snake.x[0]<=0:
                for i in range(0, self.snake.length, 1):
                    self.snake.x[0] = 1000
                    break


    def is_collison_with_wall(self,x1,y1):
        if y1<=0 or y1>=799: return True
        return False

    def is_collison(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def run(self):

        running = True
        pause = False
        while running:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pg.mixer.music.unpause()
                        pause = False
                        self.__init__()

                    if not pause :
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False


            try :
                if not pause:
                    self.play()
            except Exception as e:
                self.draw_game_over()
                pause = True
            time.sleep(0.2)


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pg.image.load("Resource/image.jpg").convert()
        self.length = length
        self.x = [SIZE]
        self.y = [SIZE]
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-10)
        self.y.append(-10)

    def draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pg.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        # Iterate from the tail end up to the second segment (index 1)
        # Each segment takes the position of the segment in front of it.
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Then, update the head's position based on direction
        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()