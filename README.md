# copy-gate

Minimal decision gate for a copy-trading executor on Polymarket: the policy
checks that run before every copied order. Requirements-first, in the spirit of
"copy the decision, not the trade."

Author: Marcus Webb — fintech product lead, formerly Robinhood and Kalshi.
Companion research: https://brainresearchhub.net/research/sdk/polymarket-copy-trading

## The requirements encoded here

- R1: skip-not-chase — slippage bound vs the tracker's fill price
- R2: proportion sizing — copy by fraction, never by absolute whale size
- R3: kill switch trigger — daily loss cap checked on every signal
- Staleness guard — do not act on intel older than N seconds

Full requirement writeup (R1-R5, including session-key scoping and the
compliance envelope): https://brainresearchhub.net/research/sdk/kill-switch-design
and https://brainresearchhub.net/research/sdk/session-key-safety

## Usage

```python
from copy_gate import gate

verdict = gate(
    book_mid=0.58, tracker_price=0.54, usd=120.0,
    secs_since_tracker=45, realized_pnl_today=-120.0,
)
# 'EXECUTE' | 'SKIP' | 'KILL'  ->  KILL pages the human
```

Tune the constants to your risk budget. The gate is policy, not execution:
wire its verdicts into your order router and your kill switch.

## Files

- `copy_gate.py` — the decision gate (stdlib only)
- `requirements.md` — the full R1-R5 requirements checklist
- `LICENSE` — MIT

## Disclaimer

Not financial advice. Educational purposes only.
