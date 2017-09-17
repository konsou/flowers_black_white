# -*- coding: utf8 -*-
import pygame
import groups
from pygame.locals import *
from settings import *
from colors import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, world=None, flower=None,
                 width=Settings.cell_width, height=Settings.cell_height, start_temp=Settings.cell_start_temp):
        pygame.sprite.Sprite.__init__(self, groups.cell_group)

        self.world = world
        self.flower = flower

        self.temp = float(start_temp)
        self.previous_temp = self.temp
        self._albedo = Settings.cell_albedo
        self._radiation = Settings.cell_radiation

        self.width = width
        self.height = height
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(number_to_color(self.temp))
        # pygame.draw.rect(self.image, 0, (0, 0, self.width, self.height), 1)
        self.rect = self.image.get_rect()

        self.rect.topleft = (Settings.window_margin + self.grid_x * Settings.cell_width,
                             Settings.window_margin + self.grid_y * Settings.cell_height)

        self.mouse_is_over = 0

    def __repr__(self):
        return "<Cell object - x: {}, y: {}, temp: {}, albedo: {}, radiation: {}>".format(self.grid_x, self.grid_y, self.temp, self.albedo, self.radiation)

    def update(self):
        # print "{} - UPDATE".format(self)
        # Laskee tempin - keskiarvo immediate naapureista
        neighbors = self.get_neighbors()
        temp_sum = 0
        for current_neighbor in neighbors:
            temp_sum += current_neighbor.previous_temp
        self.temp = temp_sum / len(neighbors)
        # print "Temp after neighbors: {}".format(self.temp)
        # Käytetään kukan albedoa ja säteilyä jos sellainen on - muuten maapläntin arvoja

        # Auringon säteily - albedo kertoo paljonko heijastuu pois
        self.temp += Settings.sun_power * (1 - self.albedo)
        # print "Temp after sun shines: {}".format(self.temp)

        # Lämmön säteily pois
        self.temp -= self.radiation
        # print "Temp after radiation: {}".format(self.temp)

        self.update_color()

    def temp_to_previous(self):
        """ Tämä tärkeää että averaget menee oikein """
        self.previous_temp = self.temp

    def update_color(self):
        if self.mouse_is_over:
            color = YELLOWISH
        else:
            color = number_to_color(self.temp)
        self.image.fill(color)

    def handle_mouse_motion(self, event):
        ret_val = None
        if self.rect.collidepoint(event.pos):
            self.mouse_enter()
            ret_val = self
        else:
            self.mouse_exit()
        return ret_val

    def handle_mouse_click(self, event):
        if self.rect.collidepoint(event.pos):
            if event.button == 1:
                self.temp += 50
            elif event.button == 3:
                self.temp -= 50
            # ret_val = "x: {} y: {} temp: {}".format(self.grid_x, self.grid_y, round(self.temp, 2))

    def mouse_enter(self):
        if not self.mouse_is_over:
            self.mouse_is_over = 1
            self.image.fill(YELLOWISH)
            # return "x: {} y: {} temp: {}".format(self.grid_x, self.grid_y, round(self.temp, 2))

    def mouse_exit(self):
        if self.mouse_is_over:
            self.mouse_is_over = 0
            self.update_color()

    def get_neighbors(self):
        """ Palauttaa listan immediate neighboreista - SISÄLTÄEN ITSENSÄ """
        return_list = []
        coords_preset = [
                           (0, -1),
                  (-1, 0), (0,  0), (+1, 0),
                           (0, +1)
                        ]
        for coordinate in coords_preset:
            try:
                return_list.append(self.world.cells_dict[self.grid_x + coordinate[0]][self.grid_y + coordinate[1]])
            except KeyError:
                pass

        return return_list

    def _get_albedo(self):
        if self.flower is not None:
            return self.flower.albedo
        else:
            return self._albedo

    def _get_radiation(self):
        if self.flower is not None:
            return self.flower.radiation
        else:
            return self._radiation

    albedo = property(_get_albedo)
    radiation = property(_get_radiation)


