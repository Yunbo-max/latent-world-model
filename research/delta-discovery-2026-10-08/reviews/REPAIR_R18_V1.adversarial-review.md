# R18 v1 independent final-byte adversarial review

- Reviewer: `/root/r18_adversarial`
- Assignment: search for hidden future oracles, local-to-global overclaims, wrong kernels, omitted recurrent state, invalid counterexamples, non-smooth/free-running gaps, and hidden resource costs
- Reviewed artifact SHA256: `c3b32f912637b5ba3f1e6978f0c981d517a3d561736e246a7b2d392011d8f559`
- Verdict: **PASS for a parked conditional theorem/control; no candidate admission**

The reviewer first found and forced correction of three overclaims: a singular PSD weight cannot certify an unweighted output kernel; deployed and reference nonlinear branches require their own downstream derivatives; and a side-state copy cannot be called globally injective. The final bytes correct all three. They also keep the protected reference independent of the destructive update, use the complete current-update kernel, preserve singular-`D` and cross-block cases, and distinguish decodability from direct deployed equality.

No blocking error remains. The artifact explicitly limits nonlinear Jacobians to first order, retains global fiber/congruence obligations, exposes non-smooth routing and free-running boundaries, and charges side state, precision, suffix generation, derivative passes, checkpoint/recompute, quotient bases, and rank coverage. Missing prefix-causal quotient estimation, global nonlinear certification, native internal scoring, originality, and empirical evidence justify park/no-candidate status.
