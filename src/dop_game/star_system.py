from datetime import timedelta, datetime

from dop_game.core_types import SystemId, PlayerId, BuildingId, ShipId
from dop_game import generics as _
from dop_game.math_helpers import fibonacci


def get_owning_player(system_data) -> PlayerId | None:
    return _.get(system_data, ["owning_player"])


def list_buildings(system_data) -> dict[BuildingId, int]:
    return _.get(system_data, ["buildings"])


def list_ships(system_data) -> dict[ShipId, int]:
    return _.get(system_data, ["ships"])


def get_production_status(system_data):
    return _.get(system_data, ["building_slot"])


def build_infrastructure(system_data, building_id: BuildingId):
    n_built = _.sum(list_buildings(system_data))
    duration = timedelta(minutes=fibonacci(n_built))
    eta = datetime.now() + duration

    event_out = {"eta": eta, "kind": building_id}
    return _.set(system_data, ["building_slot"], event_out)


def build_ship(system_data, user_id: PlayerId, ship_id: ShipId):
    raise NotImplementedError()


def send_fleet(
    system_data,
    user_id: PlayerId,
    src_id: SystemId,
    dst_id: SystemId,
    ships: dict[ShipId, int],
):
    raise NotImplementedError()


def colonize(system_data, user_id: PlayerId, src_id: SystemId, dst_id: SystemId):
    raise NotImplementedError()
