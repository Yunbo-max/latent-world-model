# R13 v3 independent final-byte mathematical review

- Reviewer: /root/r13_v3_math
- Assignment: independent dimension, necessity/sufficiency, construction, conditioning, horizon and switching audit
- Math artifact SHA256: 17b8dc6e2ac819957347ed4cd617cda22bf42ac8b9b9c0439fbf774adcb2b75d
- Repair screen SHA256: 4ea68df206d2f415a6474a3f2741d372f5c1fb209343b46ff71e863bc96daae8
- Verdict: **CONDITIONAL PASS for the scoped theorem/debug control**

The reviewer independently recomputed both hashes and found no remaining control-character or LaTeX corruption.

The affine coefficient condition \(XA+KL^\top=Q^\top\) and offset \(C=C_0-XB\) are dimensionally correct. Restricting to \(\ker A\) proves the lower bound \(s\ge\operatorname{rank}(Q^\top N)\). The thin-SVD choice \(L=NV_\ell,\ K=U_\ell\Sigma_\ell\), followed by \(X=(Q^\top-KL^\top)A^\dagger\), attains it because the remainder annihilates \(\ker A\).

Under vectorization, the post-map kernel is \(\mathbb R^{d_v}\otimes\ker A\), so its target image has rank \(d_v\operatorname{rank}(Q^\top N)\). This proves the unrestricted real-linear scalar-coordinate lower bound. The kernel-projected Eckart--Young tail is both lower-bounded and attained by the stated construction.

The spectral-cut equations and norm bound are correct. The rewritten artifact properly restricts the \(G_\tau\) tail to a fixed or constrained cut decoder and distinguishes it from the unconstrained invertible case. The normalized factorization makes the noise statement interpretable.

For \(A=(I-\beta kk^\top)D\), exact overwrite has \(\ker A=\operatorname{span}(D^{-1}k)\); hence nonzero overlap requires exactly one \(d_v\)-vector. The known-horizon product order and causal restriction are correct. For partial no-decay modes, arbitrary-switch bounded transport is equivalent to the common orthogonal fixed space because a repeated overlapping mode amplifies geometrically.

The old hidden-mode, semantic-validity, nonlinear/full-Jacobian, finite-bit and matched-cost boundaries remain explicit. This review does not establish originality, scientific admission, native measurement, semantic validity, or empirical benefit. Attempt 3/3 may be exhausted and parked.

