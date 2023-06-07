import pyasge

from game.gamedata import GameData
from pytmx import TiledTileLayer
import pyasge
import math
from numpy import random
from game.gameobjects.gamemap import GameMap
from game.pathing import resolve


class Enemy:
    def __init__(self, health, damage, speed, sprite, gamedata) -> None:
        self.x_travel_distance = 0
        self.y_travel_distance = 0
        self.scale = 1
        self.z_order = 100
        self.health = health
        self.damage = damage
        self.speed = speed
        self.enemy_sprite = sprite
        self.timer = 0
        self.multiplier = 1
        self.enemy = pyasge.Sprite()
        self.position = pyasge.Point2D(self.enemy.x, self.enemy.y)
        self.gamedata = gamedata
        self.X_pos = self.enemy.x
        self.Y_pos = self.enemy.y
        self.initEnemy()

        self.enemy_path = []
        self.enemy_next_position = []
        self.enemy_position = []

    def initEnemy(self) -> bool:
        if self.enemy.loadTexture(self.enemy_sprite):
            self.enemy.scale = .2
            return True
        return False

    def enemy_movement(self, enemy, data: GameData):

        x = enemy.enemy.x + random.randint(-100, 100)
        y = enemy.enemy.y + random.randint(-100, 100)
        enemy_next_position = pyasge.Point2D(x, y)
        enemy_position = pyasge.Point2D(enemy.enemy.x, enemy.enemy.y)
        if self.timer == 50:
            if enemy_position != enemy_next_position:
                self.enemy_path = resolve(enemy_next_position, enemy_position, data)
            self.timer = 0
        else:
            self.timer += 1

        for i in range(len(self.enemy_path)):
            if enemy.enemy.x != self.enemy_path[i].x:
                if enemy.enemy.x > self.enemy_path[i].x:
                    enemy.enemy.rotation = 3.14
                    enemy.enemy.x -= 1
                elif enemy.enemy.x < self.enemy_path[i].x:
                    enemy.enemy.rotation = 0
                    enemy.enemy.x += 1
            if enemy.enemy.x != self.enemy_path[i].x:
                if enemy.enemy.y > self.enemy_path[i].y:
                    enemy.enemy.rotation = -1.6
                    enemy.enemy.y -= 1
                elif enemy.enemy.y < self.enemy_path[i].y:
                    enemy.enemy.rotation = 1.6
                    enemy.enemy.y += 1

    def render(self, renderer: pyasge.Renderer) -> None:
        """ Renders the enemy ship """
        renderer.render(self.enemy)


