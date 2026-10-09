# Independent review — NOGO-OBLIQUE-03

- reviewer: `/root/oblique_nogo_review`
- reviewed artifact: `research/delta-discovery-2026-10-08/rejected/NOGO_OBLIQUE_03.md`
- exact artifact SHA256: `53d01b03262fbdce306c3021847efc849b9c946ca24a3db20e6846641666890d`
- verdict: **VERIFIED_NO_GO_CONTROL**

The two-dimensional block is correctly oriented: its columns are the coordinates of \(Ak\) and \(Au\) in the ordered basis \((k,u)\).  The stated \(B^\top B\) trace and determinant produce the exact eigenvalues.  If the perpendicular coefficient \(s\) is nonzero, the unit witness \(u\) gives \(\|Au\|_2^2=1+s^2>1\), so the bare factor is expansive for every \(c\).  If \(s=0\), the exact norm is \(\max\{1,|1-c|\}\) (with the orthogonal-complement term absent in one dimension), hence nonexpansiveness is equivalent to \(c\in[0,2]\).  The identity and Householder boundary cases are correct.

The scope restriction is essential and is present in the reviewed bytes.  Expansion of \(A\) alone does not imply expansion of \(AD\) or \(DA\); a sufficiently contractive decay can suppress it, and multiplication order cannot be exchanged.  The result is limited to Euclidean/Frobenius geometry and does not rule out a compensating metric or explicitly accepted transient expansion.

This is elementary rank-one linear algebra and properly remains a no-go/control rather than a candidate.  No files were edited by the reviewer, and no project code, tests, models, benchmarks, training, inference, scorer or GPU work was executed.
