# Copilot Workspace Instructions

## ✅ Mandatory Development Checklist

Before committing any changes:

- [ ] `uv run ruff check .` — lint passes with no errors
- [ ] `uv run uvicorn app.main:app --port 8000` — app starts successfully
- [ ] `uv run pytest` — all tests pass

## Project Overview

**Soc Ops** is a Social Bingo game (FastAPI + Jinja2 + HTMX). Players mark a 5×5 board by finding people matching each prompt; first to 5-in-a-row wins.

## Architecture

```
app/
├── main.py          # FastAPI routes — all POST endpoints return HTML partials (not JSON)
├── game_service.py  # GameSession dataclass + in-memory session store (_sessions dict)
├── game_logic.py    # Pure functions: generate_board, toggle_square, check_bingo
├── models.py        # Pydantic models: GameState (StrEnum), BingoSquareData, BingoLine
├── data.py          # QUESTIONS list (add prompts here only)
└── templates/components/  # HTMX partial responses returned by each route
```

## Key Patterns

- **HTMX partials**: every POST (`/start`, `/toggle/{id}`, `/reset`, `/dismiss-modal`) returns a component from `templates/components/`, never a full page
- **Immutable board**: `BingoSquareData` is frozen — `toggle_square()` and `generate_board()` always return new lists
- **Sessions**: `GameSession` lives in `_sessions` dict (in-memory); always access via `_get_game_session(request)` in routes, never instantiate directly
- **Logic separation**: pure game logic in `game_logic.py`, session orchestration in `game_service.py`, routing only in `main.py`
- **CSS**: custom utility classes (Tailwind-like) in `app/static/css/app.css` — no external CSS framework
