from dop_game import game, star_system
from dop_game.core_types import SystemId


def test_game_get_owning_player():
    game_data = {"star_systems_by_id": {"alpha": {"owning_player": "hotzenplotz"}}}
    player = game.get_owning_player(game_data, SystemId("alpha"))
    assert player == "hotzenplotz"


def test_system_get_owning_player():
    system_data = {"owning_player": "hotzenplotz"}
    player = star_system.get_owning_player(system_data)
    assert player == "hotzenplotz"


def test_game_list_buildings():
    game_data = {
        "star_systems_by_id": {"alpha": {"buildings": {"civilian": 2, "production": 1}}}
    }
    buildings = game.list_buildings(game_data, SystemId("alpha"))
    assert buildings == {"civilian": 2, "production": 1}


def test_system_list_buildings():
    system_data = {"buildings": {"civilian": 2, "production": 1}}
    buildings = star_system.list_buildings(system_data)
    assert buildings == {"civilian": 2, "production": 1}


def test_game_list_ships():
    game_data = {"star_systems_by_id": {"alpha": {"ships": {"fasty": 2, "slowy": 1}}}}
    ships = game.list_ships(game_data, SystemId("alpha"))
    assert ships == {"fasty": 2, "slowy": 1}


def test_system_list_ships():
    system_data = {"ships": {"fasty": 2, "slowy": 1}}
    ships = star_system.list_ships(system_data)
    assert ships == {"fasty": 2, "slowy": 1}
