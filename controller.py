#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Название / назначение модуля."""

# Future
# from __future__ import

# Standard Library
import math
import json
import random
from pathlib import Path

# Third-party Libraries
import numpy as np
import pandas as pd

# Own sources

# === Классы ===

class Controller():
    """Класс управления программой."""

    def __init__(self, cfg, players):
        self.cfg = cfg
        self.tt = players
        self.players_count = self.tt.shape[0]
        self.create_tournament_table()

    def create_tournament_table(self):
        bands = self.create_bands()
        initial_mm_points = self.calc_initial_mm_points(bands)
        self.add_initial_mm_points_to_table(bands, initial_mm_points)

    def create_bands(self):
        top_band = self.tt[self.tt['rating'] >= self.cfg['bar']].shape[0]
        other_players = self.players_count - top_band
        # Сейчас распределяем по оставшимся группам ММ игроков равномерно.
        # Оставшиеся игроки распределяются в последнюю группу ММ.
        players_in_band = int(other_players/(self.cfg['bands'] - 1))
        bands = [top_band] + (self.cfg['bands'] - 2)*[players_in_band]
        bands += [self.players_count - sum(bands)]
        return bands

    def calc_initial_mm_points(self, bands):
        min_diff = 1
        max_diff = math.ceil(self.cfg['rounds']/3)
        mm_points = [0]
        for i, band in enumerate(bands[1:]):
            S = int(self.cfg['D']*band/self.cfg['rounds'])
            diff = min(max(S, min_diff), max_diff)
            mm_points.append(mm_points[i] - diff)
        max_points = abs(min(mm_points))
        mm_points = [mm_point + max_points for mm_point in mm_points]
        return mm_points

    def add_initial_mm_points_to_table(self, bands, mm_points):
        mm0_tmp = [band*[mm_point] for band, mm_point in zip(bands, mm_points)]
        mm0 = [mm_point for band in mm0_tmp for mm_point in band]
        self.tt['mm0'] = mm0
        self.tt['mm'] = mm0
        self.tt['buchholz'] = self.players_count*[0]
        self.tt['berger'] = self.players_count*[0]

    def simulate_tournament(self):
        print(self.tt)

    def simulate_round(self):
        # Сортируем по очкам ММ, к-м Бухгольца, Бергера и рейтингу
        self.tt = self.tt.sort_values(
            by=['mm', 'buchholz', 'berger', 'rating'])
        # Случайно определяем добровольно отсутствующих.
        volyntary_byes = [
            random.random() < 0.05 for i in range(self.players_count)]
        volyntary_byes_count = sum(volyntary_byes)
        forced_byes = self.players_count*[False]
        if (self.players_count - volyntary_byes_count)%2:
            # Назначаем отсутствующим последнего присутствующего игрока.
            forced_bye_idx = volyntary_byes.rindex(False)
            forced_byes[forced_bye_idx] = True

    def calc_probability_by_elo(self, players_pair):
        R0 = self.tt.loc[players_pair[0], 'rating']
        R1 = self.tt.loc[players_pair[1], 'rating']
        E0 = 1/(1 + 10**((R1-R0)/400))
        E1 = 1 - E0
        return [E0, E1]


# === Функции ===

def load_json(file):
    with open(file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print('Ошибка декодирования JSON')
            data = {}
        return data


# === Инструкции ===

if __name__ == '__main__':
    players_path = Path('./tests/players.json')
    players = pd.read_json(players_path, convert_dates=['reg_datetime'])
    players = players.sort_values(by='rating', ascending=False)
    players = players.reset_index(drop=True)
    players.index = players.index + 1
    cfg = {
        'rounds': 5,
        'bar': 2300,
        'bands': 8,
        'D': 0.75,
        }
    controller = Controller(cfg, players)
    controller.simulate_tournament()
    probabilities = []
    for pair in [[1, 2], [3, 4], [5, 12]]:
        probabilities.append(controller.calc_probability_by_elo(pair))
        