# Independent review — noisy-key identification/prediction control

Reviewers: `/root/noisy_key_math` and `/root/noisy_key_sources`. Both read the final local bytes and independently computed SHA256. Read-only mathematical/source review; neither edited nor executed project/author code.

- Mathematical artifact: `rejected/NOISY_KEY_IDENTIFICATION_PREDICTION_CONTROL.md`, SHA256 `d39cafd719b4e71d2190c1f46e0902662572bb1c963ad9ac71645990fdc09842`.
- Source artifact: `sources/NOISY_KEY_EIV_SOURCE_AUDIT.md`, SHA256 `3442ee9a09db9c43549f30ca0128e262533e74ce2a914a12a756afd8aa22709c`; independently read/hash-bound by the source reviewer. Mathematical reviewer does not certify all separate code/source receipts.
- Initial mathematical draft SHA256 `d0250b1a31d525ffd7732f85a6eaa23489dc47ffa7de50e646caaaecee056f51` was accepted subject to two repairs; it was not promoted as final.

## Mathematical reasoning and corrections

`/root/noisy_key_math` independently checked dimensions and chronological order, iid mean drift, the homogeneous second-moment operator, forced cross terms, BC and IV fourth moments, risk completion, scalar identification continuum and unequal-view covariance identity. The final mean-square examples follow from expanding the squared scalar multiplier, not from the published BC-LMS step-size display. Constant-step forced variance is correctly separated from mean recovery.

Two findings were corrected and the final bytes reread: covariance cross terms require the coefficient eta; cross-view dependence alone does not invalidate a second-moment identity, whereas nonzero relevant error cross moments can. Final verdict: **accept conditional mathematical control**. No remaining demonstrated mathematical error in the reviewed scope; not a global neural-network theorem or evidence of observed project failure.

## Source and consequence reasoning

`/root/noisy_key_sources` independently checked the BC-LMS update collision, general IV exclusion/rank versus stability, noisy-query Bayes readout orientation, nonnegative risk difference and extra observation/covariance costs. It found no basis for original-method or native-text improvement admission.

The reviewer independently fetched/read `NVlabs/noise2noise@7355519e7bfc49e0606cca8867748e736431244b` README, dataset, train and validation files; all four Git blobs matched the audit. It confirmed two noise calls, noisy/clean target choice and loaded-image PSNR denominator. This is an actual pinned static source check, not execution or benchmark qualification.

Remaining: real instrument/noise/latent-query input for the current text interface, native measurement and assets, complete environment/helper audit and all actual execution. IVAP 1998 and Bradtke–Barto 1996 incomplete reads remain incomplete; the decisive classification does not depend on them. BC paper sign discrepancies are cautions, not a claimed formal erratum.

**Joint disposition:** known EIV/BC-LMS/IV statistical-objective control, no D-number, no active/admitted/selected count. Reopening needs an actual observation/query contract and a substantive contribution beyond existing methods, with the appropriate theory/target/representation obligations rather than a mandatory new module.
