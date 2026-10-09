# Independent review — NOGO-UNITARY-DILATION

- reviewer: `/root/dilation_nearest_work`
- reviewed artifact: `research/delta-discovery-2026-10-08/rejected/NOGO_UNITARY_DILATION.md`
- exact artifact SHA256: `32cf30ee7ba075237d8e3797fff0b5664d8b05ed6d5debffdcbe8cb1bc583e02`
- verdict: **VERIFIED_NO_GO_CONTROL**

The rank-one defect formula and compressed one-row Halmos completion are correct for \(0\le\beta\le2\).  Reusing that auxiliary gives an involution, so the visible key component returns after two identical erase steps instead of following \((1-\beta)^2\).  The stronger block argument is also valid: visible evolution independent of arbitrary auxiliary contents forces the feedback block to zero, after which orthogonality forces the visible operator itself to be unitary.

The all-horizon statement correctly specializes the classical Sz.-Nagy boundary: a strict finite-dimensional contraction cannot have a finite-dimensional unitary power dilation for every power.  Fresh defect channels give a finite-horizon realization only by growing state with the horizon.  The full affine Delta write must remain external forcing; the homogeneous translation is not orthogonal.

The construction and boundary collide directly with Halmos/Julia and finite \(N\)-dilation theory, with a recurrent-reservoir implementation already available in Fong, Li and Tino.  DeltaProduct covers Householder/orthogonal transition products, while reversible RNNs, HOLA and explicit slot memories expose the actual storage cost.  The artifact therefore correctly rejects the route as a method and retains only the no-go/control.

No files were edited by the reviewer, and no project code, tests, models, benchmarks, training, inference, scorer, download or GPU work was executed.
