import pyasge

from game.gamedata import GameData
from pytmx import TiledTileLayer
import pyasge
from game.gameobjects.gamemap import GameMap
from game.gamestates.gameplay import GamePlay


class Item:
    def __init__(self, buff, sprite, gamedata) -> None:
        self.scale = 1

        self.z_order = 100
        self.buff = buff
        self.item_sprite = sprite
        self.item = pyasge.Sprite()
        self.gamedata = gamedata
        self.X_pos = 2000
        self.Y_pos = 850
        self.item.x = self.X_pos
        self.item.y = self.Y_pos
        self.initItem()

    def initItem(self):
        if self.item.loadTexture(self.item_sprite):
            self.item.scale = .2
            print("Item Sprite loaded")
            return True
            return False
        pass
