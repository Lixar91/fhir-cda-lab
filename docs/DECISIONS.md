# Architecture Decision Records (ADR)
> Format: ADR (Architecture Decision Record). Each decision gets a context, the decision itself, and the consequences.
> Only NON-OBVIOUS decisions live here. If the code explains it, it doesn't.

---

## ADR-001: Canonical model normalizes absence at the extraction boundary
**Date:** 2026-07-28 | **Block:** 1 — interop parsing
**Status:** Accepted

**Context:**
Different wire formats encode "no data" differently:
- JSON (patients.json): P003 has NO "conditions" key
- XML (patients.xml): P002 has `<conditions/>` (empty element), P003 has none
- Consumers downstream (patient_utils) shouldn't have to guess which keys exist

**Decision:**
`extract_patients()` always emits ALL four keys for every patient.
Collections that are known-empty → `[]` (not `None`, not absent).
Scalars that are absent → `""` (empty string, not `None`, not missing key).

**Consequences:**
- Consumers can rely on a stable contract: `patient["conditions"]` never raises KeyError
- The "depends on the target system" serialization concern moves to output adapters
- Extraction layer is the single point of normalization

**Alternatives considered:**
- Replicate source dirtiness (omit keys when source omits them) → rejected:
  pushes complexity to every consumer, violates the canonical model principle
