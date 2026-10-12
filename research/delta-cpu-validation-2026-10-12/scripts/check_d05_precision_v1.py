"""D05 development diagnostics; constructed inputs, not a native benchmark."""
import argparse
import itertools
import json
import time
from pathlib import Path

import numpy as np


SOURCE = 'source_snapshots/cards/D05.json'


def run():
    rng = np.random.default_rng(12012)
    checks = []

    def add(cid, metrics, ok, interpretation):
        checks.append(dict(id=cid, lineage='D05', scope='constructed development diagnostic',
                           status='passed' if ok else 'failed', metrics=metrics,
                           source_refs=[SOURCE], interpretation=interpretation))

    # Direct chronological recurrence versus genuinely moving coordinates.
    s = np.array([[.2, -.3], [.4, .1], [-.2, .5]])
    z = s.copy()
    previous_t = np.eye(3)
    correct_errors, wrong_errors = [], []
    for j in range(4):
        k = rng.normal(size=3)
        k /= np.linalg.norm(k)
        d = np.diag([.7, .8, .9])
        f = (np.eye(3) - .2 * np.outer(k, k)) @ d
        v = rng.normal(size=2)
        t = np.eye(3) + .15 * rng.normal(size=(3, 3))
        direct = f @ s + .2 * np.outer(k, v)
        moving = np.linalg.solve(t, f @ previous_t @ z + .2 * np.outer(k, v))
        wrong = np.linalg.solve(t, f @ t @ z + .2 * np.outer(k, v))
        correct_errors.append(float(np.linalg.norm(t @ moving - direct)))
        wrong_errors.append(float(np.linalg.norm(t @ wrong - direct)))
        q = rng.normal(size=3)
        correct_errors.append(float(np.linalg.norm((t.T @ q) @ moving - q @ direct)))
        s, z, previous_t = direct, moving, t
    add('D05-v2.moving-coordinate-order',
        {'max_correct_error': max(correct_errors), 'max_wrong_previous_basis_error': max(wrong_errors)},
        max(correct_errors) < 1e-12 and max(wrong_errors) > 1e-3,
        'Changing bases requires T_previous in the transition and T_current.T in the query; a naive basis substitution fails.')

    # Independent exhaustive integer optimum versus separable marginal allocator.
    lam = np.array([16., 1., 0.])
    floor, budget = 1, 9
    feasible = [(b, float(np.sum(lam * 4. ** -np.array(b))))
                for b in itertools.product(range(floor, budget + 1), repeat=3)
                if sum(b) == budget]
    optimum = min(v for _, v in feasible)
    bits = np.full(3, floor, dtype=int)
    for _ in range(budget - 3 * floor):
        gain = .75 * lam * 4. ** -bits
        bits[int(np.argmax(gain))] += 1
    greedy = float(np.sum(lam * 4. ** -bits))
    add('D05-v2.integer-allocation-floor-zero-spectrum',
        {'greedy_bits': bits.tolist(), 'greedy_risk': greedy, 'exhaustive_risk': optimum, 'feasible_allocations': len(feasible)},
        abs(greedy - optimum) < 1e-14 and bits[2] == floor,
        'Discrete marginal allocation agrees with exhaustive search for this declared equal-range spectrum including a zero direction; not a mixed-bit kernel measurement.')

    # Direct subtractive dither quantizer, not simulated Gaussian injection.
    n = 8192
    bits = np.array([5, 3])
    step = 2. ** -bits
    x = rng.uniform(-.2, .2, size=(2, n))
    dither = rng.uniform(-.5, .5, size=(2, n)) * step[:, None]
    indices = np.rint((x + dither) / step[:, None])
    reconstructed = indices * step[:, None] - dither
    error = reconstructed - x
    no_overload = bool(np.all(indices >= -(2. ** (bits - 1))[:, None]) and
                       np.all(indices <= (2. ** (bits - 1) - 1)[:, None]))
    predicted_variance = step ** 2 / 12
    mean_se = step / np.sqrt(12 * n)
    variance_se = step ** 2 / np.sqrt(180 * n)
    mean_z = np.max(np.abs(error.mean(axis=1)) / mean_se)
    variance_z = np.max(np.abs((error ** 2).mean(axis=1) - predicted_variance) / variance_se)
    add('D05-v2.subtractive-dither-no-overload',
        {'n_per_row': n, 'steps': step.tolist(), 'predicted_variance': predicted_variance.tolist(),
         'observed_second_moment': (error ** 2).mean(axis=1).tolist(), 'max_mean_standard_errors': float(mean_z),
         'max_second_moment_standard_errors': float(variance_z), 'no_overload': no_overload},
        no_overload and mean_z < 6 and variance_z < 6,
        'Implemented subtractive uniform dither matches uniform-noise moments in a no-overload interior; six-SE development diagnostic, not a general coverage claim.')
    lam = np.array([16., 1.])
    samples = (lam[:, None] * error ** 2).sum(axis=0)
    predicted = float(lam @ predicted_variance)
    risk_se = float(np.sqrt(np.sum(lam ** 2 * step ** 4 / 180) / n))
    risk_z = abs(float(samples.mean()) - predicted) / risk_se
    add('D05-v2.one-injection-quadratic-risk',
        {'predicted_risk': predicted, 'observed_mean_risk': float(samples.mean()), 'standard_error_under_declared_model': risk_se,
         'absolute_standard_errors': risk_z}, risk_z < 6,
        'Single-injection expected output risk matches the direct quantizer under stated equal-range independent-dither conditions; recurrent risk is a different object.')

    # Exactly reproduce the gain and its reversal after unobserved metric drift.
    b = np.array([5, 3]); uniform = np.array([4, 4])
    normal = np.array([16., 1.]); swapped = normal[::-1]
    risks = {name: float(l @ (4. ** -bb)) for name, l, bb in [
        ('calibrated', normal, b), ('uniform', normal, uniform), ('stale_after_swap', swapped, b), ('uniform_after_swap', swapped, uniform)]}
    add('D05-v2.metric-drift-reversal', risks,
        abs(risks['calibrated'] - 8 / 256) < 1e-14 and risks['calibrated'] < risks['uniform']
        and risks['stale_after_swap'] > risks['uniform_after_swap'],
        'The causal predictor cannot use the deployed future swap; this is a drift falsifier, not a deployable oracle comparison.')

    # Repeated noise with equal single-step marginals but opposite joint laws.
    h = 4; eps = .125
    independent_signs = np.array(list(itertools.product([-1., 1.], repeat=h)))
    independent_outputs = np.cumsum(eps * independent_signs, axis=1)[:, -1]
    correlated_signs = np.array([[-1.] * h, [1.] * h])
    correlated_outputs = np.cumsum(eps * correlated_signs, axis=1)[:, -1]
    independent_risk = float(np.mean(independent_outputs ** 2))
    correlated_risk = float(np.mean(correlated_outputs ** 2))
    add('D05-v2.recurrent-cross-injection-counterexample',
        {'horizon': h, 'independent_risk': independent_risk, 'correlated_risk': correlated_risk,
         'sum_of_single_injection_risks': h * eps ** 2, 'correlated_to_independent_ratio': correlated_risk / independent_risk},
        abs(independent_risk - h * eps ** 2) < 1e-14 and abs(correlated_risk - h ** 2 * eps ** 2) < 1e-14,
        'Exhaustive two joint noise laws have identical one-step marginals but distinct final risks; the local risk cannot imply a repeated-injection certificate. This is a generic correlated-noise boundary, not subtractive-dither failure.')

    # FP32 cancellation in a legal invertible but badly conditioned basis.
    state = np.array([[1., 1.], [1., 2.]])
    precision = []
    for shear in [0., 1e4, 1e8]:
        t = np.array([[1., shear], [0., 1.]])
        exact_z = np.array([[1. - shear, 1. - 2 * shear], [1., 2.]])
        out64 = t @ exact_z
        out32 = t.astype(np.float32) @ exact_z.astype(np.float32)
        precision.append({'shear': shear, 'condition_number': float(np.linalg.cond(t)),
                          'fp64_error': float(np.linalg.norm(out64 - state)),
                          'fp32_error': float(np.linalg.norm(out32.astype(float) - state))})
    add('D05-v2.fp32-basis-cancellation', {'cases': precision, 'expected_fp32_failure_observed': precision[-1]['fp32_error'] > .5},
        max(c['fp64_error'] for c in precision) < 1e-12 and precision[0]['fp32_error'] == 0
        and precision[-1]['fp32_error'] > .5,
        'Real-arithmetic coordinate equivalence fails numerically for this ill-conditioned FP32 basis; the diagnostic passes by exposing the predicted limitation, not by asserting FP32 equivalence.')
    return checks


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--output', required=True); args = ap.parse_args()
    start = time.perf_counter(); checks = run()
    result = dict(suite='D05-precision-v1', seed=12012, data_kind='constructed mathematical diagnostic',
                  checks=checks, elapsed_seconds=time.perf_counter() - start,
                  limitations=['No payload packing, basis-refresh cost or native LM score measured.',
                               'Future spectrum is diagnostic/reference information, not available deployment evidence.',
                               'These conditions were selected after inspecting the archived theorem; development evidence only.'])
    Path(args.output).write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps({'checks': len(checks), 'failed': sum(c['status'] == 'failed' for c in checks)}))
    raise SystemExit(any(c['status'] == 'failed' for c in checks))
