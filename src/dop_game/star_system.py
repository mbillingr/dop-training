from dop_game.core_types import SystemId, PlayerId, BuildingId, ShipId


def get_owning_player(system_data, system_id: SystemId) -> PlayerId | None:
    raise NotImplementedError()


def list_buildings(system_data, system_id: SystemId):
    raise NotImplementedError()


def list_ships(system_data, system_id: SystemId):
    raise NotImplementedError()


def get_production_status(system_data, user_id: PlayerId, system_id: SystemId):
    raise NotImplementedError()


def build_infrastructure(
    system_data, user_id: PlayerId, system_id: SystemId, building_id: BuildingId
):
    raise NotImplementedError()


def build_ship(system_data, user_id: PlayerId, system_id: SystemId, ship_id: ShipId):
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
