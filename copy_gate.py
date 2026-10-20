"""copy-gate: minimal decision gate for copy-trading executors.

Policy, not execution: every copied order passes through gate() and the
verdict ('EXECUTE' | 'SKIP' | 'KILL') is enforced by the order router.
KILL is a kill-switch signal and must page a human, not just log.

Author: Marcus Webb. MIT License. Not financial advice.
"""
from __future__ import annotations

import time

__all__ = ["gate", "GateConfig"]

MAX_SLIPPAGE = 0.03          # skip if book moved > 3c past tracker fill
MAX_ORDER_USD = 250.0        # per-copy notional cap (proportion, not whale size)
DAILY_LOSS_CAP = 500.0       # kill-switch trigger on realized PnL
MIN_TRACKER_FRESHNESS = 300  # seconds since followed address last acted


def gate(
    book_mid: float,
    tracker_price: float,
    usd: float,
    secs_since_tracker: int | None = None,
    realized_pnl_today: float = 0.0,
    tracker_ts: float | None = None,
) -> str:
    """Return 'EXECUTE' | 'SKIP' | 'KILL' for one copy signal.

    Order of checks is severity order: kill conditions first, then
    staleness (stale intel is not your edge), then slippage, then sizing.
    """
    if realized_pnl_today <= -DAILY_LOSS_CAP:
        return "KILL"
    if secs_since_tracker is None and tracker_ts is not None:
        secs_since_tracker = int(time.time() - tracker_ts)
    if secs_since_tracker is None or secs_since_tracker > MIN_TRACKER_FRESHNESS:
        return "SKIP"
    if abs(book_mid - tracker_price) > MAX_SLIPPAGE:
        return "SKIP"
    if usd > MAX_ORDER_USD:
        return "SKIP"
    return "EXECUTE"
