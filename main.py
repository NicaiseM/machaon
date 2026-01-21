#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Название / назначение модуля."""

# Future
# from __future__ import

# Standard Library
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


__author__      = "Nikita Makarchuk"
__copyright__   = "Copyright 2023, Nikita Makarchuk"
__credits__     = ["Nikita Makarchuk"]
__license__     = "GPL"
__version__     = "0.0.1"
__maintainer__  = "Nikita Makarchuk"
__email__       = "nicaise@rambler.ru"
__status__      = "Prototype|Development|Production"


# === Классы ===

class MyClass():
    """Класс выполнения чего-то важного."""

    def __init__(self):
        pass

    def my_method(self):
        """Замечательное действие."""
        pass


# === Функции ===

def my_func():
    """Действие не менее замечательное."""
    pass


# === Инструкции ===

if __name__ == '__main__':
    file = Path(r"./myFile.csv")


# TODO:
# - сделать то, включая:
#   - это
# - сделать что-то еще
