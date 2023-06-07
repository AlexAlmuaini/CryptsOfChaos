import pyasge


class Projectile:
    def __init__(self, gamedata) -> None:
        self.scale = 1
        self.z_order = 100
        self.laser = pyasge.Sprite()
        self.next_x = self.laser.x
        self.initProjectile()
        self.data = gamedata
        self.next_pos = 0

    def initProjectile(self) -> bool:
        if self.laser.loadTexture("data/laser.png"):
            self.laser.scale = 0.015
            return True
        return False

    def resolve(self, game_time: pyasge.GameTime) -> bool:
        # This Sets the lasers next position as a Point2D
        self.next_x = 500 * game_time.fixed_timestep
        self.next_pos = pyasge.Point2D(self.next_x, self.laser.y)

        # This finds the tile cost of the next point
        player_next_loc = self.data.game_map.tile(self.next_pos)
        tile_cost = self.data.game_map.costs[player_next_loc[1]][player_next_loc[0]]

        if tile_cost > 100:
            return False
        return True

    def spawn(self, spawn_x, spawn_y):
        self.laser.x = spawn_x
        self.laser.y = spawn_y

    def movement(self, game_time: pyasge.GameTime):
        self.laser.x += 500 * game_time.fixed_timestep

    def render(self, renderer: pyasge.Renderer) -> None:
        renderer.render(self.laser)
