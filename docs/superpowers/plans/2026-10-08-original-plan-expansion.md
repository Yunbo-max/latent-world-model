# Original-plan expansion implementation plan

The owner has already authorized implementation and independent source review; this is a non-interactive Work continuation. Native implementation by root, independent reviewers on separate scopes. Web does not execute project code/tests.

Goal: implement the closed constructions in rounds/full-plan-2026-10-08/EXPANSION_SPEC.md through actual training, generation, restore and native comparison paths; preserve v0.

- [x] Review mathematical/interfaces and author source before corresponding implementation.
- [x] Add immutable CPU event/receipt storage and deterministic causal retrieval in src/lwm/episodic.py; tests pin FIFO, digest conflicts, replay and serialization.
- [x] Add retrieved-token reader, optional plan/realize and restricted contractive core to model.py with defaults preserving v0; tests pin causality, row parity, trainable paths and dynamics assumptions.
- [x] Wire stores/provenance/clocks into generation and checkpoint restore; tests pin whole-chunk exactly-once acceptance and branch isolation.
- [x] Wire stores/predictive CE into trainer and validation with main/auxiliary denominator separation; tests pin writer gradients, no future-state edge and resumed state identity.
- [x] Add expanded/native cost logging and complete configs/command matrices; preserve all original input/scorer acquisition and native denominators.
- [x] Independently source-review complete integrated revision, address concrete findings, parse without project execution.
- [ ] Reconcile live main, publish non-force expected-parent revision and read every changed file at that exact commit.

Review focus: future-query leaks; masked SFT targets; evicted-event replay; mixed-origin partial segment restore; old checkpoint default-field compatibility. Tests are authored for Local, not Web red/green receipts. There is no new-method admission or claimed empirical novelty in this engineering expansion.

These marks denote authored/reviewed source coverage; publication checkbox is closed only by the exact remote readback reported by integration. Runtime tests remain unexecuted.
