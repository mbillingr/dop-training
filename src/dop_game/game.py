from datetime import timedelta, datetime

from dop_game.core_types import SystemId, PlayerId, BuildingId, ShipId
from dop_game import generics as _
from dop_game.math_helpers import fibonacci


def get_owning_player(game_data, system_id: SystemId) -> PlayerId | None:
    return _.get(game_data, ["star_systems_by_id", system_id, "owning_player"])


def list_buildings(game_data, system_id: SystemId):
    return _.get(game_data, ["star_systems_by_id", system_id, "buildings"])


def list_ships(game_data, system_id: SystemId):
    return _.get(game_data, ["star_systems_by_id", system_id, "ships"])


def get_production_status(game_data, user_id: PlayerId, system_id: SystemId):
    if get_owning_player(game_data, system_id) != user_id:
        # can't view other players' production status
        return None
    return _.get(game_data, ["star_systems_by_id", system_id, "building_slot"])


def build_infrastructure(
    game_data, user_id: PlayerId, system_id: SystemId, building_id: BuildingId
):
    if get_owning_player(game_data, system_id) != user_id:
        # can't build on other players' systems
        return
    if get_production_status(game_data, user_id, system_id):
        # only one concurrent production allowed
        return
    system = _.get(game_data, ["star_systems_by_id", system_id])

    n_built = _.sum(_.get(system, ["buildings"]))
    duration = timedelta(minutes=fibonacci(n_built))
    eta = datetime.now() + duration

    event_out = {"eta": eta, "kind": building_id}
    system_out = _.set(system, ["building_slot"], event_out)
    game_data_out = _.set(game_data, ["star_systems_by_id", system_id], system_out)
    return game_data_out


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
