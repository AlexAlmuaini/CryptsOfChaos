import pyasge
from game.gamedata import GameData
from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID

class GameWon(GameState):
    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.id = GameStateID.WINNER_WINNER
        self.transition = 0

        self.background = pyasge.Sprite()
        self.background_midpoint = pyasge.Point2D(self.background.x + 960, self.background.y + 540)
        if self.background.loadTexture("data/textures/win state background.png"):
            self.background.z_order = -100
            self.background.scale = 3

        if self.data.difficulty >= 7:
            self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/Kenney Future.ttf", 64)
            self.win_text = pyasge.Text(self.data.fonts["MainFont"])
            self.win_text.string = "YOU KILLED THEM ALL"
            self.win_text.position = [100, 100]
            self.win_text.colour = pyasge.COLOURS.HOTPINK

            self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/Kenney Future.ttf", 32)
            self.play_option = pyasge.Text(self.data.fonts["MainFont"])
            self.play_option.string = ">Play Again"
            self.play_option.position = [100, 200]
            self.play_option.colour = pyasge.COLOURS.HOTPINK
        else:
            self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/Kenney Future.ttf", 64)
            self.win_text = pyasge.Text(self.data.fonts["MainFont"])
            self.win_text.string = "Wave Cleared"
            self.win_text.position = [100, 100]
            self.win_text.colour = pyasge.COLOURS.HOTPINK

            self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/Kenney Future.ttf", 32)
            self.play_option = pyasge.Text(self.data.fonts["MainFont"])
            self.play_option.string = ">Next Level"
            self.play_option.position = [100, 200]
            self.play_option.colour = pyasge.COLOURS.HOTPINK

        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/Kenney Future.ttf", 32)
        self.exit_option = pyasge.Text(self.data.fonts["MainFont"])
        self.exit_option.string = " Main Menu"
        self.exit_option.position = [400, 200]
        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        map_mid = [
            self.data.game_map.width * self.data.game_map.tile_size[0] * 0.5,
            self.data.game_map.height * self.data.game_map.tile_size[1] * 0.5
        ]
        self.camera = pyasge.Camera(map_mid, self.data.game_res[0], self.data.game_res[1])
        self.camera.zoom = 1
        self.camera.lookAt(self.background_midpoint)
        self.menu_option = 0

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        pass

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED:
            if event.key == pyasge.KEYS.KEY_RIGHT or event.key == pyasge.KEYS.KEY_LEFT:
                self.menu_option = 1 - self.menu_option
                if self.data.difficulty >= 7:
                    if self.menu_option == 0:
                        self.play_option.string = ">Play Again"
                        self.play_option.colour = pyasge.COLOURS.HOTPINK
                        self.exit_option.string = " Main Menu"
                        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    else:
                        self.play_option.string = " Play Again"
                        self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                        self.exit_option.string = ">Main Menu"
                        self.exit_option.colour = pyasge.COLOURS.HOTPINK
                else:
                    if self.menu_option == 0:
                        self.play_option.string = ">Next Level"
                        self.play_option.colour = pyasge.COLOURS.HOTPINK
                        self.exit_option.string = " Main Menu"
                        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    else:
                        self.play_option.string = " Next Level"
                        self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                        self.exit_option.string = ">Main Menu"
                        self.exit_option.colour = pyasge.COLOURS.HOTPINK
            if event.key == pyasge.KEYS.KEY_ENTER:
                if self.menu_option == 0:
                    self.transition = 1
                else:
                    self.transition = 2
        pass

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        pass

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        self.camera.lookAt(self.background_midpoint)
        self.camera.zoom = 1
        self.update_inputs()
        if self.transition == 1 and self.data.difficulty != 7:
            self.data.difficulty += 1
            return GameStateID.GAMEPLAY
        elif self.transition == 1 and self.data.difficulty == 7:
            self.data.difficulty = 1
            return GameStateID.GAMEPLAY
        elif self.transition == 2:
            return GameStateID.START_MENU
        return GameStateID.WINNER_WINNER

    def update_inputs(self):
        """ This is purely example code to show how gamepad events
        can be tracked """
        if self.data.gamepad.connected:
            if self.data.gamepad.DPAD_RIGHT and not self.data.prev_gamepad.DPAD_RIGHT \
                    or self.data.gamepad.DPAD_LEFT and not self.data.prev_gamepad.DPAD_LEFT:
                self.menu_option = 1 - self.menu_option
                if self.data.difficulty >= 7:
                    if self.menu_option == 0:
                        self.play_option.string = ">Play Again"
                        self.play_option.colour = pyasge.COLOURS.HOTPINK
                        self.exit_option.string = " Main Menu"
                        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    else:
                        self.play_option.string = " Play Again"
                        self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                        self.exit_option.string = ">Main Menu"
                        self.exit_option.colour = pyasge.COLOURS.HOTPINK
                else:
                    if self.menu_option == 0:
                        self.play_option.string = ">Next Level"
                        self.play_option.colour = pyasge.COLOURS.HOTPINK
                        self.exit_option.string = " Main Menu"
                        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    else:
                        self.play_option.string = " Next Level"
                        self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                        self.exit_option.string = ">Main Menu"
                        self.exit_option.colour = pyasge.COLOURS.HOTPINK

            if self.data.gamepad.A and not self.data.prev_gamepad.A:
                if self.menu_option == 0:
                    self.transition = 1
                else:
                    self.transition = 2

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setProjectionMatrix(self.camera.view)
        self.data.renderer.render(self.background)
        self.data.renderer.render(self.win_text)
        self.data.renderer.render(self.play_option)
        self.data.renderer.render(self.exit_option)
