from statistics import GameStats
from storage import RuntimeStorage


def test_pvp_turn_results_are_counted():
    stats = GameStats()
    stats.record_result("PVP", winner=1)
    stats.record_result("PVP", winner=2)
    assert (stats.games_played, stats.player_one_wins, stats.player_two_wins) == (2, 1, 1)


def test_storage_round_trip(monkeypatch, tmp_path):
    state_file = tmp_path / "state.json"
    monkeypatch.setattr("storage.STATE_FILE", state_file)
    monkeypatch.setattr("storage.DATA_DIR", tmp_path)
    storage = RuntimeStorage()
    storage.save({"sound": False, "volume": 0.5}, {"games_played": 3})
    assert storage.load()["settings"]["volume"] == 0.5
