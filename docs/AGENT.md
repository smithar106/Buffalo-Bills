# Agent Design

## Concept

BILLS MAFIA AI is a **tool-using agent**, not a prompt-only chatbot.

```
USER QUESTION
      ↓
AGENT
      ↓
PLAN / SELECT TOOLS
      ↓
READ-ONLY TOOLS
      ↓
STRUCTURED EVIDENCE
      ↓
LLM REASONING
      ↓
GROUNDING / VALIDATION
      ↓
ANSWER + SOURCES
```

## Modes

| Mode | Presentation |
|------|--------------|
| `analyst` | Fact-focused, concise, statistics-heavy |
| `bills_mafia` | Energetic Buffalo fan personality, factually grounded |
| `simple` | Explains football concepts without assuming football knowledge |
| `debate` | Analyzes a question from multiple perspectives with evidence |

Modes change **presentation only**. All modes share the same grounded tools and data.

## Tools (read-only)

| Tool | Returns |
|------|---------|
| `get_next_game()` | Next scheduled game |
| `get_schedule(season)` | Season schedule |
| `get_game(game_id)` | Full game details |
| `get_team_stats(season)` | Team statistics |
| `get_player_stats(player, season)` | Player statistics |
| `get_standings()` | AFC East standings |
| `get_roster()` | Active roster |
| `get_injuries()` | Injury report |
| `get_play_by_play(game_id)` | Play-by-play |
| `get_head_to_head(opponent, start_season, end_season)` | Historical matchup |
| `search_bills_news(query)` | News search |
| `get_recent_games(limit)` | Recent results |
| `get_player_game_log(player, season)` | Per-game player log |

All tools return structured JSON with `source`, `retrieved_at`, `season`, and
`game_id` (where relevant).

## Grounding rules

- Numerical/factual claims must originate from tool output.
- Never fabricate statistics, scores, injuries, standings, schedules, transactions,
  quotes, news, or historical results.
- If evidence conflicts, acknowledge the discrepancy.
- Clearly distinguish **facts** (tool data) from **analysis** (LLM).
- Never claim certainty about future outcomes — label predictions as predictions.
- If the system can't verify something:
  > "I couldn't verify that from the available Bills data."

## Safety

- Factual accuracy takes priority over personality.
- Unsupported numerical claims are rejected by the grounding validator.
- The LLM provider is configurable; no credentials are hard-coded.
