# Independent math review — query-weighted finite-bit rate--distortion

Reviewer: \`/root/capacity_candidate\`  
Final artifact SHA256: \`1f594e23635b0697ab4cf548e3d182c43faa526b28598f1628598801ff70b9a9\`  
Method: static exact-byte review; no edits, model execution, or experiment.  
Verdict: **PASS within the stated theorem/control scope.**

The review initially failed earlier byte generations and caused four substantive scope repairs: fixed conditional second moment is sufficient but not equivalent to query independence; the Fano bound needs code-before-query timing; a vector \(L_2\) moment is needed for the conditional mean; and state-dependent query laws invalidate a fixed Gram only when the conditional second moment changes. It also forced the R19 statement to be narrowed from theorem equivalence to the same \(q^r\) numerical endpoint after quotient-coordinate identification.

On the final bytes:

- \(W_\pi=I_{d_v}\otimes G_\pi\) has the correct dimensions and gives the trace/weighted-norm identity.
- The observation/coding orthogonal decomposition is exact under \(Z\leftarrow O\), conditionally independent encoder randomness, and \(\mathbb E\|x\|^2<\infty\).
- A \(2^B\)-message one-state code is a subset of the Shannon coding class, so the Gaussian reverse-water-filling distortion is a lower bound, not an achievability claim.
- The endpoint uniform-quantizer and Gaussian clipping bounds have the correct spacing, variance factor, and tail term.
- With \(p(z\mid C,J)=p(z\mid C)\), coordinate Fano, conditional entropy subadditivity, and concavity yield equation (11); \(D=0\) gives the scoped \(r\log_2q\) endpoint.
- No blocking mathematical defect remains.

This PASS does not establish originality, an executable updater, native measurement, empirical gain, scientific admission, or selection.
