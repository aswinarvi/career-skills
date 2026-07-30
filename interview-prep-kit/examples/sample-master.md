# Interview Prep — Senior Flutter Engineer @ ExampleCo

Prepared 2026-07-30 · depth: `standard` · Detected seniority: **Senior** (JD asks 5+ yrs, resume shows 6) · Recon: DSA-light loop reported, plan shifted toward system design.

| Category | Planned | Written |
|---|---|---|
| Behavioral | 16 | 16 |
| Technical by topic | 18 | 18 |
| System design | 8 | 8 |

## 1. How to Use This Doc & Answer Frameworks

Read §2–§3 tonight, rehearse the *Story Bank* out loud tomorrow. Framework legend:

- **[STAR]** Situation → Task → Action → Result — behavioral default
- **[CAR]** Challenge → Action → Result — screening rounds
- **[PPF]** Present → Past → Future — "tell me about yourself" only

> Legend: `(verify)` = confirm this detail · `(reported — source, year)` = found in recon · `(inferred)` = reasoned guess.

## 5. Behavioral

#### Ownership

**B1. Tell me about a time you owned a risky release end-to-end.** `[STAR]` `(reported — Glassdoor, 2025)`
**Suggested answer:** At [employer], I owned the staged rollout of the payments SDK migration (verify)...
*Follow-ups:*
- What would you do differently?
- How did you decide the rollback threshold?

## 7. Technical Deep-Dive by JD Topic

### T1. State Management (BLoC) — Explainer  [P0]

Predictable state container pattern separating events from UI.
**Core concepts:** events, states, `Bloc` vs `Cubit`, `BlocProvider`, stream transformers, testing with `blocTest`.
**In this role:** ExampleCo's order screen is latency-sensitive — expect rebuild-scope questions, not trivia.
**Pitfalls & gotchas:**
- Emitting states after `close()`
- Overusing a single giant bloc

#### T1 Questions

**T1.1 When would you pick Cubit over Bloc, and when would you reverse that?**
**Suggested answer:** Cubit for simple, direct state mutations; Bloc when event traceability matters...

## 14. Day-Before & Day-Of Checklist

- [ ] Re-read §2 and §3
- [x] Print questions to ask
- [ ] PPF warm-up, 90 seconds, out loud

---

```dart
// isolate example the T3 answer references
final result = await compute(parseOrders, rawJson);
```

*End of sample.*
