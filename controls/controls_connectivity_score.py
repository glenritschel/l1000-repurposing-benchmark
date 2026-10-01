#!/usr/bin/env python3
"""Six controls on the connectivity score used in the L1000 retrospective repurposing benchmark.

Rewritten 2026-10-01. The reference implementation that Section 8.1 of the paper describes
(cmap_score.py, 2026-09-30) was not retained. These six controls follow the description recorded
for it, and they are run here against the scoring function as deposited: ks() and conn_all()
below are copied verbatim from the scoring payload of RR_BENCHMARK_control0_and_control2.ipynb.

The thresholds of controls 1 to 5 were fixed in this file before the script was first run, and
all five passed on that run.

Control 6 was narrowed after its first run FAILED, and the failure is recorded here rather than
removed. As first written it asserted that reversing a signature negates the score exactly for
any query. Over 200 random queries the worst discrepancy was 0.076. The control was wrong, not
the score: one enrichment statistic and its mirror image differ by 1/n, so an enrichment that
is nearly balanced can keep its sign under reversal. The two-tailed rule then returns exactly
zero on one side and a nonzero score on the other. Control 6 now asserts what does hold (the
self-query negates exactly, and so does every query whose two scores are both nonzero) and
measures how often the exception occurs.

Requires numpy only.
Run:  python3 controls_connectivity_score.py
"""
import sys
import numpy as np

# ---- copied verbatim from the deposited control notebook --------------------------------------
def ks(rp,n,t):
    if t==0 or n==0: return 0.0
    V=np.sort(np.asarray(rp,float)); j=np.arange(1,t+1,dtype=float)
    a=np.max(j/t-V/n); b=np.max(V/n-(j-1.0)/t)
    return float(a) if a>b else float(-b)
def conn_all(Mx,up,dn):
    n=Mx.shape[1]; out=np.empty(Mx.shape[0])
    order=np.argsort(-Mx,axis=1,kind="stable")
    rank=np.empty_like(order); ar=np.arange(1,n+1)
    np.put_along_axis(rank,order,np.broadcast_to(ar,order.shape),axis=1)
    for i in range(Mx.shape[0]):
        eu=ks(rank[i,up],n,len(up)); ed=ks(rank[i,dn],n,len(dn))
        out[i]=0.0 if eu*ed>=0 else (eu-ed)/2.0
    return out
# -----------------------------------------------------------------------------------------------

SEED = 20261001
TOL = 1e-12
results = []

def report(k, name, ok, detail):
    results.append(ok)
    print(f"control {k}: {'PASS' if ok else 'FAIL'}  {name}\n    {detail}")

def top_bottom(sig, k):
    o = np.argsort(-sig, kind="stable")
    return o[:k].copy(), o[-k:].copy()

rng = np.random.default_rng(SEED)

# Controls 1, 2, 3, 5, 6 use n = 2000 genes and k = 100, the size at which the analytic
# maximum is 0.950250, the figure quoted in Section 8.1.
n, k = 2000, 100
sig = rng.standard_normal(n)
up, dn = top_bottom(sig, k)
M = sig[None, :]

# 1. Self-query against the EXACT analytic maximum, 1 - k/n + 1/(2n). Not a loose threshold.
expected = 1.0 - k / n + 1.0 / (2 * n)
s_self = conn_all(M, up, dn)[0]
report(1, "self-query equals the exact analytic maximum",
       abs(s_self - expected) < TOL,
       f"score {s_self:+.12f}   analytic maximum {expected:+.12f}")

# 2. Swapping the up and down sets flips the sign exactly.
s_swap = conn_all(M, dn, up)[0]
report(2, "swapping the query's up and down sets flips the sign exactly",
       abs(s_swap + s_self) < TOL and s_swap < 0,
       f"original {s_self:+.12f}   swapped {s_swap:+.12f}")

# 3. An unrelated signature scores near zero: 1,000 independent signatures, same query.
U = rng.standard_normal((1000, n))
s_unrel = conn_all(U, up, dn)
mx = float(np.max(np.abs(s_unrel)))
report(3, "unrelated signatures score near zero (max |score| below 0.25, |mean| below 0.01)",
       mx < 0.25 and abs(float(s_unrel.mean())) < 0.01,
       f"max |score| {mx:.4f}   mean {s_unrel.mean():+.5f}   against a self-query of {s_self:.4f}")

# 4. Null distribution over random queries, in the benchmark's own space: 978 landmark genes,
#    150 up and 150 down, 4,000 random signatures. Section 8.3 reports 44.1% exactly zero and a
#    standard deviation of 0.067 among the nonzero scores. Pass band: 41% to 47%, 0.060 to 0.074,
#    |mean| below 0.01.
n4, k4, m4 = 978, 150, 4000
perm = rng.permutation(n4)
up4, dn4 = perm[:k4].copy(), perm[k4:2 * k4].copy()
R = rng.standard_normal((m4, n4))
s_null = conn_all(R, up4, dn4)
zero = float(np.mean(s_null == 0.0))
nz_sd = float(np.std(s_null[s_null != 0.0], ddof=1))
report(4, "null distribution over 4,000 random signatures (978 genes, 150 up and 150 down)",
       0.41 <= zero <= 0.47 and 0.060 <= nz_sd <= 0.074 and abs(float(s_null.mean())) < 0.01,
       f"exactly zero {100 * zero:.1f}%   sd of nonzero {nz_sd:.4f}   mean {s_null.mean():+.5f}")

# 5. An incoherent query, both sets enriched at the same end, returns EXACTLY zero.
o = np.argsort(-sig, kind="stable")
inc_up, inc_dn = o[:k].copy(), o[k:2 * k].copy()
s_inc = conn_all(M, inc_up, inc_dn)[0]
report(5, "incoherent query (both sets at the top of the signature) returns exactly zero",
       s_inc == 0.0, f"score {float(s_inc)!r}")

# 6. Reversing the signature. Asserted: the self-query negates exactly, and over 5,000 random
#    queries every pair in which both scores are nonzero negates exactly. Measured, not asserted:
#    how often one score is exactly zero and its reversed counterpart is not.
s_rev = conn_all(-M, up, dn)[0]
worst_nonzero, exceptions, n_q = 0.0, 0, 5000
for _ in range(n_q):
    p = rng.permutation(n)
    a, b = p[:k].copy(), p[k:2 * k].copy()
    s1, s2 = conn_all(M, a, b)[0], conn_all(-M, a, b)[0]
    if (s1 == 0.0) != (s2 == 0.0):
        exceptions += 1
    else:
        worst_nonzero = max(worst_nonzero, abs(s1 + s2))
report(6, "reversing the signature negates the score exactly, outside the zero rule",
       abs(s_rev + s_self) < TOL and worst_nonzero < TOL,
       f"self-query {s_self:+.12f}   reversed {s_rev:+.12f}   worst |sum| where neither score is zero {worst_nonzero:.2e}")
print(f"    measured, not asserted: in {exceptions} of {n_q} random queries ({100 * exceptions / n_q:.1f}%) one score is exactly\n"
      f"    zero and its reversed counterpart is not")

print(f"\n{sum(results)} of {len(results)} controls pass   (seed {SEED}, numpy {np.__version__})")
sys.exit(0 if all(results) else 1)
