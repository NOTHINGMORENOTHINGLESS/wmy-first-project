#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def build_match(seed: int):
    teams = [
        {"team_id": "team_alpha", "name": "Team Alpha", "style": "high press"},
        {"team_id": "team_beta", "name": "Team Beta", "style": "low block"},
    ]

    players = [
        {"player_id": "Player_01", "team_id": "team_alpha", "name": "Player_01", "role": "RW", "pace": 92},
        {"player_id": "Player_02", "team_id": "team_alpha", "name": "Player_02", "role": "RB", "pace": 74},
        {"player_id": "Player_03", "team_id": "team_alpha", "name": "Player_03", "role": "CM", "pace": 82},
        {"player_id": "Player_04", "team_id": "team_alpha", "name": "Player_04", "role": "CF", "pace": 83},
        {"player_id": "Player_05", "team_id": "team_alpha", "name": "Player_05", "role": "LB", "pace": 78},
        {"player_id": "Player_06", "team_id": "team_alpha", "name": "Player_06", "role": "DM", "pace": 80},
        {"player_id": "Player_07", "team_id": "team_alpha", "name": "Player_07", "role": "AM", "pace": 84},
        {"player_id": "Player_08", "team_id": "team_alpha", "name": "Player_08", "role": "LW", "pace": 88},
        {"player_id": "Player_09", "team_id": "team_alpha", "name": "Player_09", "role": "ST", "pace": 81},
        {"player_id": "Player_10", "team_id": "team_alpha", "name": "Player_10", "role": "CB", "pace": 72},
        {"player_id": "Player_11", "team_id": "team_beta", "name": "Player_11", "role": "LB", "pace": 69},
        {"player_id": "Player_12", "team_id": "team_beta", "name": "Player_12", "role": "RB", "pace": 63},
        {"player_id": "Player_13", "team_id": "team_beta", "name": "Player_13", "role": "CM", "pace": 74},
        {"player_id": "Player_14", "team_id": "team_beta", "name": "Player_14", "role": "CF", "pace": 80},
        {"player_id": "Player_15", "team_id": "team_beta", "name": "Player_15", "role": "RW", "pace": 85},
        {"player_id": "Player_16", "team_id": "team_beta", "name": "Player_16", "role": "DM", "pace": 78},
        {"player_id": "Player_17", "team_id": "team_beta", "name": "Player_17", "role": "AM", "pace": 82},
        {"player_id": "Player_18", "team_id": "team_beta", "name": "Player_18", "role": "LW", "pace": 87},
        {"player_id": "Player_19", "team_id": "team_beta", "name": "Player_19", "role": "ST", "pace": 79},
        {"player_id": "Player_20", "team_id": "team_beta", "name": "Player_20", "role": "CB", "pace": 72},
    ]

    def add_event(minute, second, event_type, player_id, team_id, start, end, outcome):
        return {
            "timestamp": f"{minute}:{second:02d}",
            "minute": minute,
            "type": event_type,
            "player_id": player_id,
            "team_id": team_id,
            "start_coordinates": [round(float(start[0]), 1), round(float(start[1]), 1)],
            "end_coordinates": [round(float(end[0]), 1), round(float(end[1]), 1)],
            "outcome": outcome,
        }

    events = []

    for minute in range(90):
        if minute % 3 == 0:
            if minute < 60:
                start = [76, 28]
                end = [86, 30]
                player = "Player_01"
            else:
                start = [22, 72]
                end = [12, 70]
                player = "Player_08"
            events.append(add_event(minute, 20, "pass", player, "team_alpha", start, end, "complete"))

        if minute % 4 == 0:
            events.append(add_event(minute, 10, "pressure", "Player_03", "team_alpha", [52, 52], [60, 37], "won"))

        if minute % 5 == 0:
            events.append(add_event(minute, 31, "tackle", "Player_16", "team_beta", [50, 48], [45, 42], "won"))

        if minute % 7 == 0:
            events.append(add_event(minute, 43, "possession_change", "Player_06", "team_alpha", [42, 52], [52, 46], "won"))

        if minute > 20 and minute % 9 == 0:
            events.append(add_event(minute, 46, "shot", "Player_09", "team_alpha", [72, 54], [90, 52], "blocked"))

    pattern_events = [
        (61, 20, "pass", "Player_01", "team_alpha", [82, 28], [88, 32], "complete"),
        (61, 32, "pressure", "Player_01", "team_alpha", [84, 26], [92, 32], "won"),
        (61, 48, "tackle", "Player_12", "team_beta", [18, 18], [22, 26], "won"),
        (62, 18, "pass", "Player_03", "team_alpha", [46, 42], [18, 62], "complete"),
        (62, 36, "pressure", "Player_07", "team_alpha", [62, 38], [30, 62], "won"),
        (62, 52, "pass", "Player_08", "team_alpha", [78, 68], [10, 70], "complete"),
        (63, 22, "pass", "Player_09", "team_alpha", [70, 52], [58, 48], "complete"),
        (63, 41, "pass", "Player_10", "team_alpha", [58, 48], [66, 54], "complete"),
        (63, 54, "pressure", "Player_06", "team_alpha", [48, 52], [68, 50], "won"),
        (64, 18, "pass", "Player_01", "team_alpha", [82, 30], [88, 34], "complete"),
        (64, 39, "pressure", "Player_01", "team_alpha", [86, 30], [92, 38], "won"),
        (64, 50, "tackle", "Player_12", "team_beta", [20, 18], [24, 26], "lost"),
        (65, 14, "pass", "Player_07", "team_alpha", [56, 38], [20, 72], "complete"),
        (65, 36, "pressure", "Player_08", "team_alpha", [76, 72], [12, 70], "won"),
        (65, 48, "pass", "Player_05", "team_alpha", [18, 74], [12, 70], "complete"),
    ]

    for minute, second, event_type, player_id, team_id, start, end, outcome in pattern_events:
        events.append(add_event(minute, second, event_type, player_id, team_id, start, end, outcome))

    events.sort(key=lambda event: (event["minute"], int(event["timestamp"].split(":")[1])))

    pattern_windows = [
        {"minute": 61, "pattern": "pace_mismatch", "patternLabel": "Pace mismatch", "team_id": "team_alpha", "zones": ["Z1", "Z2", "Z4"], "xg": 0.34, "momentum": 68, "narrativeKey": 0},
        {"minute": 62, "pattern": "zone_shift", "patternLabel": "Zone shift", "team_id": "team_alpha", "zones": ["Z7", "Z8", "Z9"], "xg": 0.28, "momentum": 76, "narrativeKey": 1},
        {"minute": 63, "pattern": "one_two", "patternLabel": "One-two", "team_id": "team_alpha", "zones": ["Z5", "Z6", "Z8"], "xg": 0.41, "momentum": 84, "narrativeKey": 2},
        {"minute": 64, "pattern": "pace_mismatch", "patternLabel": "Pace mismatch", "team_id": "team_alpha", "zones": ["Z2", "Z3", "Z4"], "xg": 0.39, "momentum": 88, "narrativeKey": 0},
        {"minute": 65, "pattern": "zone_shift", "patternLabel": "Zone shift", "team_id": "team_alpha", "zones": ["Z7", "Z8", "Z9"], "xg": 0.36, "momentum": 79, "narrativeKey": 1},
    ]

    return {
        "seed": seed,
        "teams": teams,
        "players": players,
        "events": events,
        "pattern_windows": pattern_windows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic football match data.")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic random seed.")
    args = parser.parse_args()

    match = build_match(args.seed)
    output_path = Path(__file__).with_name("match.json")
    output_path.write_text(json.dumps(match, indent=2), encoding="utf-8")
    print(f"Wrote {output_path}")
   
