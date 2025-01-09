from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Item:
    """Represents an item in the game world"""

    name: str
    base_price: int


@dataclass
class Player:
    name: str
    gold: int
    inventory: dict[str, int]

    def pay(self, amount: int):
        if self.gold < amount:
            raise ValueError("Not enough gold!")
        self.gold -= amount

    def receive(self, amount: int):
        self.gold += amount


@dataclass
class Town:
    name: str
    x: int
    y: int
    is_main_city: bool = False
    price_weights: dict[str, int] = None

    @property
    def coordinates(self) -> tuple:
        """Returns the coordinates of the town as a tuple"""
        return (self.x, self.y)

    def distance_from(self, town: Town) -> int:
        """Returns the distance from this town to another town"""
        return int(math.sqrt((self.x - town.x) ** 2 + (self.y - town.y) ** 2))
