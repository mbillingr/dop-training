from dop_game.core_types import PlayerId, SystemId


def is_defeated(player_data, player_id: PlayerId) -> bool:
    raise NotImplementedError()


def get_home_system(player_data, player_id: PlayerId) -> SystemId:
    raise NotImplementedError()


def list_fleets(player_data, player_id: PlayerId):
    raise NotImplementedError()
