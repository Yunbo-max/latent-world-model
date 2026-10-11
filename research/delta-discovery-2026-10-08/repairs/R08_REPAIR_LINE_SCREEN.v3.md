# R08 v3 repair-line screen — unknown-channel information envelope

Status: **selected bounded repair; substantive attempt 3/3**  
Preserved parents: `R08_TEMPORAL_VALIDITY_RELEASE.v1.md` and `R08_ACTION_DEPENDENT_INFORMATION_VALUE.v2.md` remain unchanged.

## Earliest open premise

R08 v2 exactly computes the information value of a *known* action-specific observation channel. The deployment record, however, does not supply the counterfactual channel for an action that was not taken. The unresolved premise is therefore not another algebra error: it is whether a prefix-only controller can make a justified keep/release choice when `g_R` or `g_K` is unidentified.

## Screened patches

| Patch | Consequence | Decision |
|---|---|---|
| Learn `g_R,g_K` or `Q_R-Q_K` from the same prefix without randomized support | No identification gain: two worlds can agree on all on-policy records and reverse the untried action | Reject as an oracle relabeling |
| Use entropy, posterior variance, or validity confidence as a generic information bonus | R08 v2 already proves that equal first two posterior moments can have different action value | Reject |
| Build a multistep Delta sufficient state | Requires recursive quotient/right-congruence closure already isolated by R18 and generic POMDP state compression | Retain only as a separate known control; do not recount |
| Bound every unobserved channel by the uninformative and perfectly revealing experiments | Produces a sharp, prefix-valid interval for each information value and hence a sharp robust keep/release/abstain certificate | **Select** |

The selected patch changes the target from point estimation of an unavailable counterfactual channel to sharp partial identification under the declared information set. It does not delete v1/v2 counterexamples, does not infer future validity from model self-assessment, and does not claim a new updater.

## Bounded decision

Attempt 3 derives the exact channel-free envelope and a same-observed-record two-world nonidentifiability result. It is useful because it says precisely when the available prefix is already decisive and when further evidence or randomization is logically required. Expected-value-of-information, Blackwell/garbling, partial-identification policy learning, robust decisions and R05 cover the mechanism family. Therefore the lineage is exhausted and parked after final-byte review, with candidate delta zero and empirical effect unknown.
