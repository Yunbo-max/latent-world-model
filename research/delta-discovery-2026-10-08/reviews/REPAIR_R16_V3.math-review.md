# R16 v3 independent final-byte mathematics review

- Reviewer: \`/root/commutator_compensation_math\`
- Artifact: \`repairs/R16_SHARED_CARRIER_SCAN.v3.md\`
- Artifact SHA256: \`48ec9e9e1c94191df3e8e5e8c87e810d4119d9d902ec61dd63e14d8c39ea0b4d\`
- Source audit: \`sources/R16_V3_SHARED_CARRIER_SCAN_SOURCE_AUDIT.md\`
- Source SHA256: \`e58768e3c40dc7ca8c26a7e0926a5b9a8b811b01401c83c543fdd99597407465\`
- Execution: static mathematics/source-interface review only; no file edits or project/model/benchmark execution.
- Verdict: **PASS as a terminal conditional theorem/control; not a candidate.**

Both ordered product telescopes have the correct chronology. The factor ledger reproduces the baseline-suffix/actual-prefix form because \((P_{j-1:a}^{\top}R_j)^\top=R_j^\top P_{j-1:a}\), and all factors have compatible dimensions. The rank bound \(\operatorname{rank}(P-Q)\le\min(d,\sum_j s_j)\) follows without assuming a common token basis.

The orthogonal construction \(\Lambda_j=0,\ k_j=e_j\) is a sharp legal R16 witness: the factors commute, yet \(P_{H:1}-I\) has rank \(H\) while each one-token active core has rank one. The revised affine statement correctly requires \(m\ge H\) and independent value rows to attain key-side rank \(H\).

Under \(\Lambda_t\mathcal U\subseteq\mathcal U,\ k_t\in\mathcal U\), symmetry makes \(\mathcal U\) reducing for \(A_t,E_t\), confines the source to the carrier, and yields the exact core/complement affine scan. The fixed-\(U\), two-sided-support equivalence in (19a)–(19b) is valid by the unique symmetric principal logarithms of positive-definite \(A_t,E_t\); it is correctly not claimed universal over other operator algebras or asymmetric encodings.

The revised invariant hull uses the declared natural-flow pure-decay family. Since its seed contains every \(\operatorname{range}(C_t)\), \(A_t\)-invariance also implies \(E_t=(A_t+C_t)\)-invariance. Online causal carriers and offline chunk executors are now separated correctly. General non-symmetric exact-write carriers still require the stated left/right or transpose closure.

The recompression recursion \(F_t=E_tF_{t-1}+R_t\) and Frobenius bound follow from \(\|E_t\|_2\le1\) for the natural PSD exponential. No semantic-loss, backward-error, or exact-write contraction conclusion is inferred. The complement is independently represented and charged, so a small active core is not misreported as a universally compact full scan.

The source audit now correctly separates Martin–Cundy's general affine-scan theory from its author's diagonal/elementwise CUDA implementation. The positive construction remains the same operation as a direct reduced affine recurrence, and the negative/maintenance results substantially overlap generic affine scan, Delta/WY and internal R10/R11/R12.

**Disposition:** park after attempt 3/3; candidate, scientific-admission and selection deltas remain zero.
