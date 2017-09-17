# -*- coding: utf8 -*-
"""
main.py - hoitaa itse ohjelman suorittamisen

sisältää:
class Program - ohjelmaobjekti
debug_run() - funktio, joka käynnistää ja ajaa ohjelman
"""
import pygame
import text
import world
import cell
import groups
from pygame.locals import *
from colors import *
from settings import *


class Program(object):
    """
    Ohjelmaobjekti. Hoitaa seuraavat asiat:
        -Pygamen initit
        -graffojen piirrot
        -laskurien ja inffojen näyttö
        -eventtien handlaukset
        -lopettaminen

    Tätä on tarkoitus kutsua näin:
        game = Program()
        while game.running:
            game.update()
    """
    def __init__(self):
        # Pygamen inittiä, näytön asetus
        pygame.init()
        self.disp_surf = pygame.display.set_mode(Settings.window_size)
        pygame.display.set_caption(Settings.window_caption)

        self.clock = pygame.time.Clock()
        self.last_turn_started_at = pygame.time.get_ticks()

        self.running = 1
        # hover_cell on se solu, jonka päällä hiiri on
        self.hover_cell = None

        # world on maailma
        self.world = world.World(program=self)

        # infotekstit
        self.turn_text = text.Text(group=groups.ui_group, pos=(30, 30), text="Turn 0", font_size=40, align='topleft')
        self.info_text = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 30, 10), text="(info)", font_size=40, align='topright')
        self.avg_temp_text = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 30, 50), text="(avg tmp)", font_size=40, align='topright')
        self.black_counter_text = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 40, Settings.window_size[1] - 50), text="Black", font_size=40, align='bottomright')
        self.white_counter_text = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 40, Settings.window_size[1] - 10), text="White", font_size=40, align='bottomright')

    def update(self):
        """
        update-metodi: tätä kun kutsutaan koko ajan niin ohjelma pyörii
        """
        # ruutu tyhjäksi
        self.disp_surf.fill(BLACK)

        # sprite-groupien piirrot ruudulle
        groups.world_group.draw(self.disp_surf)
        groups.cell_group.draw(self.disp_surf)
        groups.flower_group.draw(self.disp_surf)
        groups.ui_group.draw(self.disp_surf)

        pygame.display.flip()

        self.clock.tick(Settings.fps)

        # eventtien handlaus
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = 0
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.running = 0
                # elif event.key == K_SPACE:
                #     self.advance_turn()
                # elif event.key == K_PLUS or event.key == K_KP_PLUS:
                #     Settings.turn_time_seconds -= .1
                # elif event.key == K_MINUS or event.key == K_KP_MINUS:
                #     Settings.turn_time_seconds += .1
            elif event.type == MOUSEMOTION:
                # heitetään mouse motion cellien käsiteltäväksi että osaavat muuttaa väriään jos hover
                for current_cell in groups.cell_group:
                    possible_hover_cell = current_cell.handle_mouse_motion(event)
                    if possible_hover_cell is not None:
                        self.hover_cell = possible_hover_cell
            elif event.type == MOUSEBUTTONDOWN:
                # heitetään mouse click myös cellien käsiteltäväksi - tällä hetkellä voi muuttaa lämpötilaa solussa näin
                for current_cell in groups.cell_group:
                    current_cell.handle_mouse_click(event)

        # hoveratun cellin infotekstin päivitys
        self.update_hover_text()

        # turn timen laskenta
        if pygame.time.get_ticks() - self.last_turn_started_at >= Settings.turn_time_seconds * 1000:
            self.advance_turn()

    def advance_turn(self):
        """
        Siirtää simulaation seuraavaan vuoroon. Käytännössä lähettää tästä vain tiedon world-objektille, joka
        hoitaa itse simuloinnin. Tämän jälkeen sitten päivittää infotekstit.
        """
        self.world.update()
        self.turn_text.text = "Turn {}".format(self.world.turn_counter)
        self.avg_temp_text.text = "Avg temp: {}".format(round(self.world.avg_temp, 2))
        self.black_counter_text.text = "Black: {}".format(self.world.black_counter)
        self.white_counter_text.text = "White: {}".format(self.world.white_counter)
        self.last_turn_started_at = pygame.time.get_ticks()

    def update_hover_text(self):
        """ Päivittää sen infotekstin, joka kertoo hoveratun cellin tiedot """
        if self.hover_cell is not None:
            update_text = "Cell temp: {}".format(round(self.hover_cell.temp, 2))
        else:
            update_text = ""
        self.info_text.text = update_text


def debug_run():
    game = Program()
    while game.running:
        game.update()

if __name__ == "__main__":
    debug_run()