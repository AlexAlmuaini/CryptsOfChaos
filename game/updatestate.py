""" This file is useless. In the worksheet we imported this file as the update function in the game.py
 but we already had and update function in game.py so we weren't calling this anywhere.
 I moved the code over and now it works."""
import pyasge
from game.gamestates.gamestate import GameStateID
from game.gamestates.gameplay import GamePlay
from game.gamestates.gamemenu import GameMenu
from game.gamestates.gamewon import GameWon
from game.gamestates.gameover import GameOver


def update(self, game_time: pyasge.GameTime) -> None:
    new_state = self.current_state.update(game_time)
    if self.current_state.id != new_state:
        if new_state is GameStateID.START_MENU:
            self.current_state = GameMenu(self.data)
        elif new_state is GameStateID.GAMEPLAY:
            self.current_state = GamePlay(self.data)
        elif new_state is GameStateID.WINNER_WINNER:
            self.current_state = GameWon(self.data)
        elif new_state is GameStateID.GAME_OVER:
            self.current_state = GameOver(self.data)