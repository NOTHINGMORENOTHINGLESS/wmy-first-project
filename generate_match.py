#!/usr/bin/env python3
"""Generate a deterministic synthetic 90-minute football match as JSON.

Usage:
  python generate_match.py --seed 42
  python generate_match.py --seed 42 --output match.json
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List


def fictional_player(name: str, player_id: str, role: str, pace: int, passing: int, pressing: int, x: float, y: float) -> Dict[str, Any]:
    return {
        "player_id": player_id,
        "name": name,
        "role": role,
        "attributes": {
            "pace": pace,
            "passing": passing,
            "pressing": pressing,
        },
        "start_position": {"x": x, "y": y},
    }


def build_team(team_id: str, team_name: str, possession_style: float, press_style: float, focus_side: str) -> Dict[str, Any]:
    players = [
        fictional_player("Milo Voss", f"{team_id}-1", "GK", 70, 58, 50, 5, 50),
        fictional_player("Tariq Den", f"{team_id}-2", "RB", 72, 63, 64, 16, 18),
        fictional_player("Evan Sorel", f"{team_id}-3", "CB", 62, 61, 67, 28, 40),
        fictional_player("Nico Rale", f"{team_id}-4", "CB", 63, 60, 68, 28, 60),
        fictional_player("Jules Arden", f"{team_id}-5", "LB", 68, 65, 60, 16, 82),
        fictional_player("Omar Saye", f"{team_id}-6", "CM", 74, 78, 69, 40, 34),
        fictional_player("Luca Venn", f"{team_id}-7", "RW", 92, 70, 66, 78, 16),
        fictional_player("Ilan Brox", f"{team_id}-8", "CM", 76, 80, 70, 44, 50),
        fictional_player("Dorian Vale", f"{team_id}-9", "ST", 79, 73, 68, 78, 50),
        fictional_player("Kian Sato", f"{team_id}-10", "AM", 80, 84, 72, 62, 50),
        fictional_player("Rafi Duran", f"{team_id}-11", "LW", 94, 72, 67, 78, 84),
    ]

    if team_id == "HCF":
        players[1]["name"] = "Rafe Querol"
        players[5]["name"] = "Bruno Keel"
        players[7]["name"] = "Cian Ors"
        players[10]["name"] = "Leno Ardy"
        players[1]["attributes"]["pace"] = 63
        players[4]["attributes"]["pace"] = 61
        players[6]["attributes"]["pace"] = 94
        players[10]["attributes"]["pace"] = 95
        players[6]["role"] = "RW"
        players[10]["role"] = "LW"
        players[7]["role"] = "CM"

    if team_id == "RCF":
        players[1]["name"] = "Marek Hyl"
        players[4]["name"] = "Ivo Cale"
        players[6]["name"] = "Nilo Fenn"
        players[10]["name"] = "Theo Brask"
        players[1]["attributes"]["pace"] = 76
        players[4]["attributes"]["pace"] = 79
        players[6]["attributes"]["pace"] = 88
        players[10]["attributes"]["pace"] = 90
        players[7]["role"] = "CM"

    return {
        "team_id": team_id,
        "team_name": team_name,
        "formation": "4-3-3",
        "possession_style": possession_style,
        "press_style": press_style,
        "focus_side": focus_side,
        "players": players,
    }


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def make_event(
    minute: float,
    event_type: str,
    team: str,
    player_id: str,
    start: Dict[str, float],
    end: Dict[str, float],
    related_player_id: str | None = None,
    outcome: str | None = None,
    tags: List[str] | None = None,
    details: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    event: Dict[str, Any] = {
        "minute": round(minute, 2),
        "team": team,
        "event_type": event_type,
        "player_id": player_id,
        "start": {"x": round(start["x"], 2), "y": round(start["y"], 2)},
        "end": {"x": round(end["x"], 2), "y": round(end["y"], 2)},
    }
    if related_player_id:
        event["related_player_id"] = related_player_id
    if outcome:
        event["outcome"] = outcome
    if tags:
        event["tags"] = tags
    if details:
        event.update(details)
    return event


def generate_match(seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    home = build_team("HCF", "Harbor City FC", possession_style=0.78, press_style=0.58, focus_side="right")
    away = build_team("RCF", "Redstone City FC", possession_style=0.52, press_style=0.74, focus_side="left")

    possession = "HCF"
    home_possession = 58
    away_possession = 42

    events: List[Dict[str, Any]] = []
    first_half_events = []
    second_half_events = []

    event_count = 0
    for minute in range(0, 90):
        if minute == 60:
            shift = {
                "minute": 60.0,
                "team": "HCF",
                "event_type": "tactical_shift",
                "details": {
                    "from_side": "right",
                    "to_side": "left",
                    "trigger": "zone_shift",
                    "summary": "Harbor City switch attacking focus from the right flank to the left flank after halftime.",
                },
                "tags": ["zone_shift"],
                "start": {"x": 50.0, "y": 50.0},
                "end": {"x": 50.0, "y": 50.0},
            }
            events.append(shift)

        # Phase Tactics: possession-based teams pass more; high press teams create more pressure events.
        if minute < 60:
            attack_team = "HCF" if possession == "HCF" else "RCF"
            if attack_team == "HCF":
                own_team = home
                opp_team = away
                press_bias = 0.18
                pass_weight = 0.60
            else:
                own_team = away
                opp_team = home
                press_bias = 0.35
                pass_weight = 0.45
        else:
            if possession == "HCF":
                own_team = home
                opp_team = away
                press_bias = 0.22
                pass_weight = 0.56
            else:
                own_team = away
                opp_team = home
                press_bias = 0.30
                pass_weight = 0.42

        # Switch attack focus at minute 60.
        if minute >= 60:
            home["focus_side"] = "left"
            own_team = home if possession == "HCF" else away
            if own_team["team_id"] == "HCF":
                focus_side = "left"
            else:
                focus_side = "right"
        else:
            focus_side = "right"

        # Generate a natural rhythm of events for each minute.
        event_step = rng.random()
        if event_step < 0.12:
            team_choice = "HCF" if rng.random() < home_possession / 100 else "RCF"
            team = home if team_choice == "HCF" else away
            if team_choice == "HCF":
                player = team["players"][9]
                target = team["players"][10]
            else:
                player = team["players"][9]
                target = team["players"][6]
            pass_event = make_event(
                float(minute) + rng.uniform(0.05, 0.95),
                "pass",
                team["team_name"],
                player["player_id"],
                start={"x": clamp(player["start_position"]["x"] + rng.uniform(-8, 8), 0, 100), "y": clamp(player["start_position"]["y"] + rng.uniform(-10, 10), 0, 100)},
                end={"x": clamp(target["start_position"]["x"] + rng.uniform(-5, 5), 0, 100), "y": clamp(target["start_position"]["y"] + rng.uniform(-8, 8), 0, 100)},
                related_player_id=target["player_id"],
                outcome="complete",
                tags=["possession"] if team["team_id"] == "HCF" else ["build_up"],
                details={"pass_type": "short" if rng.random() < 0.65 else "switch"},
            )
            events.append(pass_event)
            event_count += 1

        if event_step >= 0.12 and event_step < 0.34:
            team = home if rng.random() < 0.55 else away
            team_data = home if team == home else away
            press_player = team_data["players"][rng.randrange(2, 10)]
            opponent_player = away["players"][rng.randrange(2, 10)] if team is home else home["players"][rng.randrange(2, 10)]
            press_x = 64 if team_data["team_id"] == "HCF" else 36
            press_y = 50 if rng.random() < 0.5 else 70 if team_data["team_id"] == "HCF" else 30
            pressure_event = make_event(
                float(minute) + rng.uniform(0.1, 0.9),
                "pressure",
                team_data["team_name"],
                press_player["player_id"],
                start={"x": clamp(press_x + rng.uniform(-8, 8), 0, 100), "y": clamp(press_y + rng.uniform(-8, 8), 0, 100)},
                end={"x": clamp(press_x + rng.uniform(-10, 10), 0, 100), "y": clamp(press_y + rng.uniform(-10, 10), 0, 100)},
                related_player_id=opponent_player["player_id"],
                outcome="won" if team_data["press_style"] > 0.65 else "contained",
                tags=["press"],
                details={"zone": "opponent_half" if team_data["team_id"] == "HCF" else "final_third"},
            )
            if team_data["team_id"] == "HCF" and minute >= 60:
                pressure_event["tags"].append("zone_shift")
            events.append(pressure_event)
            event_count += 1

        if event_step >= 0.34 and event_step < 0.42:
            team = home if rng.random() < 0.58 else away
            team_data = home if team is home else away
            tackler = team_data["players"][rng.randrange(1, 10)]
            victim = away["players"][rng.randrange(1, 10)] if team is home else home["players"][rng.randrange(1, 10)]
            tackle_event = make_event(
                float(minute) + rng.uniform(0.2, 0.8),
                "tackle",
                team_data["team_name"],
                tackler["player_id"],
                start={"x": clamp(40 + rng.uniform(-10, 10), 0, 100), "y": clamp(50 + rng.uniform(-15, 15), 0, 100)},
                end={"x": clamp(35 + rng.uniform(-10, 10), 0, 100), "y": clamp(50 + rng.uniform(-15, 15), 0, 100)},
                related_player_id=victim["player_id"],
                outcome="won",
                tags=["defensive_recovery"],
                details={"challenge_type": "slide" if rng.random() < 0.4 else "standing"},
            )
            events.append(tackle_event)
            event_count += 1

        if event_step >= 0.42 and event_step < 0.50:
            # possession transitions are intentionally weighted by style.
            team = home if rng.random() < (home_possession / 100) else away
            team_data = home if team is home else away
            possession_event = make_event(
                float(minute) + rng.uniform(0.1, 0.9),
                "possession_change",
                team_data["team_name"],
                team_data["players"][rng.randrange(0, 11)]["player_id"],
                start={"x": 50.0, "y": 50.0},
                end={"x": 50.0, "y": 50.0},
                outcome="gain",
                tags=["turnover"],
                details={"new_possession": team_data["team_name"], "reason": "recover" if rng.random() < 0.6 else "interception"},
            )
            events.append(possession_event)
            possession = team_data["team_id"]
            if possession == "HCF":
                home_possession = clamp(home_possession + 4, 40, 70)
                away_possession = 100 - home_possession
            else:
                away_possession = clamp(away_possession + 4, 40, 70)
                home_possession = 100 - away_possession
            event_count += 1

        if event_step >= 0.50 and event_step < 0.57:
            team = home if rng.random() < 0.58 else away
            team_data = home if team is home else away
            shooter = team_data["players"][rng.randrange(6, 11)]
            shot_x = 80 if team_data["team_id"] == "HCF" else 20
            shot_y = 48 + rng.uniform(-22, 22)
            shot_event = make_event(
                float(minute) + rng.uniform(0.2, 0.9),
                "shot",
                team_data["team_name"],
                shooter["player_id"],
                start={"x": clamp(shooter["start_position"]["x"], 0, 100), "y": clamp(shooter["start_position"]["y"], 0, 100)},
                end={"x": shot_x, "y": shot_y},
                outcome="on_target" if rng.random() < 0.5 else "off_target",
                tags=["final_third"],
                details={"zone": "right" if team_data["team_id"] == "HCF" and minute < 60 else "left" if team_data["team_id"] == "HCF" else "central"},
            )
            if team_data["team_id"] == "HCF" and minute >= 60:
                shot_event["tags"].append("zone_shift")
            events.append(shot_event)
            event_count += 1

    # Add the needed demo patterns explicitly to ensure they are visible in the output.
    pace_mismatch_event = make_event(
        41.4,
        "pass",
        "Harbor City FC",
        "HCF-11",
        start={"x": 72.0, "y": 78.0},
        end={"x": 90.0, "y": 58.0},
        related_player_id="HCF-2",
        outcome="complete",
        tags=["pace_mismatch", "left_flank", "fast_winger"],
        details={
            "summary": "Fast winger beats the slow full-back down the flank using pace and direct running.",
            "winger_id": "HCF-11",
            "full_back_id": "HCF-2",
            "winger_pace": 95,
            "full_back_pace": 61,
        },
    )
    events.append(pace_mismatch_event)

    zone_shift_event = make_event(
        60.5,
        "pass",
        "Harbor City FC",
        "HCF-10",
        start={"x": 52.0, "y": 52.0},
        end={"x": 76.0, "y": 82.0},
        related_player_id="HCF-11",
        outcome="complete",
        tags=["zone_shift", "left_flank"],
        details={
            "summary": "The team pivots from the right flank to the left flank as the winger becomes the primary outlet.",
            "from_side": "right",
            "to_side": "left",
        },
    )
    events.append(zone_shift_event)

    # Sort events by minute and keep a stable order.
    events.sort(key=lambda item: (float(item["minute"]), item["event_type"]))

    match = {
        "seed": seed,
        "match_id": f"synthetic-{seed:06d}",
        "duration_minutes": 90,
        "teams": {
            "home": {
                "team_id": home["team_id"],
                "team_name": home["team_name"],
                "formation": home["formation"],
                "players": home["players"],
            },
            "away": {
                "team_id": away["team_id"],
                "team_name": away["team_name"],
                "formation": away["formation"],
                "players": away["players"],
            },
        },
        "patterns": {
            "pace_mismatch": {
                "active": True,
                "flank": "left",
                "winger_id": "HCF-11",
                "full_back_id": "HCF-2",
                "trigger_minute": 41.4,
                "description": "Fast winger attacks the slow full-back on the left side.",
            },
            "zone_shift": {
                "active": True,
                "minute": 60.0,
                "from_side": "right",
                "to_side": "left",
                "description": "Harbor City switches attacking focus from right to left after halftime.",
            },
        },
        "events": events,
    }
    return match


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a deterministic 90-minute synthetic football match JSON.")
    parser.add_argument("--seed", type=int, required=True, help="Integer seed for deterministic generation.")
    parser.add_argument("--output", type=str, default="-", help="Path to save JSON output. Use '-' for stdout.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = generate_match(args.seed)
    json_text = json.dumps(payload, indent=2)

    if args.output == "-":
        print(json_text)
        return

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json_text + "\n", encoding="utf-8")
    print(f"Wrote synthetic match JSON to {out_path}")


if __name__ == "__main__":
    main()
