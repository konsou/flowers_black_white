# -*- coding: utf8 -*-
import pygame
import groups
import cell
import flower
import random
from pygame.locals import *
from settings import *


class World(pygame.sprite.Sprite):
    def __init__(self, program=None):
        pygame.sprite.Sprite.__init__(self, groups.world_group)

        self.program = program

        self.turn_counter = 0
        # self.black_counter = 0
        # self.white_counter = 0

        self.width = Settings.cells_x * Settings.cell_width
        self.height = Settings.cells_y * Settings.cell_height
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (Settings.window_margin, Settings.window_margin)
        self.image.fill((255, 0, 0))

        self.cells_dict = {}
        self.flowers_dict = {}

        for x in range(Settings.cells_x):
            self.cells_dict[x] = {}
            self.flowers_dict[x] = {}
            for y in range(Settings.cells_y):
                self.cells_dict[x][y] = cell.Cell(x, y, world=self)
                if random.randint(1, 2) == 1:
                    flower_class = flower.WhiteFlower
                else:
                    flower_class = flower.BlackFlower
                self.flowers_dict[x][y] = flower_class(x, y, world=self, cell=self.cells_dict[x][y])

    def update(self):
        self.turn_counter += 1
        # self.white_counter = 0
        # self.black_counter = 0
        for current_cell in groups.cell_group:
            current_cell.temp_to_previous()
        groups.cell_group.update()
        groups.flower_group.update()
        self.spawn_flowers()

    def spawn_flowers(self):
        for current_cell in groups.cell_group:
            if current_cell.flower is None:
                # Mitä kauempana optimirangesta, sen huonompi tsäännssi
                white_chance = Settings.flower_spawn_white_chance
                white_chance -= abs(current_cell.temp - Settings.flower_white_pref_temp)
                white_chance = max(0, round(white_chance))

                black_chance = Settings.flower_spawn_black_chance
                black_chance -= abs(current_cell.temp - Settings.flower_black_pref_temp)
                black_chance = max(0, round(black_chance))

                if not white_chance + black_chance == 0:
                    try:
                        random_number = random.randint(1, white_chance + black_chance)
                    except ValueError:
                        raise ValueError("ValueError in World -> spawn_flowers. white_chance: {}, black_chance: {}".format(white_chance, black_chance))
                    if random_number <= white_chance:
                        flower_class = flower.WhiteFlower
                    else:
                        flower_class = flower.BlackFlower
                    self.flowers_dict[current_cell.grid_x][current_cell.grid_y] = flower_class(current_cell.grid_x, current_cell.grid_y, world=self, cell=current_cell)

    def _get_avg_temp(self):
        total_temp = 0.0
        for current_cell in groups.cell_group:
            total_temp += current_cell.temp
        return total_temp / len(groups.cell_group)

    avg_temp = property(_get_avg_temp)
