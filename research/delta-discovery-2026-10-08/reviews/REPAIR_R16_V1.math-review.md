# Independent mathematical review — R16 v1

- Reviewer: /root/r16_math
- Artifact: repairs/R16_NONCOMMUTING_JOINT_FLOW.v1.md
- Artifact SHA256: 737f49385a232bdf9261c0fe7bec10955d0856ac7315e71ea226d7c78895d7d6
- Verdict: PASS_CONDITIONAL
- Execution: exact-byte static mathematical review only; no project code, tests, model execution, training, inference, scoring, benchmark dispatch, or data/model download.

The final bytes correctly specify the controlled endpoint ODE, condition the \(u_\tau\sim1/\tau\) statement on nonzero initial residual, and compare the leakage witness against the matched correction-subflow source. Dimensions, variation of constants, endpoint normalization, inverse-metric optimization equivalence, singular exact-write factor, and both limiting write directions are correct.

The Krylov-subspace rank bound is valid for symmetric \(\Lambda\). The two-dimensional determinant coefficient

\[
-\frac{a^2c^2}{12}\tau^4
\]

and leakage coefficient \(\tau^2/4\) were independently rechecked. The ordered-split expansions have the correct signs:

\[
E_\tau-CD=\frac{\tau^2}{2}[\Lambda,kk^\top]+O(\tau^3),
\qquad
F_\tau-F_K=-\frac{\tau^2}{2}\Lambda k+O(\tau^3).
\]

The cost discussion now properly describes generic explicit dense formation/application and explicitly avoids claiming a universal lower bound against specialized structured exact-action methods.

The result is useful as a conditional Krylov-rank and affine-source boundary. It does not establish a distinct updater: the endpoint repair remains normalized inverse-metric/oblique Delta, and empirical benefit is unknown. Park after attempt 1 and add zero active, scientifically admitted, or selected candidates.
