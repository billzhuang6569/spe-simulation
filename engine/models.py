from dataclasses import dataclass

@dataclass
class Tile:
    x: int
    y: int
    walkable: bool = True
    door: bool = False

@dataclass
class Agent:
    id: str
    x: int
    y: int
    hp: int = 100
    hunger: int = 0
    anger: int = 0
    morale: int = 50
    fatigue: int = 0
    stress: int = 0
