import pygame as pg
from pygame.sprite import Sprite
from timer import Timer


class Bullet(Sprite):
    isb = [pg.image.load('images/ship_bullet0.png'), pg.image.load('images/ship_bullet1.png')]

    iab = [pg.image.load('images/alien_bullet0.png'), pg.image.load('images/alien_bullet1.png')]


    images_ship_bullet = [pg.image.load('images/ship_bullet' + str(i) + '.png') for i in range(2)]
    images_alien_bullet = [pg.image.load('images/alien_bullet' + str(i) + '.png') for i in range(2)]
    images_boom = [pg.image.load('images/alien_boom' + str(i) + '.png') for i in range(7)]
    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, game, x, y, timer):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.timer = timer
        self.x, self.y = x, y
        self.dead, self.really_dead, self.timer_switched = False, False, False

    def killed(self):
        print('bullet killed')
        if not self.dead and not self.really_dead: self.dead = True
        if self.dead and not self.timer_switched:
            self.timer = self.timer_boom
            self.timer_switched = True

    def update(self):
        if self.dead and self.timer_switched:
            if self.timer.finished:
                self.dead = False
                self.timer_switched = False
                self.really_dead = True
                self.kill()
                print('bullet was killed')
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw(self):
        # pg.draw.rect(self.screen, self.color, self.rect)
        image = self.timer.imagerect()
        print(self.timer.frameindex)
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)


class BulletFromAlien(Bullet):
    """A class to manage bullets fired from the alien"""
    def __init__(self, game, x, y):
        super().__init__(game=game, x=x, y=y,
                         timer=Timer(frames=Bullet.iab, wait=300))
        settings = game.settings
        self.color = settings.alien_bullet_color
        self.speed_factor = -settings.bullet_speed_factor
        self.width = settings.alien_bullet_width
        self.height = settings.alien_bullet_height

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.top = y
        self.rect.centerx = x
        self.y = float(self.rect.y)

    def draw(self): super().draw()
        # pg.draw.rect(self.screen, self.color, self.rect)


class BulletFromShip(Bullet):
    """A class to manage bullets fired from the ship"""
    def __init__(self, game, x, y):
        super().__init__(game=game, x=x, y=y,
                         timer=Timer(frames=Bullet.isb))
        settings = game.settings
        self.color = settings.ship_bullet_color
        self.speed_factor = -settings.bullet_speed_factor
        self.width = settings.ship_bullet_width
        self.height = settings.ship_bullet_height

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.top = y
        self.rect.centerx = x
        self.y = float(self.rect.y)
        self.speed_factor = game.settings.bullet_speed_factor

    def draw(self): super().draw()
        # pg.draw.rect(self.screen, self.color, self.rect)