# -*- coding: utf8 -*-
"""
settings.py - hoitaa asetukset

Sisältää:
class Settings - sisältää asetuksia
"""


class Settings(object):
    # Solujen määrä, koko, ominaisuudet
    cells_x = 50
    cells_y = 50
    cell_width = 10
    cell_height = 10
    cell_start_temp = 50
    cell_albedo = 0.5
    cell_radiation = 0.5

    # Kukkien ominaisuudet
    flower_margin = 2
    flower_width = cell_width - 2 * flower_margin
    flower_height = cell_height - 2 * flower_margin
    flower_lifetime = 100
    flower_spawn_white_chance = 50
    flower_spawn_black_chance = 50

    flower_white_albedo = 0.9
    flower_while_radiation = 0.4
    flower_white_pref_temp = 20
    flower_black_albedo = 0.1
    flower_black_radiation = 0.6
    flower_black_pref_temp = 80

    # Auringon voimakkuus
    sun_power = 1.0

    # Ikkunan koko
    window_margin = 100
    window_size = (cells_x * cell_width + 2 * window_margin, cells_y * cell_height + 2 * window_margin)
    window_caption = "Flowers"

    # FPS, vuoroajastin
    fps = 30
    turn_time_seconds = 0.0
