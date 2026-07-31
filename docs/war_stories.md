# War Stories — Bugs that taught me something
---

## WS-001: Inverted birthday comparison in age calculation
**Date:** 2026-07-13 | **Block:** 0
**Bug:** `age = today.year - birth.year - (1 if (today.month, today.day) >= ... else 0)`
The comparison was inverted: subtracted 1 when birthday HAD passed, not when it hadn't.
**Why tests passed:** Only test patient (Luis, 1958-11-01) was far from the boundary —
membership in the >60 list was correct by coincidence (67 real vs 68 calculated, both >60).
**Root cause:** Single test data point far from edge cases.
**Habit change:** Always test boundaries: birthday today, tomorrow, yesterday.