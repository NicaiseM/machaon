#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Название / назначение модуля."""

# Future
# from __future__ import

# Standard Library
import json
from pathlib import Path

# Third-party Libraries
import scipy as sp
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Own sources
from metric import metric as mt
from service_utilities import TimeTest

# === Классы ===

class Controller():
    """Класс управления программой."""

    def __init__(self, cfg, players):
        self.cfg = cfg
        self.players = players

    def calc_probability_by_elo(self, players_pair):
        """Расчет вероятностей победы игроков в паре."""
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
        'bands': 10,
        'D': 0.75,
        }
    controller = Controller(cfg, players)
    probabilities = []
    for pair in [[1, 2], [3, 4], [5, 12]]:
        probabilities.append(controller.calc_probability_by_elo(pair))
        