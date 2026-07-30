# DispatchIQ

Local delivery dispatch platform. Customers request deliveries, drivers get matched to orders, pricing adjusts with demand, admins get operational visibility.

Full requirements, all epics, and every story's acceptance criteria: **[`docs/BACKLOG.md`](./docs/BACKLOG.md)**. Point me there for clarifying questions.

## Headline: Dispatch & Routing Engine (Epic 4)

Five classic interview algorithm patterns, each solving a real dispatch problem:

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

## Status
Requirements/backlog complete. Build in progress (see `main.py`).
