# Independent final-byte source and distinctness review — R09 v3

Reviewer identity: `/root/r09_v3_final_source_review`  
Math artifact SHA256: `fa1c525afdf34646c750373eb45ce2e62c33881d846ea0cab63331744cf01415`  
Source audit SHA256: `a47085ed8245ededf337370fdb9ed07e9a478bb460ed38e932b60fc7f83c7699`  
Verdict: **PASS for bounded source support and collision disposition**

## Preserved correction history

The first source review failed source SHA256 `c53203f5e89af417131ad1ac2e90639e9070c722eba176e8cb949b58f5902e77` because it misstated the title/authors and equation split of arXiv:1409.1444v2 and the title/authors of arXiv:1103.1343. The integration writer corrected those metadata and locators; the final source bytes above were independently reread and rehashed.

## Final reasoning

- Bastug, Petreczky, Wisniewski and Leth, arXiv:1409.1444v2, Definition 8/equation (12), equation (13), Lemma 4 and Algorithm 2 directly support the constrained-language observable-space/quotient collision.
- Petreczky, Bako and van Schuppen, arXiv:1103.1343, supports switched realization/observability minimality; Pontes Duff, Grundel and Benner supports the Gramian-range/global-projection counterpart.
- Li--White and Schulze--Unger support the low-rank Lyapunov/switching controls.
- The DeltaProduct author repository pin `d62241a81d07aa32b1b65e7d17377f6a7cd0a5d8` and named interfaces are fixed; unavailable immutable code for the Bastug paper is not invented.
- Bounded-absence wording is non-priority evidence. Internal R18 is the decisive dual collision, with R16, R11, R20 and R09 v2 as additional controls.

The surviving Delta witness is a useful specialized debugging theorem, not a new updater or Gramian algorithm. Candidate delta `0`, attempt 3/3 park, and empirical-unknown status are supported.
