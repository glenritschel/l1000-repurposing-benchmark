# L1000 retrospective repurposing benchmark: code, pre-registration and data (version 2)

Companion to version 2 of "Building the benchmark is harder than running it" (Ritschel, 2026),
concept DOI 10.5281/zenodo.23071560. Sole author: Glen Charles Ritschel, ORCID 0009-0006-5341-8840.

## Result in one line
Seven cases; mean percentile 0.387 against a permutation null of 0.501 (sd 0.087, 10,000
permutations); p = 0.098. The pre-registered criterion (p < 0.05) was not met.

## Contents
- `paper/` the version 2 manuscript, as Markdown and as the PDF built from it.
- `preregistration/` the prediction, committed 2026-10-01 15:47 EDT before any score, and its three
  addenda, each written before any score existed. Their SHA-256 values are in MANIFEST_SHA256.txt.
- `notebooks/` in run order:
  1. `RR_BENCHMARK_control0_and_control2.ipynb` library activity control, dataset survey, and the
     null-query control (median rho +0.0994 over 20 healthy splits; void threshold 0.5).
  2. `phaseA` full-landmark library build, drug ID resolution, series survey. No scoring.
  3. `phaseB1` first signature freeze. **Superseded by B1b**; kept because two of its defects
     (tacrolimus reference formula, misspelled donor field) are reported in the paper.
  4. `phaseB1b` corrected drug IDs, donor-level rows 6 and 8, re-freeze. No scoring.
  5. `phaseB2` the scoring run against the B1b freeze.
  6. `phaseB3` exact tie audit and the declared mesenchymal-only (ASC) secondary; re-checks B2 first.
- `controls/` six controls on the connectivity score (Section 8.1 of the paper), rewritten against
  the deposited scoring function, with the output of the run. Requires numpy only.
- `rosters/` per-series case and control assignments (1,399 GEO samples), the classifier that built
  them and its guarded successor, and their provenance notes.
- `frozen_inputs_and_results/` the scored signatures and drug IDs (SHA-256 1457464f...54e9) and the
  scored result (SHA-256 cba003b1...f42d).
- `results/` the result record.

## To reproduce
Notebooks run in Google Colab and read and write `MyDrive/RitschelResearch/benchmark/`. Phase A
slices the public CMap LINCS 2020 level-5 matrix remotely (about 20 to 60 minutes) and downloads
the public GEO series it needs. Place `signatures_frozen_B1b.json` in that folder to run B2 and B3
directly against the frozen inputs; B2 refuses any other file.

## Data sources
CMap LINCS 2020 (clue.io). GEO series GSE174647, GSE256539, GSE10334, GSE35007, GSE57338,
GSE6710 and GSE16161 (platform GPL570). All public.

## License
Code and text CC BY 4.0, matching the paper.
