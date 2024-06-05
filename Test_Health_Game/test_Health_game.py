import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import unittest
from Health_Game import (
    static,
    Charactor,
    variable,
    container,
    set_map,
    interface,
    MediaPipe,
    main,
)
import datetime as dt
import json
import pygame
