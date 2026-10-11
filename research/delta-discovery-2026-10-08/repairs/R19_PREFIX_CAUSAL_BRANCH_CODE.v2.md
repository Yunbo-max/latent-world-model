# R19 v2 — prefix-causal branch code for a switched protection release

Status: **conditional theorem/debug control; substantive attempt 2 of 3; not an active D candidate**. This child preserves R19 v1 and replaces its realized/common-branch assumption by a finite, prefix-measurable nonlinear branch relation. It derives the exact one-shot zero-error side-state requirement at a destructive release. It does not identify obsolete facts, prove a new updater, or report an experiment.

## 1. Original failure, patch, and formal object

R19 v1 uses a complete-state tangent `h`, a PSD energy `P_sigma`, and one realized reset/mode. Its cross-mode condition

\[
\ker P_\sigma\subseteq\ker(R^\top P_\tau R)
\]

is exact on that branch. At a state-dependent guard, however, arbitrarily close states can take different branches; an ordinary Jacobian product does not bound the cross-branch jump. Conditioning on the branch that will later occur is also an unavailable future oracle at the current write.

The v2 patch makes the deployment information and finite-precision assumption explicit. At a prefix time `t`, let

- `X` be a finite reachable state alphabet (for example the actual bounded finite-precision recurrent state, not an uncountable real state silently encoded in finitely many bits);
- `W:X->Z` be the destructive Delta write/post-write state visible to the later decoder;
- `B(x)` be the nonempty finite set of branches still lawful from `x` under a prefix-declared transition relation;
- `lambda(b)` be the branch/reset label actually visible to the decoder after the switch; and
- `g_b(x)` be the exact released object required on branch `b`, such as a protected read or a newly exposed coordinate after its complete reset.

All sets, maps, labels and numerical values above are fixed by the lawful prefix or a declared prefix-time model. The encoder must choose a side code

\[
c:X\to\{1,\ldots,M\} \tag{1}
\]

before the future branch is revealed. After the switch a branch-specific decoder may use only `(W(x),c(x),lambda(b))`:

\[
d(W(x),c(x),\lambda(b))=g_b(x),\qquad b\in B(x). \tag{2}
\]

If the branch label is unavailable, take `lambda` constant. If the full pre-write state remains available after the label arrives, then `W` already retained it and the claimed storage saving must be charged there. Choosing `c_b` only after observing `b` is unlawful whenever `W` has already erased the needed distinction.

This is a zero-error recoverability problem, not a probability or average-loss claim. A learned uncertainty set gives only a conditional claim on the event that the realized branch belongs to it; self-generated futures do not establish that coverage.

There is also a feasibility condition that storage cannot repair. For every fixed state, the visible label must determine a unique owed target:

\[
\forall x\in X,\ \forall b,b'\in B(x):\quad
\lambda(b)=\lambda(b')\Longrightarrow g_b(x)=g_{b'}(x). \tag{F}
\]

If (F) fails, the decoder receives the identical triple for two different targets even with an arbitrarily large code, because the encoder cannot assign two messages to the same `x`. In that case no exact code exists and we set `M^*=infinity`. Condition (F) is not an innocuous regularity assumption: it says that every target-relevant part of hidden branch identity is either observable in `lambda` or irrelevant to the requested release. In particular, a constant label is lawful only when the released target is single-valued at each fixed state across all still-hidden branches.

## 2. Exact confusability graph theorem

Define an undirected graph `G_R19=(X,E)` whose vertices are reachable pre-write states. Distinct `x,y` are adjacent when the later decoder can receive identical side information but would owe different outputs:

\[
\{x,y\}\in E
\Longleftrightarrow
W(x)=W(y)
\ \text{and}\ 
\exists b\in B(x),b'\in B(y):
\lambda(b)=\lambda(b'),\ g_b(x)\neq g_{b'}(y). \tag{3}
\]

**Theorem 1 (one-shot prefix code).** If (F) fails, no exact code/decoder pair satisfying (1)--(2) exists for any `M`. If (F) holds, such a pair exists with alphabet size `M` if and only if `G_R19` is `M`-colorable. Consequently, in the feasible case, the minimum one-shot fixed-length side-state alphabet and bit width are

\[
\boxed{M^*=\chi(G_{R19}),\qquad
b^*=\lceil\log_2\chi(G_{R19})\rceil.} \tag{4}
\]

*Necessity.* If adjacent `x,y` received the same code, the witness branches in (3) would present the same `(W,c,lambda)` to the decoder but require two different released values. Hence every valid code is a proper coloring.

*Sufficiency.* Let `c` be a proper coloring. Fix any visible triple `(z,a,l)`. If two compatible state/branch pairs `(x,b)` and `(y,b')` yield this triple, then `W(x)=W(y)`, `c(x)=c(y)` and `lambda(b)=lambda(b')`. If `x=y`, condition (F) rules out unequal targets. If `x\ne y`, proper coloring rules them out. Define `d(z,a,l)` to be this common value. Thus (2) holds.

Equation (4) is exact only for the declared finite alphabet, one-shot fixed-length classical code, visible label and zero-error target. It is not a universal bit bound for real-valued states. Variable-length, block, approximate, randomized or distribution-dependent codes are different claims. Exact chromatic-number computation can be NP-hard, so (4) is a characterization rather than a cheap online algorithm.

## 3. Release jump, additive error, and old counterexample

With no code (`M=1`), exact recoverability holds exactly when every post-write/label bucket is target-constant. Define its worst unresolved diameter under a metric `d_g` on released values:

\[
\Delta_0
=\max_{\substack{x,y,b,b'\\
W(x)=W(y),\ \lambda(b)=\lambda(b')}}
d_g\bigl(g_b(x),g_{b'}(y)\bigr), \tag{5}
\]

where the maximum is restricted to lawful branch pairs. Any no-code point decoder has worst-case error at least `Delta_0/2` by the triangle inequality. More generally, a code partitions `X`; its unavoidable radius is at least half the largest target diameter inside a common `(W,c,lambda)` bucket. Under a unit-weight squared-`d_g` point-decoding loss this gives a worst-case lower bound `Delta_0^2/4`. It does not by itself lower-bound an arbitrary switched-energy term; that requires an explicit domination relation between the chosen energy and `d_g^2`.

R19 v1's two-dimensional witness survives. Quantize the old neutral coordinate to `x_1 in {0,1}`, let the old energy ignore it, let `W` erase it, and let the release target be `g(x)=x_1`. The two states share `W` but require different targets, so `G_R19=K_2`, `M^*=2` and one exact bit is necessary. The v1 reset `R=diag(0,1)` instead makes the released target constant and removes the graph edge, but only by erasing that contribution.

This recheck does not convert the side code into a stability proof. Once the released object is recovered, the complete augmented state `(post-write state,code state,decoder/mode state)` must be used in a new within-mode and cross-mode analysis. Repeated additive injections in R19 v1 are ISS-style upper bounds, not cumulative memory lower bounds: the same retained bit can serve many later releases.

## 4. Same-prefix complementary branches

Let the old neutral state be two bits `x=(x_1,x_2) in {0,1}^2`, let `W` erase both, let `B(x)={1,2}` for every `x`, and let a later visible branch label be `m in {1,2}` with

\[
g_1(x)=x_1,\qquad g_2(x)=x_2. \tag{6}
\]

Every pair of distinct states differs in at least one coordinate and is therefore adjacent through the corresponding branch. Hence `G_R19=K_4`, so

\[
M^*=4,\qquad b^*=2. \tag{7}
\]

An oracle that knows the realized branch before writing stores one bit; a lawful prefix code valid for both branches needs both bits. Revealing `m` later does not undo an earlier erasure. This is the finite/nonlinear counterpart of stacking complementary linear exposure rows and of R18 v2's same-prefix quotient collapse.

For a finite family of local linear releases, let `K` have full column rank and span the old kernel coordinates `Kz`. Let `A` be the linearized post-write observation on those coordinates, so `A=W_{lin}K`, and let

\[
B_m=P_m^{1/2}R_mK. \tag{8}
\]

A single real-linear prefix code `C Kz` with mode-specific linear decoders that may also use the post-write observation `Az` exists exactly when

\[
\ker A\cap\ker(CK)\subseteq\bigcap_m\ker B_m. \tag{9}
\]

Its minimum **additional** real code width is

\[
\boxed{p^*=\operatorname{rank}\!\begin{bmatrix}A\\ B_1\\ \vdots\\ B_M\end{bmatrix}
-\operatorname{rank}(A).} \tag{10}
\]

Necessity follows because every `B_m` must factor through the total visible linear information `[A;CK]`; equivalently `row(B_m)` must lie in `row([A;CK])`. Sufficiency follows by choosing the code rows as a basis for a complement of `row(A)` inside `row([A;B_1;...;B_M])`. If the post-write map erases the entire old kernel (`A=0`), (10) reduces to the v1-style stacked rank. Equation (10) is not a new result here: it is the one-step linear specialization of R18 v2's prefix-robust quotient/direct-ledger rank. It also counts real coordinates, not finite bits.

For a lawful prefix-declared path family, replace `B_m` by every ordered transported exposure `E_omega=O_omega Xi_omega K`, where `Xi_omega` contains the actual noncommuting Jacobian/reset or admissible saltation product and `O_omega` is the eventual measured read. A code written before the path is known must complement the visible post-write row space for every `E_omega`; its minimum additional real-linear width is `dim(row(A)+span_omega row(E_omega))-rank(A)`. For a finite family this is `rank([A;stack_omega E_omega])-rank(A)`; for an infinite family, `span` denotes the joint row span rather than a literal finite matrix stack. Per-realized-path rank is an oracle underestimate whenever these row spaces are not nested. This all-path statement is precisely switched observability/R18 territory and is recorded as a control, not a new R19 mechanism.

## 5. Branch divergence and why same-branch Jacobians fail

Consider the scalar selector `b(x)=sign(x)` and two maps

\[
F_+(x)=\rho x+a,\qquad F_-(x)=\rho x-a,
\quad 0<\rho<1,\ a>0. \tag{11}
\]

Each branch derivative is `rho`. Yet for `x=epsilon` and `y=-epsilon`,

\[
|F_+(x)-F_-(y)|=2a+2\rho\epsilon,
\qquad |x-y|=2\epsilon, \tag{12}
\]

so the cross-branch incremental gain diverges as `epsilon->0`. Dwell time and hysteresis can reduce how often a guard is crossed; they do not create a finite local multiplier for a pair that splits across the guard. A tangent/saltation argument requires its own smooth, transversal event assumptions. Arbitrary routing must instead be covered by all lawful branch pairs, a set-valued relation, or the finite confusability construction above.

## 6. Information timing, construction, and cost

A literal finite-state construction is:

1. from the lawful prefix, enumerate or otherwise represent `X`, `B(x)`, `W`, visible labels and released targets;
2. build the graph in (3);
3. choose a proper coloring `c` and store its color before the destructive write;
4. after the label arrives, decode from `(W,c,lambda)`; and
5. augment the complete recurrent state with the actual code state and rederive the subsequent Jacobian/relation.

For `N=|X|`, an explicit graph can require `O(N^2 |B|^2)` target comparisons and `O(N^2)` storage; exact minimum coloring is generally intractable. A table encoder costs `O(N)` entries before compression. The runtime side state costs `ceil(log2 M)` bits only after range, quantization, codebook, decoder, branch-label reliability and update compute are all charged. A direct signature ledger storing every possible released target is a simple upper bound and may be cheaper overall than constructing the minimum coloring. A set-valued observer carries the compatible state/mode set instead; it can be much larger but supports noise and model uncertainty honestly.

If `X` is continuous, arbitrary infinite-precision encodings invalidate naive coordinate/bit claims. A finite-bit approximation needs an explicit bounded domain, noise/roundoff model, distortion `epsilon`, decoder regularity and coverage event. R19 v2 makes no such unproved extension.

## 7. Predictions, falsifiers, controls, and measurement

Conditional predictions:

1. same-prefix complementary release branches can require strictly more side state than any realized-branch oracle code;
2. refining the decoder-visible branch label (without changing the lawful targets) can only remove confusability edges, never add them, but may still leave a complete graph when different states disagree under some shared refined label;
3. a release implementation that crosses a hard selector guard can violate a same-branch Jacobian bound even when every branch derivative is contractive;
4. an exact side code smaller than `ceil(log2 chi(G_R19))` on the declared finite object would falsify Theorem 1.

Strong same-information controls are: direct storage of the complete released-value signature; full pre-write state retention; no-write/fixed protection; R08's direct release decision using the same evidence; R18's prefix-robust quotient/direct ledger; a bank of mode-matched set-valued observers with residual elimination; and common/path-complete Lyapunov or bisimulation certificates over the same transition relation.

Existing bAbI, LAMBADA, RULER, BABILong and LongMemEval scorers can measure downstream answer/token outcomes of a future implementation. They do not natively expose the finite reachable recurrent alphabet, destructive-state fiber `W^{-1}(z)`, lawful branch relation, visible label, exact released target, confusability graph or paired same-state release counterfactual. SEAL and temporal editing endpoints likewise do not provide this mechanism label. Internal graph construction would be a derived diagnostic, not native evidence. The central mechanism therefore remains a measurement gap.

## 8. Closest work and disposition

Theorem 1 is a direct specialization of classical zero-error function computation with decoder side information: characteristic/confusion graphs connect source symbols that share decoder side information but require different function values, and one-shot fixed-length coding is graph coloring. Hidden-mode set-valued observers already maintain a bank of compatible mode/state sets, eliminate modes by residuals, and fuse the survivors. Approximate bisimulation and symbolic-model work already treats nondeterministic switched transition relations and finite abstractions. R18 v2 already gives the global fiber/right-congruence requirement and the prefix-robust linear quotient; R19 v1 already gives the realized-branch PSD jump obstruction.

The retained value is therefore a precise debugging bridge: a state-dependent Delta release is not repaired by differentiating a chosen branch; under an explicit finite-precision model its minimum one-shot exact pre-release side state is the chromatic number of the induced release-confusability graph. This is mathematically correct and more causal than v1, but it is not a new coding theorem, switched-system framework or updater. No Delta-specific matched-total-cost advantage or native mechanism object has been established.

**Decision:** park R19 after substantive attempt 2 of 3 as a conditional theorem/debug control, with `candidate_delta=0` and empirical effect unknown. Reopen attempt 3 only if a structured Delta transition family yields a tractable code strictly cheaper than the direct signature/full-state/R18 ledger at matched precision and compute, together with a native mechanism-identifying measurement object.
