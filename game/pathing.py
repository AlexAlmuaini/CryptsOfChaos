"""
This is the pathfinding script.

You will need to complete the resolve function in order to
get movement to work correctly. You should start with
BFS and consider more advanced approaches if you have time.

The function will take a player's mouse click and return a
list of tile locations it needs to visit in order to get
to its destination.

note: you should also use this pathfinding function for task4
"""

from queue import Queue

import pyasge
from game.gamedata import GameData
from typing import Protocol, Dict, List, Iterator, Tuple, TypeVar, Optional
import heapq

T = TypeVar('T')
Location = TypeVar('Location')


def resolve(xy: pyasge.Point2D, enemy: pyasge.Point2D, data: GameData):
    """
    Resolves the path needed to get to the destination point.

    Making use of the cost map, a suitable search algorithm should
    be used to create a series of tiles that the ship may pass
    through. These tiles should then be returned as a series of
    positions in world space.

    :param xy: The destination for the ship
    :param data: The game data, needed for access to the game map
    :return: list[pyasge.Point2D]
    """

    # convert point to tile location
    tile_loc = data.game_map.tile(xy)
    enemy_loc = data.game_map.tile(enemy)
    tile_cost = data.game_map.costs[tile_loc[1]][tile_loc[0]]
    # use these to make sure you don't go out of bounds when checking neighbours

    # here's an example of tiles that the player should visit
    tiles_to_visit = []

    if tile_cost == 1:
        temp = breadth_first_search(data, enemy_loc, tile_loc)
        coordinate_list = reconstruct_path(temp, enemy_loc, tile_loc)
        for coordinates in coordinate_list:
            tiles_to_visit.append(data.game_map.world(coordinates))

    # return a list of tile positions to follow
    path = []
    for tile in tiles_to_visit:
        path.append(tile)
    return path


def breadth_first_search(data, start: Location, goal: Location):
    map_width = data.game_map.width
    map_height = data.game_map.height
    frontier = Queue()
    frontier.put(start)
    came_from: Dict[Location, Optional[Location]] = {start: None}

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in neighbors(data, current, map_width, map_height):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from


def neighbors(data, current, map_width, map_height) -> List:
    children = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares
        # Get node position
        node_position = (current[0] + new_position[0], current[1] + new_position[1])
        # Make sure within range
        if node_position[0] > map_width - 1 or node_position[0] < 0 or node_position[1] > map_height - 1 or \
                node_position[1] < 0:
            continue
        # Make sure walkable terrain
        if data.game_map.costs[node_position[1]][node_position[0]] > 100:
            continue
        # Append
        children.append(node_position)
    return children


def reconstruct_path(came_from: Dict[Location, Location],
                     start: Location, goal: Location) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:  # note: this will fail if no path found
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path
