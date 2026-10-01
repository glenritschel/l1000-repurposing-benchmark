# Building the benchmark is harder than running it: a pre-registered retrospective benchmark of transcriptomic drug repurposing, from thirteen candidate cases to seven, and a null result

**Glen Charles Ritschel**  
Ritschel Research, Tega Cay, South Carolina, USA  
ORCID 0009-0006-5341-8840  

**Version 2, 2026-10-01.** Version 1 (2026-09-30) scoped the benchmark and reported no result. Version 2 adds the pre-registered run (Section 13) and records every way the run departed from what version 1 described (Section 13.1).

---

## Abstract

Transcriptomic drug repurposing rests on a claim that has never been tested at the only
endpoint that matters: that reversing a disease expression signature identifies compounds that
go on to work in patients. The obvious test is retrospective. Take drugs that were approved for
a second indication, query a frozen connectivity pipeline with disease transcriptomics collected
independently of the drug, and see where the approved drug ranks.

This report scopes that benchmark rather than running it, and finds that the scoping is where
the difficulty lives. Of roughly 72 verified FDA repurposing approvals since 2000, **thirteen**
survive a pre-registered set of inclusion gates, twelve of them cleanly. Getting there required resolving problems
that would each have silently changed the result: two of the four strongest candidates are
**circular**, because the transcriptomic data that would test the pipeline is the data that
generated the repurposing hypothesis; compound identity by InChIKey skeleton fails in **both**
directions, merging stereoisomers that differ and splitting tautomers that do not; and one
pre-registered gate, the requirement that data predate the hypothesis, turns out to be close to
**structurally unsatisfiable**, because public expression repositories postdate most of the
repurposing hypotheses that reached approval.

Three properties of the scoring metric are also reported. The self-target control proposed in
earlier work does not port to connectivity scoring, because swapping a query's up and down gene
sets flips the score's sign exactly by construction, so the naive port is an identity rather
than a test. Transcriptional activity across the reference library is **not** concentrated
(Gini 0.274 against 0.333 for a uniform distribution), which removes one way the benchmark
could have failed before starting, though 23.2% of the library has no quality-passing signature
at all. And the connectivity score returns **exactly zero for 44% of compounds**, creating a
tied block of roughly 11,653 whose tie-breaking convention alone moves a drug's percentile
**from 28 to 72**, a larger swing than any effect the benchmark could detect.

**Version 2 reports the run.** The null-query control was run first and did not fire (median
rho +0.099 over 20 healthy-versus-healthy splits, against a void threshold of 0.5). The prediction
was then committed with a SHA-256 hash before any score existed. Building the scorable set took
the thirteen candidates down to **seven**, every reduction on a deposit ground: four series hold
no disease-versus-control contrast, one has no processed expression at all, and one tissue is
heterogeneous. Five defects were caught before scoring, two of them by reading the frozen inputs.
**The pre-registered criterion was not met: mean percentile 0.387 against a null of 0.501, permutation
p = 0.098.** The direction favors the pipeline and the instrument is too small to say more. One of
the seven cases, heart failure, carries no information at all: four of its five drug identifiers
score exactly zero and its median lands on the tied block that Section 8.3 measured in advance.

---

## 1. Why this benchmark does not exist yet

A diligence team asked to evaluate a computational repurposing program asks a simple question:
has this class of method ever produced an approved drug? The honest answer is that of roughly
72 verified FDA repurposing approvals between 2000 and 2026, **exactly one has a documented
computational origin**: baricitinib for COVID-19, identified by a knowledge-graph method in
February 2020 and granted full approval in May 2022. One further case rests on a company claim
with no peer-reviewed method paper. Everything else traces to clinical observation, mechanistic
reasoning, experimental screening or serendipity.

The canonical showcases of transcriptomic reversal, topiramate for inflammatory bowel disease,
imipramine for small-cell lung cancer, bexarotene for Alzheimer's disease, have no approval
between them, and the topiramate result failed in a retrospective cohort. **No repurposing
derived from transcriptomic signature reversal has reached FDA approval.**

That fact cuts both ways. It is the reason a diligence team is skeptical, and it is the reason
a rigorous retrospective benchmark, published whichever way it falls, would be worth more than
another positive prediction.

A proposal for such a benchmark assumed 20 to 50 usable disease-drug pairs. This report counts
them, under gates fixed before the count was seen.

---

## 2. The gates, fixed in advance

A pair qualifies only if it passes all of the following, each stated so that a third party can
adjudicate it from public records.

**G1, genuine repurposing.** An FDA approval for indication A and a later FDA approval for a
different disease B. This excludes rescues (a compound that never gained its first approval),
new chemical entities derived from a repurposed parent, label expansions within one disease,
and active metabolites developed separately.

**G2, presence in the reference library.** The compound has L1000 signatures in the CMap LINCS
2020 release. **L1000 is small molecules only.**

**G2b, coverage.** At least one quality-passing exemplar signature in at least two distinct
cell lines. Added after G2 verification revealed that presence and usability are different
properties; the rationale and its pre-registration are in Section 5.

**G3, independent disease transcriptomics.** Public patient-tissue expression data exists for
indication B and was collected independently of the drug. **Independence is stronger than
treatment-naive: a cohort assembled because someone was already pursuing that drug's target or
pathway leaks the answer even if no patient received the drug.** Adjudicated by reading the
study's own statement of purpose, not by parsing repository metadata, because no
machine-readable treatment-naive field exists.

**G4, time split.** The transcriptomic data predates the repurposing hypothesis, not merely the
approval. **This gate was amended during the work and the amendment is recorded in Section 6.**

---

## 3. G2 excludes the closest precedent, and identifier matching fails both ways

### 3.1 The biologics exclusion

L1000 is a small-molecule library, and much of the immunology repurposing record is antibodies.
Tocilizumab, rituximab, alemtuzumab and denosumab are all excluded by assay scope, as are the
peptide GLP-1 agonists.

The tocilizumab exclusion is the painful one. Tocilizumab moving from rheumatoid arthritis into
systemic sclerosis on a fibroblast-activation argument is the closest available precedent to a
program targeting fibrosis, in the same disease, and **the pipeline structurally cannot be
tested on it**, because an interleukin-6 antibody has no L1000 signature. This is a property of
the reference library, not a fixable design choice, and it belongs in any statement of what
such a benchmark can and cannot address.

### 3.2 Verification, and its own controls

`compoundinfo_beta.txt` (39,321 rows, 34,419 distinct compounds) and `siginfo_beta.txt`
(1,201,944 rows, of which 720,216 are compound signatures) were retrieved from the CMap LINCS
2020 release. Each candidate was resolved by two independent routes: the library's own
`cmap_name` string, and PubChem name resolution to an InChIKey whose first fourteen characters,
the connectivity layer, were matched against the library's `inchi_key` field.

Two self-test rows traveled with the candidates: vorinostat, required to be present, and
tocilizumab, required to be absent. Both behaved as required. Without that pair, a matcher that
returned "present" for everything would have produced an identical-looking table.

**All 20 candidates are present.** The result reproduced identically across two sessions on
different days, including a fresh download of both files.

### 3.3 ⛔ The skeleton fails in both directions

Eight of the twenty disagreed between routes, and the disagreements are the substance rather
than a nuisance.

**Two library rows are named for a drug they are not.** One row carries `cmap_name` "sirolimus"
with a connectivity layer entirely different from the other five sirolimus rows. Another carries
"tacrolimus" with the same problem. A name-based lookup would have pulled both into the
benchmark as the drug.

**The skeleton is blind to stereochemistry, so it merges compounds that differ.** It reported
(S)-ruxolitinib as ruxolitinib, though the approved drug is the (R)-enantiomer, and it reported
dexfenfluramine as fenfluramine, though the approved anti-seizure drug is racemic. The first is
excluded; the second is a **declared substitution**, because the library holds no racemic entry.

**The skeleton is sensitive to tautomer representation, so it splits compounds that are the
same.** PubChem's name lookup for doxycycline returns the imidic-acid tautomer; the library
carries the amide tautomer. Same molecular formula, same compound, different connectivity layer,
different skeleton. Read as a conflict, it would have removed a usable row.

> **A skeleton disagreement is not evidence of a different compound, and a skeleton agreement is
> not evidence of the same one.** Both directions need a formula-and-name check before a row is
> included or dropped. The stereo half of this is well known; the tautomer half is stated here
> because it silently reverses the sign of the same test.

One further case makes the argument on its own: propranolol's two enantiomer entries have **no
`cmap_name` at all**. The field holds the internal identifier and the enantiomer appears only in
a synonyms column. No name search of any spelling would ever have found them.

---

## 4. Coverage: presence is not usability

G2 verification returned a second fact unasked. Exemplar-signature counts across the candidates
span 7 to 115. A compound can be in the library and still be too thinly represented to query
against.

**G2b was therefore fixed before the per-compound breakdown was examined**: at least one
quality-passing exemplar signature in at least two distinct cell lines. The rationale, stated in
advance: the query is a primary-tissue disease signature and none of the nine core L1000 lines
is that tissue, so a compound represented in a single line cannot have its signature separated
from that line's idiosyncrasy. The gate was placed on cell-line count alone; dose, timepoint and
transcriptional activity were recorded and not gated, because any threshold on those would have
been chosen after seeing the output.

**The gate binds nothing.** All rows clear it, with cell-line counts from 5 to 44. The worry
behind it was wrong in an instructive way: the thinnest row's seven exemplar signatures are
spread across five cell lines rather than concentrated in one. Across the table, exemplar count
and line count are nearly equal, which is what "exemplar" means in this release: approximately
one representative signature per compound and cell line. Gating on lines turned out to be nearly
the same gate as gating on exemplar count.

A gate that was pre-registered and then excluded nothing is reported here as such. Its value was
in being fixed before the numbers were seen, not in what it removed.

---

## 5. G3, and the circularity that removes the best candidates

Independence was adjudicated from each dataset's own statement of purpose.

**Evidence was graded asymmetrically, and deliberately.** A row that fails here is verified
failed, because target-driven language on its face is decisive. A row that passes, passes
provisionally, because absence of such language is weaker evidence than its presence. The gate
should be easier to fail than to pass.

### 5.1 ⛔ Two of the four strongest candidates are circular

**Baricitinib for severe alopecia areata is disqualified.** The transcriptomic profiling that
would test the pipeline is the profiling that generated the JAK hypothesis: the source paper's
own abstract states that global transcriptional profiling of mouse and human lesional skin
revealed the interferon-gamma signature, and the patient arrays were run for that investigation.
Scoring a transcriptomic pipeline against that data asks whether a transcriptomic method
recovers a drug a transcriptomic method found. **This is the single most quotable repurposing in
dermatology and it cannot be used.**

**Ruxolitinib for vitiligo fails for the same reason.** The largest lesional-skin series states
that samples with an active inflammatory infiltrate "were selected for gene expression profiling
in order to identify inflammatory pathways that drive depigmentation." Selected on the
infiltrate, aimed at the pathway, and ruxolitinib acts on exactly that axis.

Two of four, in two different diseases, for the same reason. That is not coincidence. **It is
selection on the outcome: the repurposings a transcriptomic pipeline would be most likely to
recover are precisely the ones whose data is disqualified, because that data is what found
them.**

### 5.2 Contaminated datasets inside otherwise clean rows

Independence is a property of each dataset, not of a disease. Two examples found by reading
purpose statements rather than titles:

Within the atopic dermatitis series, one dataset compares the mode of action of a topical
corticosteroid against **pimecrolimus**, a calcineurin inhibitor of the same class as
tacrolimus, the drug that row is meant to test. It sits in the middle of the result set and
nothing but reading the purpose would have caught it. **Excluded by name.**

Within the multiple sclerosis series, the second-largest expression cohort is a study of how
**interferon-beta** corrects gene dysregulation in the disease. It is a treatment-response
cohort for a disease-modifying therapy, with treated patients in it. Attractive on size,
disqualified on both independence and exposure. **Named in the record as a dataset to avoid.**

### 5.3 What passes

**Thirteen rows survive G3**, twelve of them cleanly and one, sirolimus for
lymphangioleiomyomatosis, retained as marginal because the entire disease has twenty series and
the usable one has twenty-five samples. **Five are verified out**: the two circular rows above,
and three with no usable tissue transcriptomics in existence: no dataset for subependymal giant cell
astrocytoma surfaced at all, and none for infantile hemangioma. Ivermectin for rosacea is the third of those, with four series for the
entire disease, one of which is a lymphoma matched in error.

The rows that pass are all diseases profiled early and broadly for their own sake, before
anyone was looking for these particular drugs in them. **That is the selection rule the benchmark
actually runs on**, and it deserves stating more plainly than the original gate did.

---

## 6. ⛔ G4 is close to unsatisfiable, and the gate was amended

Establishing the hypothesis dates exposed a structural problem.

**Public expression repositories opened in 2000, and human disease-tissue profiling at scale is
roughly 2005 onward.** A repurposing hypothesis made public before about 2005 therefore has no
transcriptomics old enough to predate it, not because the right dataset was missed but because
none exists. Meanwhile a hypothesis made public after about 2012, in a disease where
transcriptomics is mature, has usually been *generated* by transcriptomics and fails G3 for
circularity instead.

| hypothesis date | outcome |
|---|---|
| before ~2005 | no data old enough exists. **Fails G4 structurally.** |
| ~2005 to ~2012 | the survivable window, for hypotheses of non-transcriptomic origin |
| after ~2012, mature field | the hypothesis probably came *from* transcriptomics. **Fails G3.** |

The two gates close on each other. Under strict G4 the table holds **two** rows, and there is no
benchmark at n = 2.

G4 also could not be adjudicated as written. It says the data must predate "the repurposing
hypothesis." Colchicine for cardiovascular prevention has a retrospective observation in gout
and familial Mediterranean fever patients around 2001, and a first prospective trial in 2013. A
retrospective observation is a hypothesis; a first trial is a test of one. The gate was written
to exclude approval dates and never settled the gap between those two, and that gap alone moves
the count.

> **Amendment, recorded rather than applied quietly.** G4 is retired as an inclusion gate and
> becomes a **reported field**. Every row carries its hypothesis date and its data's deposition
> date, and the rows that would have satisfied strict prospectivity are marked as a subset
> within the results. G3's independence clause does the work G4 was meant to do.
>
> **The claim changes with it.** The benchmark no longer asserts that the pipeline would have
> found these drugs before anyone did. It asserts that the pipeline recovers known repurposings
> from data that did not encode the answer. A reader may still object that the recovery is after
> the fact. **That objection is correct and this design does not answer it.**

Amending a pre-registered gate after seeing which rows it kills is exactly the move this work is
trying not to make, which is why the amendment carries its date, its reasoning as it stood at
the time, and the original table left intact beside it.

**Two rows satisfy strict prospectivity and form the marked subset**: eflornithine for
neuroblastoma, whose two primary-tumor cohorts predate the ornithine decarboxylase hypothesis,
and the SGLT2 inhibitors for heart failure, whose largest myocardial cohort predates the
cardiovascular outcomes trial by nine years.

---

## 7. The thirteen rows

| # | drug | indication | query tissue | note |
|---|---|---|---|---|
| 3 | colchicine | atherosclerotic cardiovascular disease | coronary artery | |
| 4 | eflornithine | high-risk neuroblastoma | primary tumor | strict-G4 subset |
| 6 | cladribine | relapsing multiple sclerosis | CNS tissue | |
| 7 | sirolimus | lymphangioleiomyomatosis | lung nodules | **marginal**, 20 series exist |
| 8 | tadalafil | pulmonary arterial hypertension | lung | spatial assay, needs aggregation |
| 10 | doxycycline | periodontitis | gingival tissue | G2 tautomer resolved |
| 12 | hydroxyurea | sickle cell disease | blood | tissue definition flagged |
| 13 | ruxolitinib | steroid-refractory acute GVHD | colon biopsy | thin, 15 series exist |
| 14 | SGLT2 inhibitors | heart failure and chronic kidney disease | myocardium and kidney | strict-G4 subset |
| 15 | spironolactone | heart failure | myocardium | **shares row 14's query** |
| 17 | cyclosporine | psoriasis | lesional skin | |
| 18 | tacrolimus | atopic dermatitis | lesional skin | one dataset excluded |
| 19 | baricitinib | COVID-19 | lung and airway | the one computational precedent |

### 7.1 The unit of analysis is the query, not the drug

Enumerated in code rather than counted by eye: thirteen rows, thirteen distinct query
signatures, and **fourteen drug-query pairs**. The mapping is not one to one. Heart-failure myocardium serves two rows,
and one row spans two tissues.

A combined test that treats fourteen ranks as fourteen independent observations overstates its
own evidence. **The unit is therefore the query signature**: thirteen cases, with the myocardium
case scored by the **median** percentile rank of its three drugs rather than the best of them.

The reason for median rather than best is the same reason that recurs throughout this work: a
maximum over more draws is larger for that reason alone. The same inflation appears in
per-compound transcriptional activity summarized by its maximum across cell lines, where the
rank correlation between that maximum and the number of signatures a compound has is +0.618.

The null is a **permutation over drug labels** preserving the drug-to-query structure, which
handles the shared-query correlation without dropping a case or applying an analytic correction.

---

## 8. Three properties of the metric

### 8.1 The self-target control does not port

Earlier work proposed a two-part precondition on any perturbation-ranking metric, whose second
part scores the candidate library against the population the system started in rather than
against the target, and asks whether the ranking changes.

**That control cannot be ported to connectivity scoring.** A connectivity score is a two-tailed
enrichment statistic between an up-regulated and a down-regulated query set and a ranked
signature. Swapping the two query sets flips the score's sign **exactly**, by construction.

This was verified rather than asserted. In a reference implementation carrying six controls, the
swapped query returned +0.950250 against -0.950250, equal to twelve decimal places.

**A control that always fires the same way is not a control.** Running the naive port and
reporting a clean reversal would look like a pass and would establish nothing. Readers working
in connectivity space will reach for exactly this port, which is why it is stated here.

The honest replacement asks the same question in the form the metric permits: build a **null
query with the same structure and no disease content**, by splitting the healthy controls at
random into two halves, score the library against it, and correlate that ranking against the
ranking from the real disease signature. If they agree, the score is not responding to disease
content. This consumes no ground truth and costs one extra scoring pass.

### 8.2 Activity is not concentrated, but a quarter of the library is unscoreable

Before any query exists, a library-level question can be asked: is transcriptional activity so
concentrated that the set of compounds able to reach the top of any ranking is fixed before a
disease is named?

Measured over 90,834 quality-passing exemplar compound signatures across 26,425 compounds:

| measure | value | reference |
|---|---|---|
| Gini of per-compound median activity | **0.274** | uniform distribution is 0.333 |
| share held by the top 10% | 22.3% | equality is 10% |
| share held by the top 1% | 3.5% | equality is 1% |

**The control does not fire.** Activity is *less* unequal than a uniform spread, so the
reachable candidate set is not fixed in advance. One way the benchmark could have been dead on
arrival is closed off.

Two facts survive that negative, neither of them a verdict. **7,994 compounds, 23.2% of the
library, have no quality-passing exemplar signature at all** and cannot be scored under any
query. And absolute activity is low with a long tail: the median compound sits at 0.154 against
a maximum of 0.859, so the top decile begins at about a third of the maximum. Whether that is
too low to support connectivity scoring is a threshold, none was pre-registered, and one chosen
now would be chosen after seeing the distribution.

### 8.3 ⛔ Forty-four percent of scores are exactly zero

The connectivity rule returns **exactly zero** whenever a query's up and down tails enrich in
the same direction. Over 4,000 random signatures in the 978-gene landmark space:

| query size | exactly zero | sd of nonzero scores |
|---|---|---|
| 50 | 48.1% | 0.120 |
| 100 | 46.4% | 0.084 |
| **150** (convention) | **44.1%** | 0.067 |
| 200 | 40.5% | 0.057 |

At the conventional query size, in a 26,425-compound library, that is a tied block of about
**11,653 compounds**. Where a drug scoring exactly zero lands depends entirely on a convention
that is usually buried in an implementation:

| tie rule | percentile |
|---|---|
| optimistic | **28.0%** |
| midrank | **50.0%** |
| pessimistic | **72.0%** |

**Forty-four percentile points from the tie rule alone**, larger than any effect the benchmark
could detect. **Midrank is pre-registered**: it is standard, it is neither optimistic nor
pessimistic, and it is the only one of the three that cannot be accused of having been chosen
for its result. The tied count is reported per row, so a reader can see how much of each ranking
carries no resolution.

A second consequence: the nonzero scores have a standard deviation of 0.067, so the usable part
of the scale is narrow as well as half-empty. Percentiles from this metric should not be quoted
to three decimals.

---

## 9. The decisions that would have decided the answer

Implementing a choice is making it. The following are fixed here, in advance, because leaving
them to be settled inside code is how an analysis acquires a result it cannot defend.

| decision | fixed as | reason |
|---|---|---|
| tie rule | **midrank** | Section 8.3; 44 percentile points |
| query size | 150 up, 150 down | convention, and the lowest tie fraction among conventional sizes |
| gene space | 978 landmark genes only | the only directly measured space |
| disease contrast statistic | moderated t (**run: pooled-sd t with a variance floor; Section 13.1**) | ranks by evidence, not fold change alone |
| array versus sequencing rows | same statistic both paths | otherwise method is confounded with row |
| multiple datasets per row | largest independent one; others as sensitivity | merging is a modeling choice |
| spatial and single-cell rows | pseudobulk to sample level before any contrast (**run: averaged to donor; Section 13.1**) | puts every row at the same level |
| compound's many signatures | **median** | a maximum over more signatures is larger for that reason alone |
| cell lines | all, with a mesenchymal-only secondary declared now | declaring it now prevents a post-hoc rescue |
| direction | ascending, most negative is best | reversal is the hypothesis |
| combined null | permutation over drug labels, structure preserved | handles the shared query |

---

## 10. What version 1 did not report, and why (superseded by Section 13)

**No benchmark result appears here.** The control in Section 8.1 determines whether the scoring
metric responds to disease content at all, and it has not been run. If it fires, the thirteen rows
are irrelevant until the metric is repaired, and any ranks reported beforehand would have to be
withdrawn.

That sequencing is not caution for its own sake. This program has already published one report
in which a unanimous negative was drafted as a finding before the control that disqualified it
was run, and in which three further conclusions were each stated after one check and before the
check that would have overturned them. Repeating that pattern in the work that documents it
would be indefensible.

The prediction is therefore stated and left unregistered pending the control:

> Thirteen cases, one per query signature, scored by percentile rank of the approved drug within
> the library, with midrank tie-breaking. The combined statistic is the mean percentile rank
> across cases, tested against a permutation null over at least 10,000 drug-label permutations
> preserving the drug-to-query structure. **Positive requires both a permutation p below 0.05
> and a mean percentile rank inside the top 20% of the library.** If the null-query control
> shows the library ranking against a healthy split correlating with the ranking against the
> real disease signature above 0.5, **this prediction is void and no ranks are reported.**

---

## 11. Errors made in producing this report

Reported rather than removed, on the same principle as the preceding work, and because several
of them are the kind that survive review.

**Citing a dataset without checking what it holds.** One row was passed on the strength of a
title describing a transcriptional program. The dataset's assay type is genome binding and
occupancy profiling, not expression, and its description field is an empty container stub. The
row was corrected, but it had been recorded as verified in a pass whose entire stated method was
reading descriptions.

**A test that encoded the assumption it was meant to check.** A repository lookup read a
date field under the wrong capitalization and returned zero for every record. The fixture
written to test it used the same wrong capitalization, because the same author wrote both, so
it could only ever confirm the guess. Every date-based verdict in that run was built on nothing
and printed as though it were a result.

**An unstated filter that hid most of the data.** Every repository query carried a restriction
to one assay technology, never mentioned. It hid between 59% and 97% of available series
depending on the disease. The conclusions about which series are *oldest* survive, verified
separately, because the excluded technology postdates them. Every claim about depth was wrong.

**A default sort mistaken for an ordering.** Repository search returns by relevance, not date.
With a result cap below the hit count, the returned subset is relevance-biased, and its oldest
member is an artifact of that sampling. One disease appeared to have no data before 2018 when
its earliest series is from 2003.

**A looser matcher reported as a stricter one.** An adjudication step meant to explain
disagreements between two compound-matching routes reimplemented one of them as a substring
match rather than an exact match. It silently pulled a different approved drug into another
drug's candidate set.

**An arithmetic error in the headline count**, stating one tier as eight when the table it
summarized contained nine.

**Two confounds caught before they shipped, not after.** A per-compound activity summary by
maximum, which is inflated by how many cell lines a compound was tested in; the rank correlation
is +0.618. And a validation threshold of "greater than 0.95" for a self-query control, which
returns 0.9503 and looks like a pass. The statistic's exact analytic maximum is 1 - k/n + 1/(2n),
and a loose threshold would have accepted a subtly wrong implementation.

The common shape across these is not carelessness about whether the code runs. Every one of them
produced output that looked like a result. The failure is testing the part that was already
being thought about, and not the part that had to be true for the output to mean anything.

---

## 12. What would make this worth doing

Thirteen cases will not settle whether transcriptomic repurposing works. At that size the combined
test has little power, and a null result will be consistent with both a useless method and a
modest one.

What the exercise does establish is a floor for what an honest attempt requires: identifier
resolution that fails safely in both directions, independence adjudicated from stated purpose
rather than metadata, a tie convention fixed before it can be chosen for its result, and a
metric control that runs before the ranks and can void them.

**And one finding stands whatever the ranks turn out to be.** Retrospective validation of
transcriptomic repurposing is close to structurally impossible as usually conceived, because the
data that would test the method and the data that generated the hypothesis are, for the most
promising cases, the same data. That is worth saying plainly, and this report says it before
knowing whether its own benchmark would have been flattering.

---

## 13. Version 2: the run

### 13.1 Every way the run departed from version 1

Version 1 described a plan. The run differed from it in the following ways, each fixed before any score existed and each recorded in a dated, hashed addendum on the author's disk.

| version 1 said | the run did | why |
|---|---|---|
| positive needs p < 0.05 **and** mean percentile in the top 20% | **one condition: permutation p < 0.05** | the second condition was arithmetically unreachable for a large fraction of tie configurations (28.7% at n = 8) whatever the pipeline did; a count of drugs beating the tie block was checked as a replacement and is exactly as unreachable |
| thirteen cases | **seven** | Section 13.3 |
| moderated t for the disease contrast | the statistic used by the null-query control: mean difference over a pooled standard deviation floored at 0.1 times its median | the same code that ran the control ran the benchmark; a moderated t was never implemented, and switching after the control would have scored the benchmark with untested code |
| spatial rows pseudobulked to sample level | **averaged to donor within arm** | spatial "samples" turned out to be regions and sections, several per patient; sample level would have counted one patient many times |
| drug identity from a curated file | **re-derived by rule** (exact name or alias, plus both doxycycline tautomers), then a molecular-formula check | the curated file was lost; the rule and the check were fixed before scoring |
| mesenchymal-only secondary declared | run separately and reported in Section 13.6 | declared in Section 9 of version 1 |

### 13.2 The control ran first

The null-query control of Section 8.1 was run on the heart-failure myocardium series before anything was registered: the healthy controls were split at random into two halves twenty times, each split scored as a query, and its library ranking correlated with the ranking from the real disease signature. **Median rho +0.0994, range -0.47 to +0.54, none undefined.** The void threshold was 0.5. The metric responds to disease content, which is all this control can establish. It says nothing about whether the ranking is correct.

At the compound level, where the benchmark actually ranks, 34.7% of compounds score exactly zero against a real query, not the 44% that Section 8.3 measured for single signatures. A compound's score is the median of several signatures, and a median is less often exactly zero than any one draw.

### 13.3 From thirteen to seven

Every reduction came from reading what was actually deposited rather than what a paper about the deposit describes.

- **Colchicine for atherosclerosis.** The only curated dataset has one experimental variable, `individual`. No disease state, and several segments per patient.
- **Eflornithine for neuroblastoma.** One series has no sample characteristics at all and a reference channel that is itself neuroblastoma; the other is 101 tumors and one fetal brain. No neuroblastoma series anywhere has a same-series normal arm, because the tissue of origin is embryonic and is not collected as a surgical control.
- **Sirolimus for lymphangioleiomyomatosis.** The controls are cultured smooth muscle and a melanoma cell line.
- **The SGLT2 kidney query.** Both platforms' controls are tumor nephrectomies, three and two samples.
- **Baricitinib for COVID-19.** The required named tissue is heterogeneous across autopsy sites.
- **Ruxolitinib for graft-versus-host disease.** The series holds no expression data. Every sample's processed-data field reads NONE; only raw reads exist. Reprocessing them would have meant choosing an aligner and a normalization after the prediction was committed.

**The seven that ran:** cladribine for multiple sclerosis (spatial transcriptomics of brain, 13 case and 4 control donors), tadalafil for pulmonary arterial hypertension (spatial profiling of lung, 11 and 5 donors), doxycycline for periodontitis (183 and 64 gingival samples), hydroxyurea for sickle cell disease (blood, 190 and 31), the heart-failure myocardium case with dapagliflozin, empagliflozin and spironolactone (177 and 136), cyclosporine for psoriasis (13 and 13), and tacrolimus for atopic dermatitis (9 and 9).

The strict-prospectivity subset of Section 6 is not reported: eflornithine was excluded, which leaves at most one row, and a subset of one is not a subset.

### 13.4 Five defects caught before scoring

The run was split into stages so that the inputs could be frozen, hashed and read before any score existed. Five defects were caught that way, and none would have raised an error.

1. **The positive control returned no cases.** The case pattern for heart failure was written as `cardiomyopathy`; the deposit says `CMP`. All 177 cases would have been dropped. This row was included precisely because its answer was already known.
2. **A roster with no controls read as fine.** The control pattern `^control` cannot match `HI`, the deposit's label for healthy individuals.
3. **A control arm built on an assumption.** Sickle cell controls are labeled both `A` and `AA`; whether those are one group was settled from the records (interleaved specimen numbering, identical clinical fields), not from nomenclature.
4. **The formula check kept the wrong compound.** Its first rule took the reference formula from the tacrolimus identifier with the most signatures. That identifier is C45H71NO12 and is not tacrolimus; the other four are C44H69NO12. The rule kept the one wrong compound and dropped the four right ones. The corrected rule takes the formula shared by most of a drug's identifiers and stops the run unless it equals the known formula.
5. **A misspelled field defeated the donor averaging.** The lung series spells its donor field `individuial`. The pattern searched for "individual", found nothing, and scored 220 lung regions as 220 independent people. Rebuilt, the row is 11 case and 5 control donors.

Defects 1 and 2 were found by a dry run and a positive control; 4 and 5 by reading the freeze report before scoring. **The common cause of 1, 2 and 5 is a pattern written from what a label ought to say rather than from what the field contains.** Addressing variables by field name guards against a variable being in the wrong place; it gives no protection against a mis-guessed value.

### 13.5 Result

The prediction was committed at 15:47 EDT on 2026-10-01, before any score, with SHA-256 `7eee1779246f461b8595eeef8cffd17ee93ead40f6ed36b6af390cd421b7c9a2`. The scored inputs carry SHA-256 `1457464f13bac9a7bdeca438f44414f4a2c2a7e0562992375b982217fd5c54e9`.

| case | approved drug | percentile (lower is stronger reversal) | library tied at zero |
|---|---|---|---|
| psoriasis skin | cyclosporine | **0.154** | 34.2% |
| sickle cell blood | hydroxyurea | **0.176** | 39.3% |
| PAH lung | tadalafil | 0.299 | 31.2% |
| atopic dermatitis skin | tacrolimus | 0.389 | 28.6% |
| periodontitis gingiva | doxycycline | 0.504 | 32.9% |
| heart-failure myocardium | dapagliflozin, empagliflozin, spironolactone | 0.536 | 34.7% |
| MS brain | cladribine | 0.650 | 28.1% |

**Mean percentile 0.387. Permutation null mean 0.501, standard deviation 0.087, 10,000 permutations. p = 0.098. The pre-registered criterion, p < 0.05, is not met.**

**Ties, counted exactly.** Six of the 19 scored drug identifiers score exactly zero and sit on their case's tied block: dapagliflozin, empagliflozin and two of the three spironolactone identifiers in the myocardium case, and two of the four tacrolimus identifiers. **Six of the seven cases resolve off the tied block; the myocardium case does not.** The tied block does not sit at the 50th percentile: its midrank ranges from 0.461 to 0.536 across cases, depending on how many compounds score below zero. A tied drug therefore scores near, not exactly at, chance.

**Two cases point the wrong way at the level of the score itself.** Cladribine's compound score is positive (+0.018), meaning its signatures move expression *toward* the multiple sclerosis signature, not away from it. And doxycycline's two library identifiers, which are the same molecule in two tautomer representations, disagree in sign: one scores -0.035 and the other +0.046. Two independent profilings of one compound giving opposite answers is a direct measure of how much of a single case's rank is noise.

### 13.6 The declared mesenchymal-only secondary

Version 1 declared, in Section 9, a secondary analysis restricted to one mesenchymal cell line (ASC), so that it could not later be introduced as a rescue. The library holds 1,776 quality-passing ASC signatures. **Four of the seven drugs have none**: cladribine, tadalafil, doxycycline and hydroxyurea. In the three cases that can be scored, myocardium ranks at 0.197, psoriasis at 0.254 and atopic dermatitis at 0.816. Mean 0.423 against a null of 0.497 (sd 0.149), permutation p = 0.32.

The secondary says almost nothing, and it was always going to say little once four of seven drugs turned out to lack the cell line. It is reported because it was declared. One detail is worth noting without leaning on it: in ASC alone the myocardium case comes off the tied block and ranks well, at 0.197. Three drugs in one cell line is not evidence, and the observation is recorded so that no one later presents it as a rescue.

### 13.7 What the result means and does not

**It does not show the method fails.** Seven cases cannot distinguish a useless method from a modest one, which Section 12 said before the run and which the pre-registration repeated: a null must not be reported as refuting the pipeline. The direction is favorable, 1.3 null standard deviations below the null mean.

**It does not show the method works.** The two strongest cases are not evidence of much. Cyclosporine for psoriasis and tacrolimus for atopic dermatitis are the same drug class acting on two diseases of one tissue, so they are not two independent confirmations. And the method's best case is the one whose answer is least surprising: calcineurin inhibitors suppress T-cell activation, and inflamed skin is full of activated T cells.

**One case was lost to the metric itself.** Heart failure was the most valuable case in the design: three approved drugs and the largest cohort. Four of its five drug identifiers score exactly zero, and its median lands on the tied block. Section 8.3 measured that block in advance and fixed the tie rule so it could not be chosen for its result. The rule did its job. The case still carries no information, and that is a property of the connectivity score, not of the drugs.

**What stands whatever the ranks:** the finding Section 12 stated before the run. The scorable set fell from thirteen to seven for one reason in six forms, the deposit lacking the contrast or data the question needs, and five more defects that would have silently changed the answer were caught only because the inputs were frozen and read before the score. Building the benchmark was harder than running it, and the run itself took one pass.

---

## Data and code availability

The code and data for the run reported in Section 13 are deposited with this version, under Zenodo
concept DOI 10.5281/zenodo.23071560, as one archive: the staged notebooks (library activity control
and null-query control, library build, signature freeze, scoring, tie audit and secondary), the
per-series case and control rosters with the classifier that built them, the pre-registration and
its three addenda, the frozen scoring inputs, the scored result, and a SHA-256 manifest covering
every file. The six controls on the connectivity score described in Section 8.1 are deposited as a
script, rewritten against the deposited scoring function because the original reference
implementation was not retained; it reproduces the +0.950250 figure. The compound adjudication
record of version 1 no longer exists (Section 13.1); the rule that replaced it is implemented in
the deposited notebooks, and its formula check is stated in the pre-registration addenda. Compound
and signature metadata derive from the CMap LINCS 2020 release. Disease transcriptomic series are
identified by public accession in the archive's README and rosters.

## Author contributions and disclosure

Sole author. Prepared with AI assistance. All reported figures are produced by the accompanying
code and every measured quantity in this report was computed rather than recalled.

The author holds filed provisional patent applications in therapeutic areas adjacent to the
application domain discussed here. No claim in those applications depends on any result reported
in this document, and no result in this document is favorable to them.
