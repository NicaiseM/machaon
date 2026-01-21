#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Название / назначение модуля."""

# Future
# from __future__ import

# Standard Library
import math
import json
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
        self.players = players

    def simulate_tournament(self):
        bands = self.create_bands()
        initial_mm_points = self.calc_initial_mm_points(bands)
        print(bands)
        print(initial_mm_points)

    def create_bands(self):
        top_band = players[players['rating'] >= self.cfg['bar']].shape[0]
        other_players = players.shape[0] - top_band
        players_in_band = int(other_players/(self.cfg['bands'] - 1))
        bands = [top_band] + (self.cfg['bands'] - 2)*[players_in_band]
        bands += [players.shape[0] - sum(bands)]
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

    def calc_probability_by_elo(self, players_pair):
        R0 = self.players.loc[players_pair[0], 'rating']
        R1 = self.players.loc[players_pair[1], 'rating']
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
        'players_in_band': 7,
        'D': 0.75,
        }
    controller = Controller(cfg, players)
    controller.simulate_tournament()
    probabilities = []
    for pair in [[1, 2], [3, 4], [5, 12]]:
        probabilities.append(controller.calc_probability_by_elo(pair))
        