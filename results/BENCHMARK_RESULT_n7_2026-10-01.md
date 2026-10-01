# L1000 retrospective repurposing benchmark: RESULT (pre-registered, n = 7)

**Scored 2026-10-01 ~16:48 EDT.** Inputs: `signatures_frozen_B1b.json`, SHA-256 1457464f...54e9, checked before scoring. Output `B2_result.json`, SHA-256 cba003b1...f42d. Pre-registration 7eee1779...c9a2 with addenda v1.1 (39eab5db...), v1.2 (6c6c7f16...), v1.3 (3ab117f0...). The row 6 guard ran before any score and passed (no zero-spot sample entered a donor mean).

## Verdict

**Observed mean percentile 0.3870. Null mean 0.5006, sd 0.0873, 10,000 permutations. Permutation p = 0.0985. Criterion (p < 0.05): NOT MET.**

Per the pre-registration, this is an underpowered instrument and a null result does not refute the pipeline; it must not be reported as doing so. The direction is favorable (1.3 null standard deviations below the null mean) and the test does not reach the pre-registered threshold.

## Per row (lower percentile = stronger reversal)

| row | drug | percentile | library exact-zero fraction | note |
|---|---|---|---|---|
| 6 MS CNS | cladribine | 0.650 | 0.281 | wrong side of the median |
| 8 PAH lung | tadalafil | 0.299 | 0.312 | 11 vs 5 donors, 633 landmarks |
| 10 gingiva | doxycycline | 0.504 | 0.329 | its two tautomer IDs split 0.731 and 0.277 |
| 12 blood | hydroxyurea | **0.176** | 0.393 | top 20% |
| 14/15 HF myocardium | dapagliflozin, empagliflozin, spironolactone | 0.536 | 0.347 | **resolution-free: the row score is the tie-block midrank** |
| 17 psoriasis skin | cyclosporin-a | **0.154** | 0.342 | top 20%; its five IDs range 0.004 to 0.266 |
| 18 AD skin | tacrolimus | 0.389 | 0.286 | two of four IDs sit in the tie block |

## What the pre-registration requires to be reported regardless of outcome

- **Ties (exact, from Phase B3).** 6 of 19 scored drug IDs sit on the tied block: dapagliflozin, empagliflozin, two of three spironolactone IDs, two of four tacrolimus IDs. **6 of 7 cases resolve off the tied block; only 14/15 does not.** Tie-block midranks run 0.461 to 0.536 by row, not exactly 0.5.
- **Wrong-direction scores.** Cladribine scores +0.018 (mimics the MS signature). The two doxycycline tautomer IDs disagree in sign (-0.035 and +0.046).
- **ASC-only secondary (declared in v1 Section 9).** 4 of 7 drugs have no ASC signature. Scored rows: 14/15 0.197, 17 0.254, 18 0.816. Mean 0.423, null 0.497 (sd 0.149), p = 0.32. Reported, not gating.
- **Calcineurin inhibitors.** Both calcineurin rows (17 cyclosporin, 18 tacrolimus) fall below 0.5, and cyclosporin is the strongest result in the set. Two rows of one drug class are not independent evidence for the pipeline.
- **Unscored compounds:** 7,994 of 34,419 LINCS compounds have no QC-passing exemplar signature and are not in the 26,425-compound library.
- **Limitations already declared:** row 12's tissue is blood; rows 6 and 8 are spatial data averaged to donor (13 vs 4 and 11 vs 5 donors); row 8 uses 633 of 978 landmarks; n is 7 after six exclusions, each on a deposit or gate ground recorded before scoring.

## Where this leaves the paper

The thesis stands and is now complete: building the benchmark was harder than running it. Thirteen candidate rows became seven, every reduction on a deposit ground, and five defects were caught before any score existed: three roster rules by a dry run and a positive control, and the tacrolimus formula and the misspelled donor field by reading the freeze report. The run itself took one pass. The pre-registered answer is a null at p = 0.098 from an instrument that could not have been large enough to say much either way.
