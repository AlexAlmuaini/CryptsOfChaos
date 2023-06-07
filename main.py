
"""
The main entrypoint script.

This script sets the game's settings up before then creating a
new instance of a PyASGE game. It will then continue to run the
game until the signal to exit is given.
"""
import pyasge
from game.game import MyASGEGame
from game.gamestates.gamestate import GameStateID
from game.gamestates.gameplay import GamePlay
from game.gamestates.gamemenu import GameMenu
from game.gamestates.gamewon import GameWon
from game.gamestates.gameover import GameOver


def main() -> None:
    # set up the game settings first
    settings = pyasge.GameSettings()
    settings.window_width = 1920
    settings.window_height = 1080
    settings.fixed_ts = 50
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.WINDOWED
    settings.vsync = pyasge.Vsync.ENABLED
    settings.msaa_level = 8
    settings.mag_filter = pyasge.MagFilter.LINEAR
    settings.window_title = "MyASGEGame"

    # start the game
    game = MyASGEGame(settings)

    try:
        game.run()
    except KeyboardInterrupt:
        game.signal_exit()
    finally:
        game.signal_exit()

    exit(0)


if __name__ == "__main__":
    print(f"Launching MyASGEGame!!!")
    main()
