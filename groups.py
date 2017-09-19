# -*- coding: utf8 -*-
"""
groups.py - hoitaa pygamen sprite-ryhmät
"""
import pygame

# Groupit
world_group = pygame.sprite.Group()
cell_group = pygame.sprite.Group()
flower_group = pygame.sprite.Group()
ui_group = pygame.sprite.Group()

# Avustavat groupit - näitä ei ole tarkoitus piirtää
white_flowers_group = pygame.sprite.Group()
black_flowers_group = pygame.sprite.Group()
