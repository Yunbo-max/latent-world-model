# R19 v3 — finite-field syndrome release and exact no-advantage boundary

Status: **conditional theorem/debug control; substantive attempt 3 of 3; not an active D candidate**. This child preserves R19 v1/v2. It reopens the lineage only on v2's declared condition: a structured Delta release family whose exact prefix code is tractable and can be compared at matched information and precision with the direct-signature/R18 ledger. The structured code is tractable and sometimes compresses a naive per-branch signature, but it is exactly the strongest quotient-ledger baseline. Therefore the repair yields a sharp terminal theorem, not a new updater.

## 1. Original problem, exact patch, and scope

R19 v2 solves a finite one-shot release by coloring a general confusability graph. Its exact optimum can be computationally intractable, and its only legitimate third-attempt reopening condition was a structured family with a provable total-cost advantage over direct storage and R18's prefix-robust ledger.

The v3 patch restricts the finite state to a declared algebraic model. Let \(\mathbb F_q\) be a finite field and let the pre-write hidden coordinate range over the entire declared vector space

\[
z\in\mathbb F_q^n.
\]

The destructive post-write state reveals

\[
s=Az,\qquad A\in\mathbb F_q^{a\times n}. \tag{1}
\]

A branch label \(m\in\{1,\ldots,M\}\) is revealed only after the prefix code has been written. On branch \(m\), the exact released target is

\[
y_m=B_mz+b_m,
\qquad B_m\in\mathbb F_q^{o_m\times n},\quad b_m\in\mathbb F_q^{o_m}. \tag{2}
\]

The lawful branch family and matrices are fixed by the prefix. Every branch is lawful for every state in this theorem. Thus the same-state/visible-label feasibility defect from v2 is absent: a fixed \((z,m)\) has one target. State-dependent lawful branch sets or hidden sublabels fall back to the general v2 graph and need not have the structure below.

The encoder chooses a fixed-length classical message \(c(z)\in\{1,\ldots,L\}\) before \(m\) is known. For every \(m\), a decoder must satisfy

\[
d_m(Az,c(z))=B_mz+b_m \quad\text{for all }z. \tag{3}
\]

This is an exact, noiseless, one-shot finite-field abstraction. It is not a bit-exact model of floating-point Delta arithmetic, not an approximate continuous-state result, and not a repeated-write stability theorem.

Write the stacked release map

\[
B=\begin{bmatrix}B_1\\ \vdots\\ B_M\end{bmatrix},
\qquad
H=\ker A\cap\ker B. \tag{4}
\]

The relevant quotient dimension is

\[
r=\dim\ker A-\dim H
=\operatorname{rank}\!\begin{bmatrix}A\\B\end{bmatrix}-\operatorname{rank}(A). \tag{5}
\]

## 2. Exact graph structure and optimum

Two states are confusable precisely when the decoder sees the same post-write side information but some later branch asks for different targets:

\[
z\sim z'
\Longleftrightarrow
A(z-z')=0\ \text{ and }\ B(z-z')\ne0. \tag{6}
\]

Equivalently, within a fixed \(A\)-fiber, two vertices are nonadjacent exactly when they lie in the same coset of \(H\).

**Theorem 1 (structured one-shot optimum).** The graph in (6) is a disjoint union, over the distinct values of \(Az\), of complete \(q^r\)-partite graphs. Every part is an \(H\)-coset. Consequently

\[
\boxed{\chi(G)=q^r,\qquad
\min \lceil\log_2 L\rceil=\lceil r\log_2q\rceil.} \tag{7}
\]

*Upper bound.* Choose a linear map \(C\in\mathbb F_q^{r\times n}\) satisfying

\[
\ker A\cap\ker C=H. \tag{8}
\]

Such a map is obtained by taking a row-space complement of \(\operatorname{row}(A)\) inside \(\operatorname{row}([A;B])\). The message is \(Cz\), with at most \(q^r\) values. For every branch,

\[
\operatorname{row}(B_m)\subseteq \operatorname{row}\!\begin{bmatrix}A\\C\end{bmatrix}, \tag{9}
\]

so there are matrices \(D_m,E_m\) with \(B_m=D_mA+E_mC\). The decoder returns

\[
d_m(s,u)=D_ms+E_mu+b_m. \tag{10}
\]

*Lower bound.* Fix one \(A\)-fiber and choose a vector-space complement \(T\) of \(H\) inside \(\ker A\). Then \(\dim T=r\). Any two distinct points in a translate of \(T\) differ by a nonzero element of \(T\subseteq\ker A\) that is not in \(H\); hence they are adjacent. The graph contains a clique of size \(|T|=q^r\), so every deterministic exact code needs at least \(q^r\) messages. Together with the upper bound, this proves (7).

The offsets \(b_m\) do not affect confusability because the same visible branch label is compared on both states and the offset cancels. They remain in the decoder.

## 3. Nonlinear and randomized encoders do not beat the rank

The lower bound is a clique bound on the general v2 confusability graph, not a restriction to linear encoders. Therefore an arbitrary nonlinear fixed-length encoder still needs \(q^r\) messages.

Private randomness cannot reduce the alphabet under exact zero error: adjacent states must have disjoint message supports, so the same clique requires at least \(q^r\) distinct messages. With shared randomness known to the decoder, almost every seed must induce a correct deterministic coloring on this finite domain and again needs \(q^r\) colors. If the requirement is weakened to average error, outage, variable length or asymptotic block coding, the object changes and (7) is not the relevant optimum.

This distinction prevents a false repair: learned stochastic routing can trade error against rate, but it does not refute the exact one-shot bound.

## 4. Delta specialization and old-counterexample recheck

For a quantized algebraic proxy of a destructive Delta event, \(A\) represents the post-write information remaining about a declared finite hidden coordinate, while the \(B_m\) are all prefix-lawful later released reads transported along their branch labels. The exact syndrome stores only the part of the joint released row space that is absent from the post-write row space.

The v2 complementary-branch witness is the case \(q=2\), \(A=0\), \(B_1=[1\ 0]\), and \(B_2=[0\ 1]\). Then \(r=2\), \(\chi(G)=4\), and two bits are necessary. The v1 one-coordinate witness has \(r=1\) and needs one bit. Thus both old counterexamples survive exactly.

If \(B_m\)'s rows all lie in \(\operatorname{row}(A)\), then \(r=0\): the post-write state already determines every release and no side code is needed. If the stacked release map is injective on \(\ker A\), then \(r=\dim\ker A\): exact release needs the entire lost coordinate. These limiting cases match the intended information geometry.

Finite-field arithmetic is a structural audit, not a silent physical assumption. A floating or integer implementation needs an explicit quantizer, range, overflow rule, noise model and distortion claim. Mapping arbitrary real Delta states into \(\mathbb F_q^n\) can change kernels and releases; no transfer theorem is asserted.

The full-space assumption is also substantive. If the reachable set is one affine subspace \(z_0+U\), equation (5) must be restricted to its direction space:

\[
r_U=\operatorname{rank}\!\begin{bmatrix}AU\\ BU\end{bmatrix}-\operatorname{rank}(AU). \tag{11}
\]

For an arbitrary reachable subset, even this formula can fail and the exact v2 graph is required. For example, with \(q=2\), \(n=1\), \(A=0\), \(B=1\), but reachable set \(\{0\}\), the ambient formula gives one bit while the actual optimum is zero bits.

## 5. Construction and actual cost

The structured class removes general graph coloring from the construction:

1. stack the lawful release matrices into \(B\);
2. compute a row-space basis for \([A;B]\);
3. select \(r\) complement rows modulo \(\operatorname{row}(A)\) to form \(C\);
4. solve the factorizations in (9); and
5. before destructive writing, retain \(u=Cz\); after observing \(m\), apply (10).

Dense Gaussian elimination is polynomial rather than chromatic-number search. A conventional implementation uses cubic-order preprocessing in the aggregate matrix dimensions, then \(O(rn)\) field operations per encode plus branch-dependent decoder multiplies. Runtime state is exactly \(r\) \(q\)-ary symbols, or \(\lceil r\log_2q\rceil\) bits only when the field symbols are stored without extra framing/error protection. Matrices \(C,D_m,E_m\), branch labels, quantization metadata and decoder compute remain charged.

This can be smaller than a **naive** concatenation \((B_1z,\ldots,B_Mz)\), whose nominal width is \(\sum_m o_m\), and smaller than storing the full \(z\). But a strong direct signature first removes row dependencies and information already visible in \(Az\). Its minimum additional width is exactly (5). R18's direct joint-row ledger performs the same quotient. Thus the syndrome construction has no state advantage over the strongest same-information baseline; it is merely an efficient coordinate realization of that baseline.

## 6. Why this exhausts, rather than rescues, R19

V2's attempted reopening criterion had two parts: tractability and a matched-cost advantage. V3 satisfies the first but disproves the second for the cleanest structured family.

- General nonlinear finite release: exact optimum is graph coloring, already classical zero-error function computation.
- Linear finite-field release: graph coloring collapses to Gaussian elimination, but the optimal message is exactly the quotient/direct ledger.
- Linear real release: v2 equation (10) already gives the same row-rank quotient in real coordinates.
- Restricted or irregular reachable sets: use (11) only for one affine subspace; otherwise translation invariance can disappear and the general v2 graph is required.
- Hidden/state-dependent branches: the rank formula can overcount or become infeasible. If only label \(m=z\) is lawful in a binary scalar example, the later label already reveals \(z\), while blindly stacking both labels predicts an unnecessary bit. Hidden branches sharing one visible label but requiring different targets violate v2 feasibility and no code size repairs them.
- Approximate/noisy release: a distortion/noise/rate object is required and can no longer inherit the zero-error theorem.
- Repeated destructive writes: the code itself must have a lawful transition and stability/precision analysis; a one-shot syndrome is insufficient.

Therefore there is no remaining mathematical patch inside the bounded R19 lineage that both respects the information timing and yields a distinct updater. Reopening again would require new external evidence or a genuinely different scientific object, not a fourth reparameterization.

## 7. Predictions, falsifiers, and strong controls

Conditional predictions:

1. for the declared finite-field linear family, measured optimal exact message count equals \(q^r\);
2. any implementation claiming fewer messages must fail on at least one pair in a size-\(q^r\) clique, unless it changes the information, error, variable-length or block-coding contract;
3. storing every branch target can appear more expensive only when it fails to remove linear dependencies or post-write-visible information;
4. state-dependent branch sets can destroy the complete-multipartite structure and return the problem to general graph coloring.

Falsifiers are an exact code with fewer than \(q^r\) messages under (1)--(3), or a same-information implementation whose retained state is smaller than the quotient while remaining exact on all states and branches. The clique proof rules out both inside the theorem's scope.

Strong controls are: the row-reduced direct target signature; R18's joint-row ledger; full pre-write state; no write/fixed protection; R08's same-evidence release decision; a general v2 optimal coloring on small declared alphabets; and a set-valued observer when branch/state uncertainty is retained.

## 8. Measurement boundary and disposition

LongMemEval, LongMemEval-V2, EvoMemBench, AToKE, SEAL, bAbI, LAMBADA, RULER and BABILong can measure downstream answer, retrieval, temporal-update or forgetting outcomes of a future implementation. They do not natively expose \(A\), the lawful family \(B_m\), the quotient rank \(r\), a size-\(q^r\) clique, exact field-valued release, or matched retained bits. An instrumented algebraic diagnostic would be derived rather than native evidence. The central mechanism therefore remains unmeasured by existing native scorers.

**Decision:** the mathematics is accepted only as an exact finite-field, one-shot, zero-error theorem and terminal debugging control. It makes the v2 graph optimum tractable, but the resulting syndrome is functionally identical to the strongest direct/R18 quotient ledger. R19 has exhausted substantive attempt 3 of 3 and is parked with `candidate_delta=0`; empirical effect remains unknown. No project/model code, tests, training, inference, scoring, dataset/model download, GPU job or Docker was used.
