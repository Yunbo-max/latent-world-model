# Corrections discovered during first CPU verification

## Archived SPD rank-one theorem: identity degeneracy

The pinned control `rejected/LYAPUNOV_OBLIQUE_METRIC.md` states that an SPD H
with A^T H A <= H for A=I-wr^T exists iff0<r^T w<=2,without explicitly
excluding zero factors. For w=0 or r=0,A=I and every SPD H is a certificate
although r^T w=0. The accompanying Hw=alpha r requirement also is not necessary
for an identity map.

Correct scoped statement: if wr^T=0,the map is identity and an SPD certificate
exists. Otherwise both w and r are nonzero,and existence is equivalent to
0<r^T w<=2,with the stated alignment proof applicable. Numerical witness uses
w=(0,0),r=(1,0),H=I;zero slack contradicts the unqualified archived iff.

The nondegenerate construction and whitening-equivalence result are preserved.
This is an assumption repair,not a new algorithm or a refutation of the entire
Delta programme. Original source bytes are retained;the correction is a linked
new record. The correction was noticed during independent definition review and
then actually exercised by the root CPU suite.

## Implementation and reporting repairs

- Initial feedback script had unmatched parentheses. The failed source and actual
  stderr/receipt remain;the repaired task uses a new identity and output path.
- Source capture added a trailing newline. Removal occurred only when the exact
  expected Git blob hash verified the recovered original bytes;all70 match.
- Proc child RSS sampling was unavailable across PID namespaces. New reports use
  Linux kernel RUSAGE_CHILDREN and state its scope;old zero-sample telemetry is
  retained and does not mean zero memory use. RLIMIT_DATA is an allocation limit.
- BLAS/OpenMP thread variables do not prove solver concurrency. HiGHS is now
  explicitly requested to use one thread;actual thread count remains unmeasured.
- The R18/A21 ledger leak and envelope values were coefficients. Revised outputs
  additionally report absolute energy bounds multiplied by pairwise_radius^2.
- The feedback witness now implements four actual decision rules. Its future-
  informed control has extra information and is not a deployable fair competitor.
