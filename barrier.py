import pygame as pg
from pygame.sprite import Sprite
from pygame.sprite import Group
from copy import copy
from timer import Timer


class Barriers(Sprite):
    def __init__(self, game):
        super().__init__()
        self.barriers = [Barrier(game=game, x=x, y=650) for x in range(250, 1050, 200)]
        # slower way
        # self.barriers = [Barrier(game=game, x=250, y=650), Barrier(game=game, x=450, y=650),
        #                  Barrier(game=game, x=650, y=650), Barrier(game=game, x=850, y=650)]
        self.barriers_group = Group()
        for barrier in self.barriers:                                  # add individual BarrierBlocks to group
            self.barriers_group.add(barrier.barrier_group.sprites())   # so ship/alien can test bullets against blocks

    def group(self): return self.barriers_group

    def update(self):
        super().__init__()
        for barrier in self.barriers:
            barrier.update()

    def draw(self):
        for barrier in self.barriers:
            barrier.draw()


class Barrier(Sprite):
    bi = [pg.image.load('images/block4.png'), pg.image.load('images/block3.png'),
          pg.image.load('images/block2.png'), pg.image.load('images/block1.png'),
          pg.image.load('images/block0.png')]

    block_images = [pg.image.load(f"images/block{x}.png") for x in range(4, -1, -1)]
    block_topL_images = [pg.image.load(f"images/blockTL{x}.png") for x in range(4, -1, -1)]
    block_topR_images = [pg.image.load(f"images/blockTR{x}.png") for x in range(4, -1, -1)]

    block_rect = block_images[0].get_rect()
    height, width = block_rect.width, block_rect.height
    barrier_height = 5
    barrier_width = 7

    def __init__(self, game, x, y):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.x, self.y = x, y
        self.rect = copy(Barrier.block_rect)
        self.screen_rect = game.screen.get_rect()
        self.rect.x, self.rect.y = x, y
        self.barrier_group = Group()
        self.create_barrier()

    def create_barrier(self):
        w, h = Barrier.block_rect.width, Barrier.block_rect.height
        rect = copy(self.rect)
        for x in range(Barrier.barrier_width):
            for y in range(Barrier.barrier_height):
                if y >= Barrier.barrier_height - 1 and 2 <= x <= 4: continue
                r = copy(rect)

                timer = Timer(frames=Barrier.block_images, looponce=True, wait_for_command=True)
                if y == 0 and x == 0:
                    timer = Timer(frames=Barrier.block_topL_images, looponce=True, wait_for_command=True)
                elif y == 0 and x == Barrier.barrier_width - 1:
                    timer = Timer(frames=Barrier.block_topR_images, looponce=True, wait_for_command=True)
                r = copy(rect)
                r.y += h * y
                r.x += w * x
                self.barrier_group.add(BarrierBlock(parent=self, game=self.game, timer=timer, rect=r))

    def group(self): return self.barrier_group

    def update(self):
        self.barrier_group.update()
        for block in self.barrier_group:
            block.update()

    def draw(self):
        for block in self.barrier_group:
            block.draw()


class BarrierBlock(Sprite):
    FIT_AS_A_FIDDLE = 4
    JUST_A_SCRATCH = 3
    PRETTY_SERIOUS = 2
    CRITICAL = 1
    DEAD = 0

    def __init__(self, parent, game, timer, rect):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.parent = parent
        self.game = game
        self.timer = timer
        self.screen = game.screen
        self.rect = rect
        self.health = BarrierBlock.FIT_AS_A_FIDDLE

    def damaged(self):
        health = self.health
        if health is not BarrierBlock.DEAD: self.health -= 1
        self.timer.advance_frame_index()
        if self.timer.finished: self.kill()

    def update(self): pass   # update self to show damage
    # TODO:  USE PILLOW to modify self.image to show extent of damage to health
    #    TODO: OR... use a Timer and advance it each time the barrier is damaged...

    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
