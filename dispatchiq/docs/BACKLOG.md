# DispatchIQ — Full Product Backlog

Complete business requirements, epics, and user stories with acceptance criteria. This is the detailed reference; see [`../CLAUDE.md`](../CLAUDE.md) for the short summary.

## Product Vision
A local delivery dispatch platform that lets customers request deliveries, matches them to available drivers efficiently, prices dynamically based on demand, and gives ops visibility into the whole flow.

Deliberately designed so five classic interview algorithm patterns are load-bearing parts of the product (Epic 4), each with real precedent in production systems at companies like Uber, DoorDash, and Instacart:
- **Sliding Window** → surge pricing (rolling order volume per zone)
- **Hash Map** → no duplicate driver assignment (atomic order→driver map)
- **Graph BFS/DFS** → zone reachability given road closures
- **Heap / Priority Queue (Top-K)** → nearest available drivers
- **Dynamic Programming (Knapsack)** → optimal package loading under vehicle capacity

---

## Epic 1: Accounts & Auth
**Business context:** Three distinct user types (customer, driver, admin) need separate onboarding flows and permission levels.

### STORY 1.1 — Customer signup/login
*As a customer, I want to create an account and log in, so I can place delivery orders.*
- AC1: Email/password signup with verification email.
- AC2: Session persists across app restarts (token-based auth).
- AC3: Password reset flow available.

### STORY 1.2 — Driver signup with verification
*As a driver, I want to sign up and submit verification info (license, vehicle info), so I can be approved to accept deliveries.*
- AC1: Driver account is in "pending" state until admin approves.
- AC2: Driver cannot go "available" or receive orders until approved.
- AC3: Rejected applications include a reason and allow resubmission.

### STORY 1.3 — Role-based access control
*As an admin, I want customers, drivers, and admins to only access what's relevant to their role, so the system stays secure and uncluttered.*
- AC1: Driver-only endpoints (accept order, update location) reject non-driver tokens.
- AC2: Admin dashboard routes reject non-admin tokens.
- AC3: Role is enforced server-side, not just hidden client-side.

---

## Epic 2: Order Lifecycle
**Business context:** The core transaction — a customer needs something delivered, and the system needs to track it from creation to completion.

### STORY 2.1 — Create a delivery order
*As a customer, I want to enter pickup/dropoff details and request a delivery, so a driver can be dispatched.*
- AC1: Order requires pickup address, dropoff address, and package description.
- AC2: Order is quoted a price (see Epic 5) before customer confirms.
- AC3: Order enters "searching for driver" state immediately after confirmation.

### STORY 2.2 — Order state machine
*As a system, orders need to move through well-defined states, so every part of the app can trust what stage an order is in.*
- AC1: States: `created → searching → assigned → picked_up → in_transit → delivered` (plus `cancelled` from any pre-`picked_up` state).
- AC2: Invalid transitions (e.g., `delivered → assigned`) are rejected at the API level.
- AC3: Every state transition is timestamped and stored for later audit/analytics.

### STORY 2.3 — Cancel an order
*As a customer, I want to cancel an order before it's picked up, so I'm not charged for a delivery I no longer need.*
- AC1: Cancellation allowed only in `created`, `searching`, or `assigned` states.
- AC2: If a driver was already assigned, they're notified and released back to available.
- AC3: Cancellation fee applies if cancelled after driver assignment (business rule, configurable).

---

## Epic 3: Driver Onboarding & Availability
**Business context:** Drivers need a simple way to signal when they're working and what they can carry.

### STORY 3.1 — Toggle availability
*As a driver, I want to mark myself available/unavailable, so I only receive order offers when I'm actually working.*
- AC1: Toggle updates driver status instantly; unavailable drivers are excluded from dispatch candidate pools.
- AC2: Going unavailable mid-delivery does not cancel the active delivery — only affects new assignments.

### STORY 3.2 — Vehicle profile
*As a driver, I want to specify my vehicle type and capacity, so I'm only offered orders I can actually carry.*
- AC1: Profile includes vehicle type (bike/car/van) and max weight/volume.
- AC2: Orders exceeding a driver's capacity are excluded from their offers.

---

## Epic 4: Dispatch & Routing Engine ⭐
**Business context:** Given an incoming order, the system must efficiently find and assign the best available driver, prevent double-booking, respect road/zone closures, price fairly based on real-time demand, and help drivers optimize what they carry.

### STORY 4.1 — Surge pricing based on rolling order volume
*As a business, I want delivery prices to increase automatically when demand spikes in a short time window, so we can incentivize more drivers to come online during peak periods.*
**Pattern: Sliding Window**
- AC1: Track order count per zone over a rolling 15-minute window (sliding, not fixed-bucket, so a spike at :07 and :22 aren't averaged into meaninglessness).
- AC2: When order count in the window exceeds a threshold, apply a surge multiplier to new order quotes in that zone.
- AC3: Multiplier decays smoothly as the window's order count drops, rather than snapping instantly to 1x.
- AC4: Includes a test simulating a burst of orders followed by a lull, asserting the surge rises and falls correctly as the window slides.

### STORY 4.2 — Prevent duplicate driver assignment
*As a dispatcher, I want the system to guarantee no two drivers are ever assigned to the same order, so we don't pay for redundant deliveries or confuse customers.*
**Pattern: Hash Map**
- AC1: Maintain a hash map of order ID → assigned driver ID as the single source of truth for active assignments.
- AC2: Assignment is an atomic check-and-set against the map (no read-then-write race condition between two dispatch workers).
- AC3: Attempting to assign an already-assigned order returns a conflict error, not a silent overwrite.
- AC4: Includes a concurrency test simulating two simultaneous assignment attempts on the same order, asserting only one succeeds.

### STORY 4.3 — "Can this driver reach this zone" reachability check
*As a dispatcher, I want to know whether a driver can actually reach a delivery zone given current road closures, so we don't assign undeliverable orders.*
**Pattern: Graph Traversal (BFS/DFS)**
- AC1: Model zones/road segments as a graph; closures remove edges dynamically.
- AC2: Given a driver's current zone and an order's destination zone, run BFS to determine reachability and shortest hop-count path.
- AC3: If unreachable, the order is excluded from that driver's candidate list rather than assigned and later failed.
- AC4: Graph updates (closures reopening, etc.) are reflected in the next dispatch cycle without requiring a service restart.

### STORY 4.4 — Nearest available drivers (Top-K)
*As a dispatcher, I want to see the top 5 nearest available drivers for a new order, so I can offer it to the best candidates first instead of scanning the entire driver list.*
**Pattern: Heap / Priority Queue (Top-K)**
- AC1: Given a new order location and a set of available drivers, maintain a max-heap (or min-heap of negated distances) of size 5 to find nearest drivers without sorting the full driver pool.
- AC2: Offer goes to driver #1; on decline/timeout, automatically falls through to #2–5 in order.
- AC3: Newly available drivers are incorporated into future queries without requiring a full recompute of all driver distances.
- AC4: Load test demonstrates this scales sub-linearly better than full-sort for 500+ concurrent drivers.

### STORY 4.5 — Optimal package loading under vehicle capacity
*As a driver, I want the app to tell me the best combination of packages to take on one trip given my vehicle's weight/volume limit, so I maximize deliveries per trip.*
**Pattern: Dynamic Programming (Knapsack)**
- AC1: Given a list of pending packages (weight, delivery-priority score) and a vehicle capacity, compute the subset maximizing total priority score without exceeding capacity.
- AC2: Solved via DP, with documented complexity and a fallback greedy heuristic for extremely large package pools (e.g., >500 items) where exact DP is impractical.
- AC3: High-priority (e.g., time-sensitive) packages are weighted so the DP doesn't just optimize for raw count.
- AC4: Test suite includes a case demonstrating the DP solution outperforms a naive greedy-by-weight approach in total priority score.

---

## Epic 5: Pricing Engine
**Business context:** Price needs to reflect distance, demand, and vehicle type — and be shown to the customer *before* they confirm.

### STORY 5.1 — Base quote calculation
*As a customer, I want to see a price quote before confirming my order, so there are no surprises.*
- AC1: Quote = base fare + distance-based fare + surge multiplier (from Story 4.1).
- AC2: Quote is locked for 60 seconds after being shown; re-quoted if the customer takes longer to confirm.

### STORY 5.2 — Driver payout calculation
*As a driver, I want to see how much I'll earn for a delivery before accepting it, so I can decide whether it's worth it.*
- AC1: Payout shown on the offer screen includes base pay + any surge bonus.
- AC2: Payout is guaranteed once accepted, even if surge multiplier changes mid-delivery.

---

## Epic 6: Tracking & Notifications
**Business context:** Customers and drivers both need real-time visibility into an active delivery.

### STORY 6.1 — Live order tracking
*As a customer, I want to see my driver's live location and ETA, so I know when my delivery will arrive.*
- AC1: Driver location updates at least every 10 seconds while `in_transit`.
- AC2: ETA recalculates as location updates arrive.

### STORY 6.2 — Push notifications on state changes
*As a customer, I want to be notified when my order is assigned, picked up, and delivered, so I don't have to keep checking the app.*
- AC1: Notification fires on each state transition from Story 2.2.
- AC2: Notifications are also available in-app as a fallback if push fails.

---

## Epic 7: Admin/Ops Dashboard
**Business context:** Ops needs visibility into what's happening across the whole system, and the ability to intervene.

### STORY 7.1 — Live order map
*As an admin, I want to see all active orders and driver locations on a map, so I can monitor operations in real time.*
- AC1: Map shows all orders in `searching`/`assigned`/`in_transit` states.
- AC2: Clicking an order shows its full state history (from Story 2.2's audit log).

### STORY 7.2 — Manual reassignment
*As an admin, I want to manually reassign an order to a different driver, so I can intervene when a driver goes offline unexpectedly.*
- AC1: Reassignment releases the current driver and re-runs the Story 4.4 nearest-driver logic.
- AC2: Action is logged with the admin's ID for accountability.

### STORY 7.3 — Driver approval queue
*As an admin, I want to review and approve/reject pending driver applications (from Story 1.2), so only vetted drivers join the platform.*
- AC1: Queue shows all `pending` drivers with submitted verification docs.
- AC2: Approve/reject action updates driver state and triggers a notification to the applicant.

---

## Suggested Sprint Plan (2-week sprints)

| Sprint | Focus | Stories |
|---|---|---|
| 0 — Setup | Project scaffolding, CI, data models | — |
| 1 — Accounts | Auth for all three roles | 1.1, 1.2, 1.3 |
| 2 — Core Order Flow | Order creation & lifecycle (simple assignment, no smart dispatch yet) | 2.1, 2.2, 2.3, 3.1, 3.2 |
| 3 — Dispatch Engine | The algorithmic core — headline sprint | 4.2, 4.4, 4.3 |
| 4 — Pricing & Capacity | Surge pricing + load optimization | 4.1, 4.5, 5.1, 5.2 |
| 5 — Tracking & Notifications | Real-time UX polish | 6.1, 6.2 |
| 6 — Admin & Ops | Operational visibility and control | 7.1, 7.2, 7.3 |

Sprint 3 is the one to over-invest in for interview storytelling — hash maps, graphs, and heaps all work together to solve one coherent problem (matching a driver to an order).
