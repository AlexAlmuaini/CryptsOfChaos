import pyasge
from pytmx import TiledTileLayer
import pyasge
from game.gameobjects.gamemap import GameMap


class Player:
    def __init__(self, health, damage, speed, sprite, gamedata) -> None:
        self.inputs = None
        self.scale = 1
        self.z_order = 100
        self.health = health
        self.damage = damage
        self.speed = speed
        self.player_sprite = sprite
        self.player = pyasge.Sprite()
        self.gamedata = gamedata
        self.X_pos = self.player.x
        self.Y_pos = self.player.y
        self.next_pos = pyasge.Point2D()
        self.keys = []
        self.x_velocity = 0
        self.y_velocity = 0
        self.player.x = 200
        self.player.y = 250
        self.next_x = self.player.x
        self.next_y = self.player.y
        self.midpoint = pyasge.Point2D(self.player.x, self.player.y)
        self.flipped = False
        self.initPlayer()

    def initPlayer(self) -> bool:
        if self.player.loadTexture(self.player_sprite):
            self.player.scale = .2
            return True
        return False

    def input(self, event: pyasge.KeyEvent):
        if event.action is pyasge.KEYS.KEY_PRESSED:
            if event.key is pyasge.KEYS.KEY_W:
                self.y_velocity = -50
            if event.key is pyasge.KEYS.KEY_S:
                self.y_velocity = 50
            if event.key is pyasge.KEYS.KEY_A:
                self.x_velocity = -50
            if event.key is pyasge.KEYS.KEY_D:
                self.x_velocity = 50

        if event.action is pyasge.KEYS.KEY_RELEASED:
            if event.key is pyasge.KEYS.KEY_W:
                self.y_velocity = 0
            if event.key is pyasge.KEYS.KEY_S:
                self.y_velocity = 0
            if event.key is pyasge.KEYS.KEY_A:
                self.x_velocity = 0
            if event.key is pyasge.KEYS.KEY_D:
                self.x_velocity = 0

    def resolve(self, game_time: pyasge.GameTime):
        # This Sets the players nexts position as a Point2D
        if self.gamedata.gamepad.connected:
            self.x_velocity = self.gamedata.inputs.getGamePad().AXIS_LEFT_X * 50
            self.y_velocity = self.gamedata.inputs.getGamePad().AXIS_LEFT_Y * 50

        self.next_x += (self.x_velocity * self.speed * game_time.fixed_timestep)
        self.next_y += (self.y_velocity * self.speed * game_time.fixed_timestep)
        self.next_pos = pyasge.Point2D(self.next_x + 20, self.next_y + 10)

        # This finds the tile cost of the next point
        player_next_loc = self.gamedata.game_map.tile(self.next_pos)
        tile_cost = self.gamedata.game_map.costs[player_next_loc[1]][player_next_loc[0]]
        if tile_cost < 100:
            self.player.x = self.next_x
            self.player.y = self.next_y
        if tile_cost > 100:
            self.next_x = self.player.x
            self.next_y = self.player.y

        self.midpoint = pyasge.Point2D(self.player.x, self.player.y)
