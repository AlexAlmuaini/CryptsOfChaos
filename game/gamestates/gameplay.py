import math
import random

import numpy as np
import pyasge

from game.Player import Player
from game.Projectile import Projectile
from game.enemy import Enemy
from game.pathing import resolve
from game.gamedata import GameData
from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gamestates.gamemenu import GameMenu


class GamePlay(GameState):
    """ The game play state is the core of the game itself.

    The role of this class is to process the game logic, update
    the players positioning and render the resultant game-world.
    The logic for deciding on victory or loss should be handled by
    this class and its update function should return GAME_OVER or
    GAME_WON when the end game state is reached.
    """

    def __init__(self, data: GameData) -> None:
        """ Creates the game world

        Use the constructor to initialise the game world in a "clean"
        state ready for the player. This includes resetting of player's
        health and the enemy positions.

        Args:
            data (GameData): The game's shared data
        """
        super().__init__(data)

        self.timer = 0
        self.id = GameStateID.GAMEPLAY
        self.data.renderer.setClearColour(pyasge.COLOURS.CORAL)
        self.init_ui()
        self.transition = 0
        self.game_time = pyasge.GameTime

        # sets up the camera and points it at the player
        map_mid = [
            self.data.game_map.width * self.data.game_map.tile_size[0] * 0.5,
            self.data.game_map.height * self.data.game_map.tile_size[1] * 0.5
        ]
        self.data.player = Player(100, 10, 1, "data/textures/test sprite.png", self.data)
        self.camera = pyasge.Camera(map_mid, self.data.game_res[0], self.data.game_res[1])
        self.camera.zoom = 2.25
        self.health_ui = 100
        self.ui_label = pyasge.Text(self.data.renderer.getDefaultFont(), "HP: 100", 10, 50)
        self.ui_label.z_order = 120
        self.camera.lookAt(self.data.player.midpoint)
        self.enemies = []
        self.enemy_moving = False
        self.spawn_enemies()
        self.data.cursor.scale = 2
        self.kill_tally = 0
        self.projectiles = []

    def player_health(self):
        if self.data.player.health >= 100:
            self.ui_label.string = "HP: 100"
        elif 90 <= self.data.player.health < 100:
            self.ui_label.string = "HP: 90"
        elif 80 <= self.data.player.health < 90:
            self.ui_label.string = "HP: 80"
        elif 70 <= self.data.player.health < 80:
            self.ui_label.string = "HP: 70"
        elif 60 <= self.data.player.health < 70:
            self.ui_label.string = "HP: 60"
        elif 50 <= self.data.player.health < 60:
            self.ui_label.string = "HP: 50"
        elif 40 <= self.data.player.health < 50:
            self.ui_label.string = "HP: 40"
        elif 30 <= self.data.player.health < 40:
            self.ui_label.string = "HP: 30"
        elif 20 <= self.data.player.health < 30:
            self.ui_label.string = "HP: 20"
        elif 10 <= self.data.player.health < 20:
            self.ui_label.string = "HP: 10"
        elif 1 <= self.data.player.health < 10:
            self.ui_label.string = "HP: 1"

    def spawn_enemies(self) -> None:
        """ Loads the map and spawns enemies"""
        rands = random.sample(self.data.game_map.spawns, 35)
        while len(self.enemies) != 5*self.data.difficulty:
            self.enemies.append(Enemy(3, 10, 10, "data/Test_cube.png", GameData))
            x, y = rands.pop()
            self.enemies[-1].enemy.x = x
            self.enemies[-1].enemy.y = y

    def spawn_projectiles(self) -> None:
        if len(self.projectiles) >= 10:
            self.projectiles.pop(0)
        else:
            self.projectiles.append(Projectile(self.data))
        self.projectiles[-1].spawn(self.data.player.player.x + 40, self.data.player.player.y + 10)

    def init_ui(self):
        """Initialises the UI elements"""
        pass

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.button is pyasge.MOUSE.MOUSE_BTN2 and \
                event.action is pyasge.MOUSE.BUTTON_PRESSED:
            pass

        if event.button is pyasge.MOUSE.MOUSE_BTN1 and \
                event.action is pyasge.MOUSE.BUTTON_PRESSED:
            pass

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        """ Listens for mouse movement events from the game engine """
        pass

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        """ Listens for key events from the game engine """
        self.data.player.input(event)
        if event.key == pyasge.KEYS.KEY_SPACE:
            self.spawn_projectiles()
        if event.key == pyasge.KEYS.KEY_ENTER:
            self.transition = True

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """ Simulates deterministic time steps for the game objects"""
        for enemy in self.enemies:
            enemy.enemy_movement(enemy, self.data)
            if self.collision_check(enemy.enemy, self.data.player.player):
                self.data.player.health -= 1
                self.player_health()

            for laser in self.projectiles:
                if self.collision_check(enemy.enemy, laser.laser):
                    if enemy.health <= 0:
                        self.kill_tally += 1
                        self.enemies.remove(enemy)
                    else:
                        self.projectiles.remove(laser)
                        enemy.health -= 1

        for laser in self.projectiles:
            laser.movement(game_time)
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        self.data.player.resolve(game_time)
        """ Updates the game world

        Processes the game world logic. You should handle collisions,
        actions and AI actions here. At present cannonballs are
        updated and so are player collisions with the islands, but
        consider how the ships will react to each other

        Args:
            game_time (pyasge.GameTime): The time betwewaen ticks.
        """

        # This changes game states to gameover.py
        if self.data.player.health == 0:
            self.transition = 3
        elif self.kill_tally == 5 * self.data.difficulty:
            self.transition = 2
        else:
            self.transition = 0
        self.update_camera()
        self.update_inputs()

        # changes player to death screen - change self.transition to an int for multiple states.
        if self.transition == 1:
            return GameStateID.START_MENU
        if self.transition == 2:
            return GameStateID.WINNER_WINNER
        if self.transition == 3:
            return GameStateID.GAME_OVER
        return GameStateID.GAMEPLAY


    def update_camera(self):
        """ Updates the camera based on gamepad input"""
        if self.data.gamepad.connected:
            self.camera.translate(
                self.data.inputs.getGamePad().AXIS_LEFT_X * 10,
                self.data.inputs.getGamePad().AXIS_LEFT_Y * 10, 0.0)
        self.camera.lookAt(self.data.player.midpoint)

        # This keeps the camera lock onto the bounds of the map
        view = [
            self.data.game_res[0] * 0.5 / self.camera.zoom,
            self.data.game_map.width * 32 - self.data.game_res[0] * 0.5 / self.camera.zoom,
            self.data.game_res[1] * 0.5 / self.camera.zoom,
            self.data.game_map.height * 32 - self.data.game_res[1] * 0.5 / self.camera.zoom
        ]
        self.camera.clamp(view)

    def update_inputs(self):
        """ This is purely example code to show how gamepad events
        can be tracked """
        if self.data.gamepad.connected:
            if self.data.gamepad.A and not self.data.prev_gamepad.A:
                self.spawn_projectiles()
                pass
            elif self.data.gamepad.A and self.data.prev_gamepad.A:
                # A button is being held
                pass
            elif not self.data.gamepad.A and self.data.prev_gamepad.A:
                # A button has been released
                pass

    def render(self, game_time: pyasge.GameTime) -> None:
        """ Renders the game world and the UI """
        self.data.renderer.setViewport(pyasge.Viewport(0, 0, self.data.game_res[0], self.data.game_res[1]))
        self.data.renderer.setProjectionMatrix(self.camera.view)
        # THIS IS THE SHADER.
        self.data.shaders["example"].uniform("rgb").set([0.75, 1.0, 0.75])
        for enemy in self.enemies:
            if self.collision_check(enemy.enemy, self.data.player.player):
                self.data.shaders["example"].uniform("rgb").set([1.0, 0.5, 0.5])
        self.data.renderer.shader = self.data.shaders["example"]
        self.data.game_map.render(self.data.renderer, game_time)
        self.render_ui()
        for enemy in self.enemies:
            enemy.render(self.data.renderer)
        self.data.renderer.render(self.data.player.player)
        for lasers in self.projectiles:
            lasers.render(self.data.renderer)

    def render_ui(self) -> None:
        """ Render the UI elements and map to the whole window """
        # set a new view that covers the width and height of game
        camera_view = pyasge.CameraView(self.data.renderer.resolution_info.view)
        vp = self.data.renderer.resolution_info.viewport
        self.data.renderer.setProjectionMatrix(0, 0, vp.w, vp.h)

        # THIS IS THE HEALTH RENDER
        self.data.renderer.render(self.ui_label)

        # this restores the original camera view
        self.data.renderer.setProjectionMatrix(camera_view)

    def to_world(self, pos: pyasge.Point2D) -> pyasge.Point2D:
        """
        Converts from screen position to world position
        :param pos: The position on the current game window camera
        :return: Its actual/absolute position in the game world
        """
        view = self.camera.view
        x = (view.max_x - view.min_x) / self.data.game_res[0] * pos.x
        y = (view.max_y - view.min_y) / self.data.game_res[1] * pos.y
        x = view.min_x + x
        y = view.min_y + y

        return pyasge.Point2D(x, y)

    """This is collision detection, don't fuck with it, it works. 
    It's currently being used for player to enemy collision but it's abstract so it can be used
    for projectiles when implemented. If you need help understanding it, ASK. ~Alex"""

    def collision_check(self, sprite, projectile) -> bool:
        sprite_bounds = sprite.getWorldBounds()
        projectile_bounds = projectile.getWorldBounds()

        if (sprite_bounds.v1.x < projectile_bounds.v3.x) and (sprite_bounds.v3.x > projectile_bounds.v1.x) and (
                sprite_bounds.v1.y < projectile_bounds.v3.y) and (sprite_bounds.v3.y > projectile_bounds.v1.y):
            return True
        return False

    #def behaviour_tree(self, enemy, data):
        #if self.data.player.midpoint.x >= enemy.position.x - 10:
            #enemy.enemy_movement(enemy, data)
