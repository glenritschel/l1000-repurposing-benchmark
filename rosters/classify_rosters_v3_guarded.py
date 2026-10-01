#!/usr/bin/env python3
"""classify_rosters.py -- build the case/control roster for each benchmark query.

Rules are declared HERE, above the data, from the field inventory in
RR_QUERY_SURVEY and the confirmations in RR_ROWSET_RESOLVED. They are printed
alongside every result.

⛔ THE RULE THAT SHAPES THIS FILE: a variable is addressed by its FIELD NAME,
never by its characteristic LINE INDEX. GEO writes one !Sample_characteristics
line per characteristic SLOT, not per variable, so a sample carrying a different
number of characteristics shifts every later variable up or down a line. Measured
in GSE35007: line 4 reads 'hb phenotype' for 310 samples and 'white blood cells'
for one. Indexing by position silently mislabels those samples.

    python classify_rosters.py --selftest    # no network
    python classify_rosters.py               # prints rosters, writes nothing
    python classify_rosters.py --confirm     # writes the roster CSVs
"""
import collections, csv, gzip, os, re, sys, urllib.request

# ------------------------------------------------------------------ the rules
# where: "char" (a named characteristics field), "title", or "source".
# Precedence is EXCLUDE, then CONTROL, then CASE, then unassigned. Control
# outranks case because 'non-failing' contains 'failing'.
RULES = {
 "GSE174647": dict(row="6",     query="ms_cns",        where="char", field="disease state",
                   ctrl=[r"^control", r"^HI$"], case=[r"^ms$"], exclude=[],
                   note="HI = healthy individual, CONFIRMED 2026-10-01 from !Sample_source_name_ch1 "
                        "('Contr. brain N' for HI vs 'MS brain N' for MS). The bare '^control' "
                        "pattern matched nothing and dropped all 28 controls."),
 "GSE256539": dict(row="8",     query="pah_lung",      where="source", field=None,
                   ctrl=[r"^control"], case=[r"^ipah"], exclude=[],
                   note="digital spatial; pseudobulk to one value per sample BEFORE any contrast"),
 "GSE10334":  dict(row="10",    query="gingiva",       where="char", field="gingival tissue phenotype",
                   ctrl=[r"^healthy"], case=[r"^diseased"], exclude=[]),
 "GSE35007":  dict(row="12",    query="blood",         where="char", field="hb phenotype",
                   ctrl=[r"^A$", r"^AA$"], case=[r"^SS$"], exclude=[r"^SC$", r"^AS$"],
                   note="SC is a different genotype; AS is TRAIT, a carrier state, in neither arm. "
                        "A vs AA RESOLVED 2026-10-01 ON EVIDENCE, not nomenclature: all 19 'A' and all "
                        "12 'AA' samples are titled 'Blood Control individual HFS<n>', carry "
                        "'clinical status: C' and 'severity score: 0', interleave in one HFS numbering "
                        "series (105,111,113,116,117,119,122,124), and share the same 10-field set. "
                        "Same control group, genotype transcribed inconsistently. Control arm = 31. "
                        "NOTE: one 'A' sample carries 8 fields, lacking genotypic pc1/pc2; harmless for "
                        "classification, relevant if a later step conditions on those covariates."),
 "GSE134662": dict(row="13",    query="gvhd_colon",    where="char", field="gvhd stage",
                   ctrl=[r"^control$"], case=[r"^onset$", r"^refractory$"], exclude=[]),
 "GSE57338":  dict(row="14/15", query="hf_myocardium", where="char", field="disease status",
                   ctrl=[r"non.?failing"],
                   case=[r"ischemic", r"dilated", r"cardiomyopathy", r"^failing"], exclude=[],
                   note="ALREADY BUILT in control 2; here as the POSITIVE CONTROL for this script. "
                        "FIXED 2026-10-01: the values are 'ischemic' (95) and 'idiopathic dilated CMP' "
                        "(82). 'cardiomyopathy' does not match the abbreviation CMP and nothing matched "
                        "'ischemic', so the POSITIVE CONTROL returned 0 cases and dropped all 177. "
                        "Safe against the control arm because precedence is EXCLUDE, CONTROL, CASE."),
 "GSE6710":   dict(row="17",    query="psoriasis_skin", where="title", field=None,
                   ctrl=[r"\buninvolved\b"], case=[r"\blesional\b"], exclude=[],
                   note="label is in the TITLE; characteristics carry NO disease field at all"),
 "GSE16161-GPL570": dict(row="18", query="ad_skin",    where="char", field="condition",
                   ctrl=[r"^normal"], case=[r"atopic dermatitis"], exclude=[]),
}
EXPECT = {  # from RR_ROWSET_RESOLVED, checked against the run. A disagreement is a defect.
 # REBUILT 2026-10-01. Every row now carries BOTH arms. The 09-30 table had three holes and
 # they are why the first run's defects were nearly written:
 #   GSE174647 was (182, None) -> a roster with 0 controls read as OK
 #   GSE256539 was (152, None) -> same hole, benign only by luck
 #   GSE10334  was (None, None) -> no check at all
 #   GSE35007's control count encoded the very A+AA assumption under test (circular)
 "GSE174647":      (182, 28),   # controls CONFIRMED 2026-10-01: 'HI' = healthy individual
 "GSE256539":      (152, 68),
 "GSE10334":       (183, 64),   # CONFIRMED 2026-10-01 15:50: GEO overall-design text (submitter prose, not the characteristics field) states 183 diseased / 64 healthy of 247
 "GSE35007":       (190, 31),   # ⚠ was circular; control arm now EVIDENCE-BACKED (A == AA)
 "GSE134662":      (44, 10),
 "GSE57338":       (177, 136),  # 177 independently via 'heart failure: yes' [O15]
 "GSE6710":        (13, 13),
 "GSE16161-GPL570": (9, 9),
}

# ⛔ An arm that finishes EMPTY is an error, not a warning. Both first-run defects (GSE57338
# 0 cases, GSE174647 0 controls) presented exactly this way and neither stopped the run.
# Addressing by field name guards against a variable being in the wrong PLACE; nothing guarded
# against a pattern written from what the label OUGHT to say rather than what the field holds
# ('^control' against 'HI', 'cardiomyopathy' against 'CMP'). This is that guard.
EMPTY_ARM_IS_FATAL = True

def _nb(): return "ipykernel" in sys.modules or "google.colab" in sys.modules

def url_for(acc):
    g = acc.split("-")[0]
    stub = g[:-3] + "nnn" if len(g) > 6 else g
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/{stub}/{g}/matrix/{acc}_series_matrix.txt.gz"

def fetch(acc, cache="."):
    p = os.path.join(cache, f"{acc}_series_matrix.txt")
    if os.path.exists(p):
        return open(p, encoding="utf-8", errors="replace").read()
    with urllib.request.urlopen(url_for(acc), timeout=300) as r:
        t = gzip.decompress(r.read()).decode("utf-8", errors="replace")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    print(f"  downloaded {p} ({len(t)/1e6:.1f} MB)")
    return t

def parse(text):
    """{gsm: {'title':..,'source':..,'chars':[..]}} preserving per-sample order."""
    acc = titles = source = None
    charlines = []
    for line in text.splitlines():
        if line.startswith("!series_matrix_table_begin"):
            break
        if not line.startswith("!Sample_"):
            continue
        key, _, rest = line.partition("\t")
        vals = [v.strip().strip('"') for v in rest.split("\t")]
        k = key.lower()
        if k == "!sample_geo_accession": acc = vals
        elif k == "!sample_title": titles = vals
        elif k == "!sample_source_name_ch1": source = vals
        elif k.startswith("!sample_characteristics"): charlines.append(vals)
    if not acc:
        raise ValueError("no !Sample_geo_accession line")
    out = {}
    for i, g in enumerate(acc):
        out[g] = dict(
            title = titles[i] if titles and i < len(titles) else "",
            source = source[i] if source and i < len(source) else "",
            chars = [row[i] for row in charlines if i < len(row) and row[i]],
        )
    return out

def field_value(rec, where, field):
    """⛔ Addresses a characteristics variable BY NAME across ALL lines."""
    if where == "title":  return rec["title"]
    if where == "source": return rec["source"]
    want = field.lower()
    for c in rec["chars"]:
        name, sep, val = c.partition(":")
        if sep and name.strip().lower() == want:
            return val.strip()
    return None            # the field is absent for this sample, not mis-sited

def classify(rec, rule):
    v = field_value(rec, rule["where"], rule["field"])
    if v is None: return None, None
    for p in rule["exclude"]:
        if re.search(p, v, re.I): return "excluded", v
    for p in rule["ctrl"]:
        if re.search(p, v, re.I): return "control", v
    for p in rule["case"]:
        if re.search(p, v, re.I): return "case", v
    return None, v

def build(acc, rule, text):
    meta = parse(text)
    roster, seen = {}, {}
    for g, rec in meta.items():
        lab, v = classify(rec, rule)
        roster[g] = (lab, v)
        seen[lab] = seen.get(lab, 0) + 1
    return meta, roster, seen

def report(acc, rule, meta, roster, seen):
    print(f"\n{'='*74}\n{acc}   row {rule['row']}   query {rule['query']}")
    if rule.get("note"): print(f"  NOTE: {rule['note']}")
    print(f"  addressed by {rule['where'].upper()}" + (f" field {rule['field']!r}" if rule['field'] else ""))
    for k in ("exclude", "ctrl", "case"):
        if rule[k]: print(f"     {k:<8} {rule[k]}")
    n = len(meta)
    cases = sum(1 for l, _ in roster.values() if l == "case")
    ctrls = sum(1 for l, _ in roster.values() if l == "control")
    exc   = sum(1 for l, _ in roster.values() if l == "excluded")
    una   = sum(1 for l, _ in roster.values() if l is None)
    # TWO INDEPENDENTLY DERIVED TOTALS. A disagreement is the bug that hid a
    # truncated roster for an entire scoring run.
    assert cases + ctrls + exc + una == n, f"CLASS SUM {cases+ctrls+exc+una} != PARSED {n}"
    print(f"  samples {n}   cases {cases}   controls {ctrls}   excluded {exc}   unassigned {una}")
    ec, ek = EXPECT.get(acc, (None, None))
    for label, got, want in (("cases", cases, ec), ("controls", ctrls, ek)):
        if want is not None:
            print(f"     {label}: got {got}, expected {want} -> " + ("OK" if got == want else "*** DISAGREES ***"))
    vals = collections.Counter(v for l, v in roster.values() if v is not None)
    print(f"  distinct values seen in the addressed field: {len(vals)}")
    for v, c in vals.most_common(8): print(f"     {c:>5}  {v[:60]}")
    miss = sum(1 for g, rec in meta.items() if field_value(rec, rule["where"], rule["field"]) is None)
    if miss:
        print(f"  ⚠ {miss} sample(s) DO NOT CARRY THAT FIELD AT ALL. Excluded, not guessed.")
        print(f"     This is the ragged-line case. Addressing by line index would have")
        print(f"     silently given them whatever variable happened to sit in that slot.")
    if ctrls < 10: print(f"  ⚠ ONLY {ctrls} CONTROLS. Thin.")
    if una:        print(f"  ⚠ {una} unassigned. They are DROPPED, not defaulted.")
    # ⛔ An EMPTY ARM is a defect in the RULES, never a property of the data. Both 2026-10-01
    # first-run failures presented this way and neither stopped the run: GSE57338 (the positive
    # control) returned 0 cases because 'cardiomyopathy' misses the abbreviation 'CMP', and
    # GSE174647 returned 0 controls because '^control' misses 'HI'. Returning a defect here
    # rather than printing a warning is what makes the next one impossible to write.
    fatal = []
    if cases == 0: fatal.append("ZERO CASES")
    if ctrls == 0: fatal.append("ZERO CONTROLS")
    ec_, ek_ = EXPECT.get(acc, (None, None))
    if ec_ is not None and cases != ec_: fatal.append(f"cases {cases} != expected {ec_}")
    if ek_ is not None and ctrls != ek_: fatal.append(f"controls {ctrls} != expected {ek_}")
    if fatal:
        print(f"  ⛔ DEFECT in {acc}: " + "; ".join(fatal))
        print(f"     The rule is wrong, not the data. Check the printed value list above")
        print(f"     against the patterns: a pattern written from what the label OUGHT to")
        print(f"     say will miss what the field actually holds.")
    return fatal

def write_roster(acc, rule, meta, roster, outdir="."):
    p = os.path.join(outdir, f"{acc}_roster.csv")
    with open(p, "w", newline="", encoding="utf-8") as f:   # context manager: it FLUSHES
        w = csv.writer(f)
        w.writerow(["gsm", "group", "value", "row", "query"])
        for g, (lab, v) in roster.items():
            w.writerow([g, lab or "unassigned", v or "", rule["row"], rule["query"]])
    # verify by PARSING BACK and counting RECORDS, not lines: embedded newlines
    # inside a field make a line count wrong, which is how the first fix failed.
    with open(p, encoding="utf-8") as f:
        back = list(csv.DictReader(f))
    assert len(back) == len(roster), f"WROTE {len(roster)} BUT READ BACK {len(back)}"
    print(f"  wrote {p}: {len(back)} records read back, matches {len(roster)} classified")
    return p

# ----------------------------------------------------------------- self-tests
def selftest():
    ok = True
    def chk(name, cond, extra=""):
        nonlocal ok
        print(("  PASS  " if cond else "  FAIL  ") + name + (f"  {extra}" if extra else ""))
        if not cond: ok = False
    print("classify_rosters self-tests")

    # ⛔ THE RAGGED FIXTURE. GSM2 carries an EXTRA characteristic first, so its
    # 'hb phenotype' sits on a different line than every other sample's.
    rag = "\n".join([
      '!Sample_title\t"s1"\t"s2"\t"s3"',
      '!Sample_geo_accession\t"GSM1"\t"GSM2"\t"GSM3"',
      '!Sample_characteristics_ch1\t"hb phenotype: SS"\t"white blood cells: 13"\t"hb phenotype: AA"',
      '!Sample_characteristics_ch1\t"sex: M"\t"hb phenotype: SS"\t"sex: F"',
      '!series_matrix_table_begin',
    ])
    m = parse(rag)
    r = dict(where="char", field="hb phenotype", ctrl=[r"^AA$"], case=[r"^SS$"], exclude=[])
    labs = {g: classify(rec, r)[0] for g, rec in m.items()}
    chk("ragged: GSM2's shifted field is found BY NAME", labs["GSM2"] == "case", str(labs))
    chk("ragged: unshifted samples still right", labs["GSM1"] == "case" and labs["GSM3"] == "control", str(labs))
    # prove the test can fail: index-by-line gives GSM2 the wrong variable
    byline = m["GSM2"]["chars"][0].partition(":")[2].strip()
    chk("ragged test is non-degenerate (line 0 for GSM2 is NOT the phenotype)",
        byline == "13", repr(byline))

    # ⛔ THE ANCHORING TRAP. Unanchored 'A' matches SS, AS, SC and everything else.
    vals = ["SS", "SC", "AS", "A", "AA"]
    anch = [v for v in vals if re.search(r"^A$|^AA$", v, re.I)]
    loose = [v for v in vals if re.search(r"A", v, re.I)]
    chk("anchored control pattern selects exactly A and AA", anch == ["A", "AA"], str(anch))
    # The point is not a tally, it is WHICH extra value the loose pattern admits:
    # AS is sickle cell TRAIT, and an unanchored control pattern puts carriers in
    # the control arm, contaminating it with HbS-expressing samples.
    chk("anchoring test is non-degenerate (unanchored admits AS, the trait carrier)",
        "AS" in loose and "AS" not in anch, str(loose))

    # ⛔ THE PSORIASIS TRAP, from the real GSE6710 field set.
    pso = "\n".join([
      '!Sample_title\t"Patient B, lesional skin"\t"Patient B, uninvolved skin"',
      '!Sample_geo_accession\t"GSM1"\t"GSM2"',
      '!Sample_characteristics_ch1\t"Duration of psoriasis: 15 years"\t"Duration of psoriasis: 15 years"',
      '!series_matrix_table_begin',
    ])
    mp = parse(pso)
    rp = RULES["GSE6710"]
    lp = {g: classify(rec, rp)[0] for g, rec in mp.items()}
    chk("psoriasis: title rule splits lesional from uninvolved",
        lp["GSM1"] == "case" and lp["GSM2"] == "control", str(lp))
    # The real naive classifier joins every field into one blob and searches it,
    # which is what control2_phaseA does. Emulate THAT, not a field lookup.
    blob = lambda rec: " ; ".join([rec["title"], rec["source"]] + rec["chars"]).lower()
    lb = {g: ("case" if re.search(r"psoriasis", blob(rec)) else None) for g, rec in mp.items()}
    chk("psoriasis test is non-degenerate (blob matching calls BOTH a case)",
        lb["GSM1"] == "case" and lb["GSM2"] == "case", str(lb))
    chk("and the blob is why: 'Duration of psoriasis' is in BOTH samples' text",
        "psoriasis" in blob(mp["GSM1"]) and "psoriasis" in blob(mp["GSM2"]))

    # ⛔ ORDERING: control must outrank case, because non-failing contains failing.
    nf = "\n".join([
      '!Sample_title\t"a"\t"b"',
      '!Sample_geo_accession\t"GSM1"\t"GSM2"',
      '!Sample_characteristics_ch1\t"disease status: non-failing"\t"disease status: failing"',
      '!series_matrix_table_begin',
    ])
    mn = parse(nf)
    ln = {g: classify(rec, RULES["GSE57338"])[0] for g, rec in mn.items()}
    chk("ordering: non-failing is CONTROL, failing is CASE",
        ln["GSM1"] == "control" and ln["GSM2"] == "case", str(ln))

    # ⛔ O15: an extractor must give DIFFERENT answers to DIFFERENT inputs.
    a = field_value(m["GSM1"], "char", "hb phenotype")
    b = field_value(m["GSM3"], "char", "hb phenotype")
    chk("two different samples give two different values (O15)", a != b, f"{a!r} vs {b!r}")

    # absent field is None, never a guess
    chk("absent field returns None rather than a guess",
        field_value(m["GSM1"], "char", "no such field") is None)

    # round trip, including the record-count check
    import tempfile
    d = tempfile.mkdtemp()
    ros = {g: classify(rec, r) for g, rec in m.items()}
    p = write_roster("FIXTURE", dict(row="X", query="fx"), m, ros, outdir=d)
    chk("roster round-trips with matching record count", os.path.exists(p))

    chk("URL for a plain accession", url_for("GSE10334").endswith("GSE10nnn/GSE10334/matrix/GSE10334_series_matrix.txt.gz"))
    chk("URL for a platform-qualified accession",
        url_for("GSE16161-GPL570").endswith("GSE16nnn/GSE16161/matrix/GSE16161-GPL570_series_matrix.txt.gz"),
        url_for("GSE16161-GPL570"))

    print("\n" + ("ALL SELF-TESTS PASSED" if ok else "SELF-TESTS FAILED"))
    return ok

def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        good = selftest()
        if not _nb(): sys.exit(0 if good else 1)
        return
    if not selftest():
        print("\nself-tests failed, refusing to run")
        if not _nb(): sys.exit(1)
        return
    confirm = "--confirm" in args
    only = [a for a in args if not a.startswith("--")]
    todo = only or list(RULES)
    print(f"\nclassifying {len(todo)} series. "
          + ("WRITING ROSTERS." if confirm else "NOTHING WILL BE WRITTEN."))
    bad = []
    for acc in todo:
        rule = RULES[acc]
        try:
            meta, roster, seen = build(acc, rule, fetch(acc))
            defects = report(acc, rule, meta, roster, seen)
            if defects:
                # ⛔ A defective row is NOT written, with or without --confirm. Writing a
                # roster with an empty arm is worse than writing nothing: the contrast is
                # silently void downstream and nothing downstream will notice.
                bad.append((acc, "; ".join(defects)))
                print(f"  ⛔ NOT WRITING {acc}. Fix the rule and re-run.")
            elif confirm:
                write_roster(acc, rule, meta, roster)
        except Exception as e:
            print(f"\n{acc}  ** FAILED: {type(e).__name__}: {e}")
            bad.append((acc, f"{type(e).__name__}: {e}"))
    print("\n" + "="*74)
    print(f"classified {len(todo)-len(bad)} of {len(todo)}")
    for a, e in bad: print(f"  {a}: {e}")
    if bad:
        print(f"\n⛔ {len(bad)} SERIES WITH DEFECTS. Nothing was written for these.")
        if not _nb(): sys.exit(1)
    elif not confirm:
        print("\nRead every roster above. Re-run with --confirm to write them.")

if __name__ == "__main__":
    main()
