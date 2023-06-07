import pyasge
from game.gamedata import GameData
from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID


class GameOver(GameState):
    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.id = GameStateID.GAME_OVER
        self.transition = False
        self.menu_option = 0

        self.background = pyasge.Sprite()
        self.background_midpoint = pyasge.Point2D(self.background.x + 960, self.background.y + 540)
        if self.background.loadTexture("/data/textures/game_over_background.jpg"):
            self.background.z_order = -100
            self.background.scale = 1

        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/Kenney Future.ttf", 64)
        self.lose_text = pyasge.Text(self.data.fonts["MainFont"])
        self.lose_text.string = "GAME OVER?"
        self.lose_text.position = [100, 100]
        self.lose_text.colour = pyasge.COLOURS.CHARTREUSE

        self.play_option = pyasge.Text(self.data.fonts["MainFont"])
        self.play_option.string = ">REPLAY"
        self.play_option.position = [100, 400]
        self.play_option.colour = pyasge.COLOURS.HOTPINK

        self.exit_option = pyasge.Text(self.data.fonts["MainFont"])
        self.exit_option.string = "EXIT"
        self.exit_option.position = [500, 400]
        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        self.background_midpoint = pyasge.Point2D(self.background.x + 960, self.background.y + 540)
        map_mid = [
            self.data.game_map.width * self.data.game_map.tile_size[0] * 0.5,
            self.data.game_map.height * self.data.game_map.tile_size[1] * 0.5
        ]
        self.camera = pyasge.Camera(map_mid, self.data.game_res[0], self.data.game_res[1])
        self.camera.zoom = 1



    def click_handler(self, event: pyasge.ClickEvent) -> None:
        pass

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED:
            if event.key == pyasge.KEYS.KEY_RIGHT or event.key == pyasge.KEYS.KEY_LEFT:
                self.menu_option = 1 - self.menu_option
                if self.menu_option == 0:
                    self.play_option.string = "> REPLAY"
                    self.play_option.colour = pyasge.COLOURS.HOTPINK
                    self.exit_option.string = " EXIT"
                    self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                else:
                    self.play_option.string = " REPLAY"
                    self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    self.exit_option.string = " > EXIT"
                    self.exit_option.colour = pyasge.COLOURS.HOTPINK
            if event.key == pyasge.KEYS.KEY_ENTER:
                if self.menu_option == 0:
                    self.transition = True
                else:
                    exit(0)

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        pass

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> None:
        self.camera.lookAt(self.background_midpoint)
        self.camera.zoom = 1
        self.update_inputs()
        if self.transition:
            return GameStateID.GAMEPLAY
        pass

    def update_inputs(self):
        """ This is purely example code to show how gamepad events
        can be tracked """
        if self.data.gamepad.connected:
            if self.data.gamepad.DPAD_RIGHT and not self.data.prev_gamepad.DPAD_RIGHT \
                    or self.data.gamepad.DPAD_LEFT and not self.data.prev_gamepad.DPAD_LEFT:
                self.menu_option = 1 - self.menu_option
                if self.menu_option == 0:
                    self.play_option.string = ">START"
                    self.play_option.colour = pyasge.COLOURS.HOTPINK
                    self.exit_option.string = " EXIT"
                    self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                else:
                    self.play_option.string = " START"
                    self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    self.exit_option.string = " >EXIT"
                    self.exit_option.colour = pyasge.COLOURS.HOTPINK

            if self.data.gamepad.A and not self.data.prev_gamepad.A:
                if self.menu_option == 0:
                    self.transition = True
                else:
                    exit(0)

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setViewport(pyasge.Viewport(0, 0, self.data.game_res[0], self.data.game_res[1]))
        self.data.renderer.setProjectionMatrix(self.camera.view)
        self.data.renderer.render(self.background)
        self.data.renderer.render(self.lose_text)
        self.data.renderer.render(self.play_option)
        self.data.renderer.render(self.exit_option)
