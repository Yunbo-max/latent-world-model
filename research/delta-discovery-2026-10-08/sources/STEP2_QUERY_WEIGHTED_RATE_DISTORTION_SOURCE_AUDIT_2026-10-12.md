# Source audit — query-weighted finite-bit rate--distortion boundary

Date: 2026-10-12  
Scope: version-pinned literature/mechanism audit for `STEP2_QUERY_WEIGHTED_RATE_DISTORTION_2026-10-12.md`, using primary papers plus one explicitly marked survey. This is not a broad originality guarantee, implementation verification, or experimental result.

## Sources read

1. Nir Shlezinger and Yonina C. Eldar, **Task-Based Quantization with Application to MIMO Receivers**, arXiv:2002.04290v1, 2020, explicitly identified here as a survey; abstract and full HTML through Section III-A, especially Definition 1 and the MMSE/excess-MSE decomposition at lines corresponding to Sec. II--III.  
   Version URL: https://arxiv.org/abs/2002.04290v1  
   Relevant content: finite codebook definition; rate/distortion setup; indirect rate--distortion framing; for MSE, quantize the MMSE statistic; exact decomposition
   \[
   \mathbb E\|s-\widehat s\|^2
   =\mathbb E\|s-\mathbb E[s\mid x]\|^2
   +\mathbb E\|\mathbb E[s\mid x]-\widehat s\|^2.
   \]

2. Nir Shlezinger, Yonina C. Eldar, and Miguel R. D. Rodrigues, **Hardware-Limited Task-Based Quantization**, arXiv:1807.08305v1, 2018; later IEEE Transactions on Signal Processing.  
   Version URL: https://arxiv.org/abs/1807.08305v1  
   Relevant content: primary fixed-finite-resolution task-based quantizer construction and achievable distortion under downstream estimation objectives.

3. J. K. Wolf and J. Ziv, **Transmission of Noisy Information to a Noisy Receiver with Minimum Distortion**, IEEE Transactions on Information Theory 16(4), 1970.  
   Fixed DOI: https://doi.org/10.1109/TIT.1970.1054469  
   Relevant content: primary noisy/indirect source-coding basis for reducing MSE estimation to coding an appropriate conditional statistic.

4. Photios A. Stavrou and Mikael Skoglund, **Indirect NRDF for Partially Observable Gauss-Markov Processes with MSE Distortion: Complete Characterizations and Optimal Solutions**, arXiv:1912.07640v4, 2021-10-20; later IEEE TAC 2024, DOI 10.1109/TAC.2024.3364028.  
   Version URL: https://arxiv.org/abs/1912.07640v4  
   Relevant content: finite-horizon indirect nonanticipative RDF for partially observed multivariate Gauss--Markov processes; current-time sufficient statistic; SDP characterization; dynamic reverse-water-filling; steady-state conditions. This directly covers the general causal/partial-observation class surrounding equations (4), (8)--(10), not the exact Delta notation.

5. Photios A. Stavrou, Themistoklis Charalambous, Charalambos D. Charalambous, and Sergey Loyka, **Optimal Estimation via Nonanticipative Rate Distortion Function and Applications to Time-Varying Gauss-Markov Processes**, arXiv:1603.04172v3, 2017-02-10; SIAM JCO, DOI 10.1137/17M1116349.  
   Version URL: https://arxiv.org/abs/1603.04172v3  
   Relevant content: finite-time causal filters as encoder/channel/decoder realizations; conditional-mutual-information lower bound; multidimensional time-varying Gauss--Markov reverse water-filling. This blocks any claim that causal rate--distortion or recursive Gaussian reverse water-filling is new here.

6. Hang Zou, Chao Zhang, Samson Lasaulce, Lucas Saludjian, and H. Vincent Poor, **Goal-Oriented Quantization: Analysis, Design, and Application to Resource Allocation**, arXiv:2209.15347v1, 2022.  
   Version URL: https://arxiv.org/abs/2209.15347v1  
   Relevant content: quantizer design for a downstream goal function rather than source reconstruction; high-resolution analysis and task-specific quantizer construction. This is a direct mechanism collision for calling a query-weighted distortion "semantic" novelty.

7. Packet-internal exact controls read at these local artifact bytes: `R17_CAUSAL_PREDICTIVE_LEAKAGE_CERTIFICATE.v2.md` (`c7f7843a9508dbb5cc6fdf9525e23dc311eff070f58b572bb133850722eb1438`), `R17_RESIDUAL_SCALED_SPECTRAL_CERTIFICATE.v3.md` (`f7bf7ce4f7e94262ec337ebd299a7ffe7cd7ee6dd883b5b7c4e016fcf1e322d0`), `R18_RECURSIVE_JOINT_QUOTIENT.v1.md` (`1ba72192c2712e85937fddc8ed23b9b062c45ba59e664fca27e563c075be4873`), `R18_BOUNDED_FIBER_LEAKAGE_LEDGER.v3.md` (`947ef43e1b5f34adb4e5badf07c0ca8fb68c01a31128f77dc3a433ce1b256879`), `R19_PREFIX_CAUSAL_BRANCH_CODE.v2.md` (`0d771029d39677e8077b7c23d761c90b2c9ffaecf03b81781a078ec8561ed105`), and `R19_FINITE_FIELD_SYNDROME_RELEASE.v3.md` (`ea932cd7350806d52d66f2fd243f9d9e23a849dabfae438ce10183e34c40fc49`). Existing reviews remain bound to their recorded historical bytes; this audit directly reread the listed current artifact bytes and does not silently rebind old reviews.  
   Relevant content: lawful prefix query/observability Gram; spectral tail; recursive quotient and kernel compatibility; bounded fiber ledger; characteristic-graph/branch-code formulation; exact finite-field (q^r)-message lower bound.

## Mechanism mapping

| New artifact component | Closest covered mechanism | Residual value |
|---|---|---|
| fixed-query Gram (W_\pi=I\otimes G_\pi) | task-based distortion; R17 observability/query Gram | Delta matrix notation only |
| (D_{\mathrm{obs}}+D_{\mathrm{code}}) split | indirect task-based quantization/MMSE decomposition | makes declared-state non-identifiability explicit in the Delta packet |
| Gaussian reverse water-filling lower bound | classical Gaussian RDF; indirect/nonanticipative Gaussian RDF | one-state converse warning and Delta-weighted eigenvalues |
| fixed-codebook clipping/quantization upper bound | standard scalar/vector quantization | explicit finite-range implementation bound, not new mechanism |
| recursive metric inequality | causal filtering/NRDF; R17--R18 observability | explicit kernel-compatibility condition and bridge-query counterexample |
| (q)-ary Fano lower bound | lossy source coding; R19 zero-error code | recovers the same (q^r) numerical endpoint under the quotient-coordinate identification |

## Formula and claim audit

- The fixed-Gram equality requires a query law independent of the encoded error or a fixed conditional second moment. The artifact states this and does not apply an unconditional average Gram to state-dependent queries.
- The indirect orthogonal split requires the reconstruction to be generated from the allowed observation. Encoder randomness is permitted only conditionally independent of the latent state given that observation.
- Gaussian reverse water-filling is used only under a Gaussian source; the indirect extension explicitly assumes a jointly Gaussian observation model. It is stated as a lower bound for a single finite codebook, not as one-token achievability.
- The recursive seminorm bound now includes the necessary kernel condition. Without it, the pseudoinverse expression alone is insufficient; a previously invisible direction can become visible.
- The uniform-quantizer upper bound uses endpoint levels and a declared finite range. The Gaussian tail term is clipping loss, and overflow/saturation are not hidden.
- The discrete lower bound follows from coordinate-wise Fano plus entropy subadditivity and concavity; at zero error it recovers the same (q^r) numerical lower bound after the quotient-coordinate identification, not R19's full branch/side-information theorem.
- Equations (2)--(4) use the standard Gaussian quadratic RDF/reverse-water-filling result and apply it to the displayed weighted Gaussian coordinates. Equations (11)--(12) give their own coordinate-wise Fano/entropy derivation. These formula families are treated as self-contained standard derivations here, not claimed as new and not attributed solely to the neighboring mechanism papers.
- Equation (1) decomposes distortion of the declared latent \(x=\operatorname{vec}(S)\). It does not measure an external provenance, validity, or correct-action label absent from \(x\) and the declared distortion.

## Implementation and native measurement audit

No new implementation or project code was inspected or run because the artifact does not propose an executable candidate. Author-code availability and implementation semantics were not verified, and no absence claim is made. The cited papers establish general coding/filtering mechanisms, not a verified ready-made Delta implementation.

The packet's established native benchmark set measures endpoint answers, retrieval, temporal updates, or forgetting. It does not natively expose the latent/observable MMSE split, exact message alphabet, query Gram available at write time, codebook and metadata bits, recursive kernel compatibility, quantization-noise sequence, or a matched task-aware direct-ledger curve. Therefore the current result remains a mathematical feasibility/control record with a measurement gap; it is not an experimental negative.

## Source decision

The primary sources strongly cover task-aware, indirect, goal-oriented, and causal/nonanticipative rate--distortion mechanisms. Packet-internal R17--R19 cover the Delta-specific observability, recursive quotient, bounded ledger, and exact discrete endpoint. No evidence supports a new updater or a strict matched-cost advantage. Retain `theorem/control`, `candidate_delta=0`, empirical effect unknown.
