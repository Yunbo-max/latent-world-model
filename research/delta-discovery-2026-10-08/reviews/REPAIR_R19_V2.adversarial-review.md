# R19 v2 independent adversarial review

- Reviewer identity: `/root/r19_v2_adversarial`
- Assignment: search for counterexamples, hidden future information, dimensional errors, cost omissions, and overclaims in the final artifact.
- Reviewed SHA256: `0d771029d39677e8077b7c23d761c90b2c9ffaecf03b81781a078ec8561ed105`
- Verdict: **PASS; no blocking correction**

## Attacks and resolution

The initial bytes failed three attacks: same-state hidden-branch ambiguity, failure to subtract information already present in `W(x)` from the additional linear code, and an unjustified squared-diameter energy claim. The final bytes resolve all three with condition (F)/infeasibility, the quotient rank `rank([A;B_1;...;B_M])-rank(A)`, and the scoped `Delta_0^2/4` point-loss bound.

The K4 example now declares `B(x)={1,2}` for every state and satisfies (F) because the target-relevant branches have different visible labels. The label monotonicity claim is restricted to refinement with fixed lawful targets. The code is chosen before destructive writing; any learned branch set has only conditional coverage, so no future oracle has been reintroduced. The all-path statement handles noncommuting reset/Jacobian or admissible saltation products and defines the infinite-family object through the joint row span.

The artifact separates runtime bits from codebook, decoder, precision, reliability, construction and update costs, and requires rederivation on the augmented recurrent state. The parked/no-candidate conclusion survives every attack.
