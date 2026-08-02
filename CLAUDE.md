# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# DispatchIQ

Local delivery dispatch platform. Customers request deliveries, drivers get matched to orders, pricing adjusts with demand, admins get operational visibility.

Full requirements, all epics, and every story's acceptance criteria: **[`docs/BACKLOG.md`](docs/BACKLOG.md)**. Point me there for clarifying questions about scope or acceptance criteria.

## Headline: Dispatch & Routing Engine (Epic 4)

The point of this project: five classic interview algorithm patterns, each solving a real dispatch problem, as load-bearing product code rather than toy functions.

| Pattern | Used for |
|---|---|
| Sliding Window | Surge pricing (rolling order volume per zone) |
| Hash Map | Prevent duplicate driver assignment |
| Graph BFS/DFS | Zone reachability given road closures |
| Heap / Top-K | Nearest available drivers |
| DP (Knapsack) | Optimal package loading under vehicle capacity |

## Epics

1. Accounts & Auth
2. Order Lifecycle
3. Driver Onboarding & Availability
4. Dispatch & Routing Engine ⭐
5. Pricing Engine
6. Tracking & Notifications
7. Admin/Ops Dashboard

Suggested sprint order (see BACKLOG.md for the full table): setup → accounts → core order flow → dispatch engine → pricing/capacity → tracking → admin.

## Repo layout

Application code lives under `dispatchiq/`, but requirements docs live at the repo root:

```
docs/BACKLOG.md          # full requirements — the source of truth for scope/AC
dispatchiq/
  pyproject.toml          # currently empty — no build backend, deps, or tooling configured yet
  src/dispatch/
    __init__.py            # empty
    main.py                 # entry point stub (print-only placeholder so far)
    orderState.py           # OrderState enum + DeliveryOrder — Epic 2 (Order Lifecycle)
  tests/                    # exists, currently empty
```

`README.md` at the repo root explains the project's purpose and an authorship note: application code is written by the user, not AI — AI's role has been limited to planning (product/BA/QE) during requirements writing, not implementation.

## Status / working conventions

- Requirements and backlog are complete; implementation is early and incremental (see commit history — one story/function at a time, e.g. `orderState.py`'s `cancel()` was added as its own commit for Story 2.3).
- No test framework, linter, or build backend is configured yet (`pyproject.toml` is empty, `tests/` is empty). Don't assume `pytest`/`ruff`/etc. are wired up — check `pyproject.toml` before assuming any tooling command works, and ask before introducing new tooling/dependencies.
- Run scripts directly, e.g. `python3 dispatchiq/src/dispatch/main.py`, until a proper package/entry-point setup exists.

## Architecture notes

- `orderState.py` models order lifecycle state as `OrderState` (an `Enum`) plus a `DeliveryOrder` class with a guarded `transition()` method and a narrower `cancel()` convenience method. Both enforce the state machine described in BACKLOG.md Story 2.2/2.3 (e.g. cancellation only from `CREATED`/`SEARCHING`/`ASSIGNED`; no transition into `CANCELLED` from `IN_TRANSIT`/`DELIVERED`). When extending order lifecycle logic, keep new transitions consistent with the AC in Story 2.2 rather than adding ad hoc state checks elsewhere.
- The Epic 4 algorithmic components (sliding window, hash map, graph BFS/DFS, heap, DP) don't exist yet — when they're built, expect them to be the core of the dispatch flow that Epic 2's order lifecycle and Epic 3's driver availability feed into.
