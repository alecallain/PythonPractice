# PythonPractice

This repo is dedicated to me delving back into the world of Python since college. The flagship project here is **DispatchIQ** — see below.

## DispatchIQ

A local delivery dispatch platform (customers request deliveries, drivers get matched to orders, pricing adjusts with real-time demand, admins get operational visibility) — think a scaled-down Uber/DoorDash dispatch backend. Code lives in [`dispatchiq/`](./dispatchiq).

### Why this project exists

Technical interviews lean heavily on a handful of classic algorithm patterns (LeetCode/HackerRank style), but it's rare to see them applied anywhere close to a real production codebase. This project closes that gap: a genuinely useful application where five of the most commonly-tested patterns are actual, load-bearing parts of the product — not toy functions bolted on for show.

| Pattern | Where it lives in this app |
|---|---|
| Sliding Window | Surge pricing — rolling order volume per zone |
| Hash Map | Preventing duplicate driver assignment |
| Graph Traversal (BFS/DFS) | Zone reachability given road closures |
| Heap / Priority Queue (Top-K) | Finding the nearest available drivers |
| Dynamic Programming (Knapsack) | Optimal package loading under vehicle capacity |

Each pattern has a direct real-world precedent — dispatch/routing problems like these show up in public engineering writeups from Uber, DoorDash, and Instacart.

Full requirements and every user story's acceptance criteria: [`dispatchiq/docs/BACKLOG.md`](./dispatchiq/docs/BACKLOG.md).

### Authorship

**All application code in this repository is written by me.**

AI (Claude) was used exclusively in three non-coding roles during planning:
- **Product Owner** — defining the product concept and business requirements
- **Business Analyst** — writing epics, user stories, and acceptance criteria
- **Quality Engineer** — reviewing requirements for testability and flagging edge cases/acceptance criteria gaps

AI did not write, generate, or refactor any code in this project.

### Status

🚧 Early development — requirements and backlog are complete; implementation is in progress.
