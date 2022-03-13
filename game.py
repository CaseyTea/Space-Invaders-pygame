import pygame as pg
from landing_page import LandingPage
from sys import exit
import game_functions as gf
from time import sleep
from stats import Stats
from scoreboard import Scoreboard
from laser import Lasers
from ship import Ship
from alien import AlienFleet
from settings import Settings
from sound import Sound
import barrier


class Game:
    RED = (255, 0, 0)


    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.stats = Stats(game=self)
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color

        self.bg_image = pg.transform.scale(pg.image.load('images/background-black.bmp'),
                                           (self.settings.screen_width, self.settings.screen_height))

        self.sound = Sound()
        self.sb = Scoreboard(game=self)
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        self.lasers = Lasers(game=self, owner=self.ship)                  # for ship lasers
        self.alien_lasers = Lasers(game=self, owner=self.alien_fleet)   # for alien lasers
        self.ship.set_alien_fleet(self.alien_fleet)
        self.ship.set_lasers(self.lasers)

        self.shape = barrier.shape
        self.block_size = 6
        self.blocks = pg.sprite.Group()
        self.barrier_amount = 4
        self.barrier_x_positions = [num * (self.settings.screen_width / self.barrier_amount) for num in range(self.barrier_amount)]
        self.create_multiple_barriers(*self.barrier_x_positions, x_start=self.settings.screen_width / 15, y_start=480)

    def create_barrier(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = barrier.Barrier(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_barriers(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_barrier(x_start, y_start, offset_x)

    def restart(self):
        if self.stats.ships_left == 0: 
          self.game_over()
        print("restarting game")
        while self.sound.busy():    # wait for explosion sound to finish
            pass
        self.lasers.empty()
        self.alien_fleet.empty()
        self.alien_fleet.create_fleet()
        self.ship.center_bottom()
        self.ship.reset_timer()
        self.update()
        self.draw()
        sleep(0.5)

    def update(self):
        self.ship.update()
        self.alien_fleet.update()
        self.lasers.update()
        self.sb.update()

    def draw(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.bg_image, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.lasers.draw()
        self.sb.draw()
        pg.display.flip()
        self.blocks.draw(self.screen)

    def play(self):
        self.finished = False
        self.sound.play_bg()
        while not self.finished:
            self.update()
            self.draw()
            gf.check_events(game=self)   # exits game if QUIT pressed
        self.game_over()

    def game_over(self):
      self.sound.play_game_over()
      print('\nGAME OVER!\n\n')
      exit()    # can ask to replay here instead of exiting the game

def main():
    g = Game()
    lp = LandingPage(game=g)
    lp.show()
    g.play()


if __name__ == '__main__':
    main()
