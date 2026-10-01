# rosters_2026-10-01 — provenance

Built 2026-10-01 ~13:51 EDT in Google Colab (GEO is unreachable from both the cloud
container and the local shell: gateway policy denial, 403 on CONNECT to
ftp.ncbi.nlm.nih.gov).

## What built what

- `classify_rosters_v2_as_built.py` — THE SCRIPT THAT WROTE THESE ROSTERS.
  md5 0cd10cd9f5122ef9811782ac01415fba. Rows 6 and 14/15 already fixed; row 12 confirmed.
- `classify_rosters_v3_guarded.py` — NOT used for these rosters. Adds the empty-arm guard
  and a complete EXPECT table. md5 2345fbaf5ab33e4205e720f51e3816f7. USE THIS ONE NEXT TIME.

## Verified, read back from the written CSVs

950 cases, 359 controls, 90 excluded. 1,399 distinct GSM ids, zero duplicates, zero
unassigned in any row. Every file is n+1 lines (header + records).

| series | row | cases | controls | excluded | n |
|---|---|---|---|---|---|
| GSE174647 | 6 | 182 | 28 | 0 | 210 |
| GSE256539 | 8 | 152 | 68 | 0 | 220 |
| GSE10334 | 10 | 183 | 64 | 0 | 247 |
| GSE35007 | 12 | 190 | 31 | 90 | 311 |
| GSE134662 | 13 | 44 | 10 | 0 | 54 |
| GSE57338 | 14/15 | 177 | 136 | 0 | 313 |
| GSE6710 | 17 | 13 | 13 | 0 | 26 |
| GSE16161-GPL570 | 18 | 9 | 9 | 0 | 18 |

CSV columns: `gsm,group,value,row,query`. `group` is one of case / control / excluded.

## Three things a later reader needs

1. The FIRST run of this classifier was wrong on three of eight rows. The dry run (no
   `--confirm`) caught all three. Never run `--confirm` first.
2. GSE57338 is the POSITIVE CONTROL — already built in control 2, answer known in advance.
   It returned 0 cases on the first run. It is the reason the rest is trustworthy.
3. Row 10's 183/64 split is this run's FIRST determination. `RR_ROWSET_RESOLVED` recorded
   only the 247 total. Nothing independent stands behind the split.

See `RR_ROSTERS_BUILT_2026-10-01` and the corrected `RR_ROWSET_RESOLVED_2026-09-30`.


## 2026-10-01 15:50 EDT: row 10 (GSE10334) split independently confirmed

The 183 case / 64 control split was this run's own first determination. It is now confirmed against a second, independent field: the GEO series record's Overall Design text, written by the submitter, states "a total of 247 samples (from 183 diseased and 64 healthy sites)" from 90 patients (63 chronic, 27 aggressive periodontitis). The classifier read the characteristics value field, so the two sources are different fields that agree.

Supporting but not counted as proof: a per-sample tally of titles ending "Affected site" / "Unaffected site" via a summarizing fetch tool returned 183 / 64 of 247. Per-sample GSM-level agreement between title and roster was NOT checked: the series matrix could not be fetched (NCBI is blocked from both shells and the browser pane refused the site). If a matrix copy turns up, compare titles to roster groups by GSM.

EXPECT comment for GSE10334 in classify_rosters_v3_guarded.py updated accordingly (backup .bak_2026-10-01T1550). Rosters unchanged.

## 2026-10-01 16:00 EDT: row 4 (eflornithine / neuroblastoma) third-series search, CLOSED NEGATIVE

Searched for a third neuroblastoma series with a same-series control arm. None qualifies:
- Bulk: the field's standard design pairs tumor-only series (GSE16476, GSE14880, GSE16237, GSE13136, GSE62564) with normal adrenal from SEPARATE series (GSE3526, GSE7307, GSE8514). Per Springer Hum Genet 2024 (doi 10.1007/s00439-024-02700-2), GSE3526 is the only mixed accession they used and it holds normal tissues only, no tumors. Cross-series controls are barred by the benchmark's same-series rule.
- Single-nucleus atlases (adrenal + neuroblastoma in one series) exist, but whole normal adrenal is cortex-dominated, so the contrast would measure tissue composition, not disease. Not admissible as a disease-vs-control signature.
- The NCBI GEO pages could not be read directly this session (bot check on fetch, browser pane refused), so this rests on published descriptions of the deposits, not on the deposits themselves.

Reason, for the paper: the tissue of origin (embryonic sympathoadrenal neuroblast) is not collectible as a pediatric surgical control, so no same-series normal arm is ever deposited. Same thesis as rows 3, 4, 7 and the kidney query: the deposit lacks the contrast the indication needs. n stays 8.
