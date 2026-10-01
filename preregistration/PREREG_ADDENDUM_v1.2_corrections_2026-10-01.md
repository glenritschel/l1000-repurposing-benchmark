# Pre-registration addendum v1.2: two corrections, made after Phase B1 and BEFORE any score

**2026-10-01 ~17:00 EDT.** No connectivity score had been computed for any row. Base pre-registration SHA-256 7eee1779...c9a2 and addendum v1.1 SHA-256 39eab5db...622b stand except as corrected here.

1. **Drug formula reference (corrects v1.1 rule 2).** v1.1 took the reference formula from the ID with the most library signatures. For tacrolimus that ID, BRD-K08845546, is C45H71NO12, which is not tacrolimus; the other four tacrolimus IDs are C44H69NO12, tacrolimus's known formula. The v1.1 rule kept the wrong compound and dropped the four right ones. **New rule: the reference is the formula shared by the majority of the drug's IDs, and it must equal the drug's known formula or the run stops.** Under it, tacrolimus is BRD-A96754982, BRD-K44094599, BRD-K65261396 and BRD-K69608737; BRD-K08845546 is dropped. All other drugs are unchanged and every kept formula matches its known formula.

2. **Row 8 donor field (applies v1.1 rule 5 as intended).** The deposit spells the donor field `individuial`; B1's pattern looked for "individual" and missed it, so B1 built row 8 per ROI. Row 8 is rebuilt averaged to one value per donor within arm. Row 6 is built the same way through the spot annotation's `donor_pseud` field.

3. **Row 13 has no processed expression in GEO.** Every GSE134662 sample lists its supplementary file as NONE; only SRA raw reads exist. Not built. Its disposition is Glen's decision and will be recorded here as v1.3 before scoring.
