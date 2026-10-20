# Copy-Trading Executor Requirements (R1-R5)

Product requirements for a production copy-trading bot on Polymarket,
written as a checklist you can turn straight into issues.

Companion post: https://brainresearchhub.net/research/sdk/polymarket-copy-trading

## R1. Copy the decision, not the trade
- A whale's fill at 0.54 is information; your market order at 0.61 is a
  different position.
- Slippage bound per copy action; **skip-not-chase** when the book moved
  beyond it.
- Copy by **proportion** of the tracker's sizing, never absolute size.

## R2. Reconciliation beats re-fetching
- After any order action, reconcile from the order/user channel.
- No polling loops against REST after writes — bursts are how rate budgets
  die. See: https://brainresearchhub.net/research/sdk/polymarket-rate-limits

## R3. Kill switch with a human-readable trigger list
- Daily loss cap, tracker-stale threshold, manual flag — minimum set.
- Every automated failure lands in the log the switch reads.
- Design notes: https://brainresearchhub.net/research/sdk/kill-switch-design

## R4. Session keys with scoped spend
- No hot keys in the executor. Scoped session keys with spend caps keep a
  bug from becoming a drain.
- Patterns: https://brainresearchhub.net/research/sdk/session-key-safety

## R5. The compliance envelope is a product feature
- On a CFTC-regulated venue: geofencing, KYC state, market eligibility are
  pre-trade checks in the executor, not user documentation.
- US specifics: https://brainresearchhub.net/research/access/polymarket-us-kyc

## What we do not ship
- Copying short-window markets (resolution drift kills the tracker's edge).
- Blind retry loops on order placement (non-idempotent writes).
- Trusting displayed tracker PnL — derive from on-chain fills.

## Decision gate
See `copy_gate.py` — R1/R3 compressed into one function that gates every
copy action. `KILL` pages a human.

---
*Not financial advice. Educational purposes only.*
