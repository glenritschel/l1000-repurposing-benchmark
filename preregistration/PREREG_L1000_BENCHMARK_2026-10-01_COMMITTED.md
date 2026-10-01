# PRE-REGISTRATION: L1000 retrospective repurposing benchmark. COMMITTED.

**Committed by Glen Ritschel, 2026-10-01 15:47 EDT ("commit now"), before any scoring run.**
Frozen text below. Its SHA-256 is recorded in `ledger/decisions.csv`. Any later change is a new version with its own commit, never an edit to this file.

This is a separate instrument from the outreach prediction register (`predictions.csv`) and does not enter it. The register's hold on new predictions while 33/REPLY is open applies to that register, not to this one (decision recorded 2026-10-01).

Source draft: `RR_PREREG_REVISED_2026-09-30` (project store, corrected 2026-10-01 12:15). Factual updates from 2026-10-01 work are folded in and listed at the end; none touches the criterion.

---

**Prediction, L1000 retrospective repurposing benchmark.**

FDA-approved repurposings that pass all inclusion gates (G1 genuine repurposing, G2 presence in CMap LINCS 2020 with curated pert_id sets, G2b coverage of at least two cell lines, G3 independence of the disease transcriptomics from the repurposing hypothesis) are scored against the frozen L1000 connectivity pipeline. G4 time split is reported per row and is not an inclusion gate.

For each row the pipeline is queried with a disease-versus-control signature from the tissue named in the protocol, and the percentile rank of the approved drug within the scored library is recorded, ascending, so that the strongest reversal is best.

**Criterion, fixed before any scoring run. ONE condition: the permutation p-value is below 0.05.** The statistic is the mean percentile rank of the approved drugs across cases. The null is built by permuting drug labels within the library, preserving the drug-to-query structure, over at least 10,000 permutations.

**Stated in advance:** there is no second condition and in particular no absolute percentile threshold. The connectivity score returns exactly zero for 34.7% of compounds at the compound level, and under the agreed midrank rule every one of those sits at the 50th percentile. A threshold phrased as an absolute percentile, or as a count of drugs beating the tied block, is unreachable for arithmetic reasons alone whatever the pipeline does. At n=8 the old top-20% condition would have been impossible 28.7% of the time; this criterion is impossible 2.4% of the time. The mean percentile rank, the tie count per row, and the number of cases resolving above the tie block are all reported, and none of them gates the result.

**Stated in advance:** the unit of analysis is the query signature. The heart-failure myocardium case has three correct answers, dapagliflozin, empagliflozin and spironolactone, and is scored by their MEDIAN percentile rank, not the best of them.

**Stated in advance, the row set: EIGHT cases, with arms as built and verified 2026-10-01** (rosters at `ledger/rosters_2026-10-01/`, 1,399 distinct GSM ids, zero duplicates, zero unassigned):

| row | query | series | cases | controls | excluded |
|---|---|---|---|---|---|
| 6 | MS CNS | GSE174647 | MS 182 | HI 28 | 0 |
| 8 | PAH lung | GSE256539 | IPAH Lung 152 | Control Lung 68 | 0 |
| 10 | gingiva | GSE10334 | Diseased 183 | Healthy 64 | 0 |
| 12 | blood | GSE35007 | SS 190 | A 19 + AA 12 = 31 | SC 60, AS 30 |
| 13 | GVHD colon | GSE134662 | Onset 22 + Refractory 22 | Control 10 | 0 |
| 14/15 | HF myocardium | GSE57338 | ischemic 95 + dilated CMP 82 | non-failing 136 | 0 |
| 17 | psoriasis skin | GSE6710 | lesional 13 | uninvolved 13 | 0 |
| 18 | AD skin | GSE16161-GPL570 | AD 9 | Normal 9 | 0 |

Row 12: SC is a different genotype and AS is a carrier state; both are excluded from both arms. A and AA are one control group transcribed two ways (interleaved HFS numbering, identical clinical status and severity fields). Row 10's split is confirmed against the GEO series Overall Design text.

**Stated in advance, the five exclusions, each on a gate ground and each recorded before any scoring run:**
- **Row 3, colchicine for ASCVD.** GEO's curated GDS1597 carries one experimental variable, `individual`, 22 patients. No disease state and no lesion grade. Segments are multiple per patient, so even with grades the samples would not be independent.
- **Row 4, eflornithine for neuroblastoma.** GSE2283 has no `!Sample_characteristics` lines at all on either platform and its two-color reference is itself a mixture of human neuroblastoma. The fallback GSE3960 is 101 primary tumors and one Fetal Brain sample. A third-series search (2026-10-01) found no bulk series with a same-series control arm; the field pairs tumor-only series with normal adrenal from separate series, and single-nucleus atlases compare against cortex-dominated whole adrenal.
- **Row 7, sirolimus for LAM.** GSE12027 is 14 LAM nodules against cultured smooth muscle and four Malme-3M, a melanoma cell line. No healthy control.
- **Row 14's kidney query.** GSE104948's control on both platforms is `Tumor Nephrectomy`: 3 samples on GPL22945, 2 on GPL24120. Merging is barred by the platform rule and by probe-set incompatibility. Row 14 survives through its myocardium query.
- **Row 19, baricitinib for COVID-19.** The protocol requires a signature from a named tissue and row 19's tissue is heterogeneous across autopsy sites. An open G3 question also stands against it, since baricitinib for COVID came from a computational screen in early 2020 and both candidate series postdate that.

**Stated in advance, because it is the thing a reader will suspect:** the reachability table is not monotone in n, so under the old criterion n=13 would have been more reachable than n=12. That is a floor-function artifact and it was deliberately not allowed to influence any exclusion. Every exclusion rests on the deposit, and all five were recorded before scoring.

**Stated in advance, the remaining limitations.** Row 12's tissue is blood, which is the diseased tissue for a hemoglobinopathy but not solid tissue. Row 13 is thin on the control side: 10 controls among 54 samples. Row 8 requires pseudobulk aggregation to one value per sample before any contrast; the rest do not. Both strict-G4 rows are gone (row 4 entirely and row 14's second query), so there is no prospective subset to report.

**Stated in advance, the platform-selection rule.** Four series span more than one array platform, and GEO writes one matrix per platform rather than one per series. A multi-platform series is not one dataset. A platform qualifies only if it contains both cases and controls. Among qualifying platforms the single largest by sample count is used, ties broken by landmark coverage and then by lowest GPL number. Platforms are never merged. Landmark coverage and the number of samples left behind are reported per row.

**Stated in advance:** if control 2 shows that the library ranking against a null healthy split correlates with the ranking against the real disease signature at rho above 0.5, this prediction is void. Control 2 has been run and returned a median rho of +0.0994 over 20 splits, 0 of 20 undefined, so the prediction is live.

**Stated in advance: this is an underpowered instrument.** Eight cases, and no amount of correct procedure changes that. A null result does not refute the pipeline and must not be reported as doing so.

---

## Changes from the 2026-10-01 12:15 draft (none touches the criterion)

1. Row-set table added with the built-and-verified arm counts.
2. Row 12's control arm stated as evidence-backed (A == AA), with SC and AS exclusions named.
3. Row 13's limitation corrected: the draft said "15 total series", which was wrong; it is 10 controls among 54 samples.
4. Row 4's exclusion now records the third-series search.
5. The draft's "What still has to happen before this is committed" list is closed: all four items were completed 2026-10-01.
