from datetime import timedelta, datetime

from dop_game.core_types import SystemId, PlayerId, BuildingId, ShipId
from dop_game import generics as _, star_system
from dop_game.math_helpers import fibonacci


def get_owning_player(game_data, system_id: SystemId) -> PlayerId | None:
    system = get_system(game_data, system_id)
    return star_system.get_owning_player(system)


def list_buildings(game_data, system_id: SystemId) -> dict[BuildingId, int]:
    system = get_system(game_data, system_id)
    return star_system.list_buildings(system)


def list_ships(game_data, system_id: SystemId) -> dict[ShipId, int]:
    system = get_system(game_data, system_id)
    return star_system.list_ships(system)


def get_production_status(game_data, user_id: PlayerId, system_id: SystemId):
    system = get_system(game_data, system_id)
    if star_system.get_owning_player(system) != user_id:
        # can't view other players' production status
        return None
    return star_system.get_production_status(system)


def build_infrastructure(
    game_data, user_id: PlayerId, system_id: SystemId, building_id: BuildingId
):
    if get_owning_player(game_data, system_id) != user_id:
        # can't build on other players' systems
        return
    if get_production_status(game_data, user_id, system_id):
        # only one concurrent production allowed
        return

    system = get_system(game_data, system_id)
    system_out = star_system.build_infrastructure(system, building_id)
    return _.set(game_data, ["star_systems_by_id", system_id], system_out)


def build_ship(game_data, user_id: PlayerId, system_id: SystemId, ship_id: ShipId):
    raise NotImplementedError()


def send_fleet(
    game_data,
    user_id: PlayerId,
    src_id: SystemId,
    dst_id: SystemId,
    ships: dict[ShipId, int],
):
    raise NotImplementedError()


def colonize(game_data, user_id: PlayerId, src_id: SystemId, dst_id: SystemId):
    raise NotImplementedError()


def get_home_system(game_data, player_id: PlayerId) -> SystemId:
    raise NotImplementedError()


def list_fleets(game_data, player_id: PlayerId):
    raise NotImplementedError()


def get_system(game_data, system_id: SystemId):
    return _.get(game_data, ["star_systems_by_id", system_id])
