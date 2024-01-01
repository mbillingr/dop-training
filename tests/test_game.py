import pytest

from dop_game import game
from dop_game.core_types import SystemId


def test_get_system():
    game_data = {"star_systems_by_id": {"alpha": {"name": "Alpha Centauri"}}}
    system = game.get_system(game_data, SystemId("alpha"))
    assert system == {"name": "Alpha Centauri"}

    with pytest.raises(LookupError):
        game.get_system(game_data, SystemId("beta"))
