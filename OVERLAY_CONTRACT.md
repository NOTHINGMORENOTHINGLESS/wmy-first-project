# MatchLens — Overlay Data Contract

The narrative output emitted by this pipeline is designed for broadcast overlay rendering.

Each narrative object contains:
- `timestamp`: broadcast clock in MM:SS format
- `trigger_event_id`: the event that triggered this narrative
- `narratives`: three modes — `casual_fan`, `analyst`, `former_player`
- `overlay.zone_highlight`: the pitch zone to highlight
- `overlay.player_highlight`: array of player IDs to highlight
- `overlay.duration_seconds`: how long to display the overlay

This contract is stable and can be consumed by any graphics renderer without transformation.
