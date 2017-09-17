# -*- coding: utf8 -*-
"""
flower.py - hoitaa kukkien käyttäytymisen

Sisältää:
class Flower - kukkien yleisobjekti
class WhiteFlower - valkoinen kukkaobjekti
class BlackFlower - musta kukkaobjekti
"""
import pygame
import groups
import random
from pygame.locals import *
from settings import *
from colors import *


class Flower(pygame.sprite.Sprite):
    """
    Kukkaobjekti. Hoitaa:
        -oman eliniän laskemisen lämpötilan mukaan
        -itsensä tappamisen kun elinikä täysi
    """
    def __init__(self, grid_x, grid_y, world=None, cell=None):
        pygame.sprite.Sprite.__init__(self, groups.flower_group)

        # Viittaukset maailmaan ja soluun
        self.world = world
        self.cell = cell
        # Tärkeä - asetettaa solun kukaksi itsensä
        self.cell.flower = self

        # Väri, albedo, radiation, suosittu lämpötila - nämä tarkoitus overrideta
        self.color = (127, 127, 127)
        self.albedo = None
        self.radiation = None
        self.preferred_temp = None

        # Elinikä
        self.lifetime = Settings.flower_lifetime
        # TODO: tämän ei pitäisi tapahtua näin joka kerta kun kukka spawnaa vaan vain alkuspawnauksessa
        self.life_counter = random.randint(0, self.lifetime - 1)

        # Kuva, rect
        self.image = pygame.Surface((Settings.flower_width, Settings.flower_height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        # Paikka ruudukossa
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.rect.topleft = (Settings.window_margin + Settings.flower_margin + self.grid_x * Settings.cell_width,
                             Settings.window_margin + Settings.flower_margin + self.grid_y * Settings.cell_height)

    def kill(self):
        """
        Tappaa kukan. Eli:
            -poistaa sprite-ryhmästä
            -poistaa maailman flower citionarystä
            -poistaa solusta viittauksen
        """
        pygame.sprite.Sprite.kill(self)
        del self.world.flowers_dict[self.grid_x][self.grid_y]
        self.cell.flower = None

    def update(self):
        """
        Laskee elinaikaa. Jos liian kuuma/kylmä, elinaika lyhyempi. Jos elinaika täysi, kuolee.
        Myös lisää itsensä kukkalaskuriin.
        """
        temp_diff = float(abs(self.world.cells_dict[self.grid_x][self.grid_y].temp - self.preferred_temp))
        self.life_counter += 1 + int(temp_diff / 20)
        if self.life_counter >= self.lifetime:
            self.kill()

        # Statistiikkalaskuri
        if self in groups.flower_group:
            if self.color == WHITE:
                self.world.white_counter += 1
            elif self.color == BLACK:
                self.world.black_counter += 1

    def update_color(self):
        """ Päivittää kuvan oikean väriseksi """
        self.image.fill(self.color)


class WhiteFlower(Flower):
    """ Valkoinen kukka. Albedo suurempi, radiation-arvo vähän pienempi kuin mustalla. """
    def __init__(self, grid_x, grid_y, world=None, cell=None):
        Flower.__init__(self, grid_x, grid_y, world=world, cell=cell)
        self.color = WHITE
        self.update_color()
        self.albedo = Settings.flower_white_albedo
        self.radiation = Settings.flower_while_radiation
        self.preferred_temp = Settings.flower_white_pref_temp


class BlackFlower(Flower):
    """ Musta kukka. Albedo matalampi, radiation-arvo vähän suurempi kuin valkoisella. """
    def __init__(self, grid_x, grid_y, world=None, cell=None):
        Flower.__init__(self, grid_x, grid_y, world=world, cell=cell)
        self.color = BLACK
        self.update_color()
        self.albedo = Settings.flower_black_albedo
        self.radiation = Settings.flower_black_radiation
        self.preferred_temp = Settings.flower_black_pref_temp
