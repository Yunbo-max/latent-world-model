#!/usr/bin/env python3
"""Small deterministic constructed diagnostics for the pinned Delta source packet.

These are numerical audits of conditional identities, optimizations, and stated
failure boundaries. They are neither public benchmark results nor mathematical
proofs. No source data, model, or deployment certificate is inferred by this file.
Run serially on a CPU: python check_statistics.py --output result.json --seed 17
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import time


BASE = Path(__file__).resolve().parents[1]
SOURCES = {
    "R02": "source_snapshots/repairs/R02_APPROXIMATE_CAUSAL_DYNAMIC_QUOTIENT.v3.md",
    "R03": "source_snapshots/repairs/R03_WASSERSTEIN_FREE_RUNNING_SAFETY.v3.md",
    "R05": "source_snapshots/repairs/R05_PREFIX_CONDITIONAL_PARTIAL_ID.v4.md",
    "R08": "source_snapshots/repairs/R08_SHARP_CHANNEL_FREE_RELEASE.v3.md",
    "R14": "source_snapshots/repairs/R14_OBSERVABLE_EQUIVALENCE_CLOSURE.v3.md",
    "R15": "source_snapshots/repairs/R15_FINITE_JET_CERTIFICATE_BOUNDARY.v3.md",
    "R17": "source_snapshots/repairs/R17_RESIDUAL_SCALED_SPECTRAL_CERTIFICATE.v3.md",
    "R19": "source_snapshots/repairs/R19_FINITE_FIELD_SYNDROME_RELEASE.v3.md",
    "query_weighted_rate_distortion": "source_snapshots/STEP2_QUERY_WEIGHTED_RATE_DISTORTION_2026-10-12.md",
    "compound_query_hedge": "source_snapshots/STEP2_COMPOUND_QUERY_HEDGE_2026-10-12.md",
    "active_evidence": "source_snapshots/STEP2_ACTIVE_EVIDENCE_ACQUISITION_2026-10-12.md",
}
ATOL = 2e-10
RTOL = 2e-9
OPT_TOL = 2e-6


def close(a, b, atol=ATOL, rtol=RTOL):
    return bool(np.allclose(a, b, atol=atol, rtol=rtol))


def lp(c, *, a_eq=None, b_eq=None, a_ub=None, b_ub=None, bounds=None):
    result = optimize.linprog(c, A_eq=a_eq, b_eq=b_eq, A_ub=a_ub,
                             b_ub=b_ub, bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError("reference linear program failed: " + result.message)
    return result


def slsqp(fun, x0, bounds, constraints):
    result = optimize.minimize(fun, np.asarray(x0, dtype=float), method="SLSQP",
                               bounds=bounds, constraints=constraints,
                               options={"ftol": 1e-12, "maxiter": 2000})
    if not result.success:
        raise RuntimeError("reference convex optimization failed: " + result.message)
    return result


def psd_sqrt(a):
    vals, vecs = np.linalg.eigh(a)
    return (vecs * np.sqrt(np.maximum(vals, 0.0))) @ vecs.T


def waterfill(weights, rate):
    """Bisection for half-log rate; zero weights carry no allocated rate."""
    w = np.asarray(weights, dtype=float)
    if rate == 0 or not np.any(w > 0):
        return float(np.max(w, initial=0.0)), np.zeros_like(w)
    positive = w > 0
    lo, hi = -1000.0, float(np.log2(w[positive].max()))
    for _ in range(180):
        mid = (lo + hi) / 2
        used = 0.5 * np.maximum(np.log2(w[positive]) - mid, 0).sum()
        if used > rate:
            lo = mid
        else:
            hi = mid
    level = 2.0 ** ((lo + hi) / 2)
    allocations = np.zeros_like(w)
    allocations[positive] = 0.5 * np.maximum(np.log2(w[positive] / level), 0)
    return level, allocations


def w1(p, q, locations):
    n = len(p)
    cost = np.abs(locations[:, None] - locations[None, :]).ravel()
    rows = []
    for i in range(n):
        row = np.zeros((n, n)); row[i, :] = 1; rows.append(row.ravel())
    for j in range(n):
        row = np.zeros((n, n)); row[:, j] = 1; rows.append(row.ravel())
    return float(lp(cost, a_eq=np.array(rows), b_eq=np.r_[p, q],
                    bounds=(0, None)).fun)


def polynomial_extrema(poly, radius):
    """All real stationary points and endpoints, not a sampled optimizer."""
    points = [-radius, radius]
    for root in poly.deriv().roots():
        if abs(root.imag) < 1e-8 and -radius <= root.real <= radius:
            points.append(float(root.real))
    values = np.array([poly(x) for x in points])
    return float(values.min()), float(values.max()), float(points[int(values.argmin())])


def gf_rank(matrix, prime):
    a = np.array(matrix, dtype=int, copy=True) % prime
    row = 0
    for col in range(a.shape[1]):
        choices = np.flatnonzero(a[row:, col])
        if len(choices) == 0:
            continue
        pivot = row + int(choices[0])
        a[[row, pivot]] = a[[pivot, row]]
        a[row] = a[row] * pow(int(a[row, col]), -1, prime) % prime
        for other in range(a.shape[0]):
            if other != row:
                a[other] = (a[other] - a[other, col] * a[row]) % prime
        row += 1
        if row == a.shape[0]:
            break
    return row


def exact_chromatic(adjacency):
    """Actual finite graph coloring search, with color permutation symmetry removed."""
    n = len(adjacency)
    order = sorted(range(n), key=lambda i: -int(adjacency[i].sum()))
    colors = [-1] * n

    def feasible(k, depth=0, used=0):
        if depth == n:
            return True
        vertex = order[depth]
        banned = {colors[j] for j in range(n) if adjacency[vertex, j] and colors[j] >= 0}
        for color in range(min(k, used + 1)):
            if color not in banned:
                colors[vertex] = color
                if feasible(k, depth + 1, max(used, color + 1)):
                    return True
        colors[vertex] = -1
        return False

    for k in range(1, n + 1):
        colors[:] = [-1] * n
        if feasible(k):
            return k, colors.copy()
    raise RuntimeError("finite coloring search found no coloring")


def r02_aipw(rng):
    history_mass = np.array([0.5, 0.5])
    propensity = np.array([0.25, 0.75])
    outcome = np.array([0.0, 1.0])
    coarse_p = float(history_mass @ propensity)
    target = float(history_mass @ outcome)
    expectations = []
    for nuisance in [0.0, 0.17, 0.9, 1.0]:
        expected = 0.0
        # Enumerate the joint observational Bernoulli experiment, including A=0.
        for h, action, y in itertools.product(range(2), range(2), range(2)):
            action_prob = propensity[h] if action else 1 - propensity[h]
            y_mean = outcome[h] if action else 0.0
            mass = history_mass[h] * action_prob * (y_mean if y else 1 - y_mean)
            psi = nuisance + action * (y - nuisance) / coarse_p
            expected += mass * psi
        expectations.append(expected)
    covariance = float(history_mass @ ((propensity - coarse_p) * (outcome - target)))
    sigma_mu = math.sqrt(float(history_mass @ (propensity - coarse_p) ** 2))
    sigma_m = math.sqrt(float(history_mass @ (outcome - target) ** 2))
    bound = sigma_mu * sigma_m / coarse_p
    # The second hidden world has the same complete quotient-level binary (A,Y) law.
    other_outcome = np.array([1.0, 2 / 3])
    joint1 = np.array([coarse_p - history_mass @ (propensity * outcome),
                       history_mass @ (propensity * outcome)])
    joint2 = np.array([coarse_p - history_mass @ (propensity * other_outcome),
                       history_mass @ (propensity * other_outcome)])
    ok = close(np.array(expectations) - target, covariance / coarse_p)
    ok &= close(bound, 0.25) and close(expectations[0] - target, bound)
    ok &= close(joint1, joint2) and abs(history_mass @ other_outcome - target) > 0.3
    return ok, {"enumerated_aipw_expectations": expectations, "target_mean": target,
                "bias": expectations[0] - target, "sharp_cs_bound": bound,
                "observational_joint_law_max_gap": float(abs(joint1 - joint2).max()),
                "second_world_target_mean": float(history_mass @ other_outcome)}, \
        "Sharp covariance bias is reproduced; equal quotient observational laws leave the target mean unidentified."


def r02_value(rng):
    horizon, states, actions = 3, 4, 2
    quotient = np.array([0, 0, 1, 1])
    gamma = 0.8
    rewards = rng.uniform(0, 1, (horizon, states, actions))
    transitions = rng.dirichlet(np.ones(states), (horizon, states, actions))
    policy = np.array([[0.25, 0.75], [0.65, 0.35]])
    abstract_r = np.zeros((horizon, 2, actions))
    abstract_p = np.zeros((horizon, 2, actions, 2))
    push = np.stack([transitions[..., quotient == q].sum(axis=-1) for q in range(2)], axis=-1)
    for q in range(2):
        abstract_r[:, q] = rewards[:, quotient == q].mean(axis=1)
        abstract_p[:, q] = push[:, quotient == q].mean(axis=1)
    eps_r = np.array([abs(rewards[t] - abstract_r[t, quotient]).max() for t in range(horizon)])
    eps_p = np.array([0.5 * abs(push[t] - abstract_p[t, quotient]).sum(axis=-1).max()
                      for t in range(horizon)])
    values = np.zeros((horizon + 1, states)); abstract_v = np.zeros((horizon + 1, 2))
    for t in range(horizon - 1, -1, -1):
        values[t] = np.sum(policy[quotient] * (rewards[t] + gamma * (transitions[t] @ values[t + 1])), axis=1)
        abstract_v[t] = np.sum(policy * (abstract_r[t] + gamma * (abstract_p[t] @ abstract_v[t + 1])), axis=1)

    def enumerate_paths(t, h):
        if t == horizon:
            return 0.0
        total = 0.0
        for a, following in itertools.product(range(actions), range(states)):
            total += policy[quotient[h], a] * transitions[t, h, a, following] * \
                (rewards[t, h, a] + gamma * enumerate_paths(t + 1, following))
        return total

    enumeration = np.array([enumerate_paths(0, h) for h in range(states)])
    M = np.array([sum(gamma ** j for j in range(horizon - t)) for t in range(horizon + 1)])
    errors = abs(values - abstract_v[:, quotient]).max(axis=1)
    bounds = np.zeros(horizon + 1)
    for t in range(horizon - 1, -1, -1):
        bounds[t] = eps_r[t] + gamma * bounds[t + 1] + gamma * M[t + 1] * eps_p[t]
    expanded = sum(gamma ** t * eps_r[t] for t in range(horizon)) + \
        sum(gamma ** (t + 1) * M[t + 1] * eps_p[t] for t in range(horizon - 1))
    ok = close(enumeration, values[0]) and close(expanded, bounds[0])
    ok &= bool(np.all(errors <= bounds + ATOL))
    return ok, {"horizon": horizon, "full_path_count_per_initial_state": (actions * states) ** horizon,
                "bellman_vs_path_max_gap": float(abs(enumeration - values[0]).max()),
                "uniform_reward_defects": eps_r.tolist(), "conventional_tv_defects": eps_p.tolist(),
                "value_errors": errors.tolist(), "ordered_bound": bounds.tolist()}, \
        "Independent finite-path enumeration supports the target-policy abstraction bound under uniform reachable defects."


def r02_boundaries(rng):
    delta = 0.01
    behavior_average = 2 * delta * (1 - delta)
    target_error = 1 - delta
    pointwise_mu = np.array([0.0, 1.0])
    coarse_overlap = float(pointwise_mu.mean())
    # Equal right quotients, a hidden-state gate, and identical retained side state.
    S0, S1 = np.array([[1.0, 0.0]]), np.array([[1.0, 2.0]])
    W = np.array([[1.0], [0.0]])
    k, v = np.array([1.0]), np.array([3.0, 0.0])
    beta0, beta1 = 0.2, 0.8
    f0 = (S0 + beta0 * np.outer(k, v - S0.T @ k)) @ W
    f1 = (S1 + beta1 * np.outer(k, v - S1.T @ k)) @ W
    ok = coarse_overlap > 0 and pointwise_mu[0] == 0
    ok &= target_error > 40 * behavior_average and close(S0 @ W, S1 @ W)
    ok &= abs(float((f1 - f0).item())) > 1
    return ok, {"coarse_propensity": coarse_overlap, "missing_pointwise_propensity": 0.0,
                "behavior_average_defect": behavior_average, "target_value_error": target_error,
                "same_quotient_gate_leakage": float(abs(f1 - f0).item())}, \
        "Expected boundary: coarse overlap, behavior-average calibration, and equal SW alone do not satisfy the stronger certificate assumptions."


def r03_wasserstein(rng):
    locations = np.array([0.0, 1.0, 2.5])
    reference = np.array([[0.8, 0.2, 0.0], [0.5, 0.4, 0.1], [0.2, 0.5, 0.3]])
    action = 0.85 * reference + 0.15 * np.array([[0, 0, 1.0]] * 3)
    kappa = max(w1(reference[i], reference[j], locations) / abs(locations[i] - locations[j])
                for i in range(3) for j in range(i))
    epsilon = max(w1(action[i], reference[i], locations) for i in range(3))
    p, q = np.array([0, 1.0, 0]), np.array([1.0, 0, 0])
    actual, envelope = [w1(p, q, locations)], [w1(p, q, locations)]
    for _ in range(5):
        p, q = p @ action, q @ reference
        actual.append(w1(p, q, locations))
        envelope.append(epsilon + kappa * envelope[-1])
    product = [kappa ** h * actual[0] + sum(kappa ** (h - j - 1) * epsilon for j in range(h))
               for h in range(6)]
    loss = np.array([0.0, 0.4, 1.0])
    L = max(abs(loss[i] - loss[j]) / abs(locations[i] - locations[j]) for i in range(3) for j in range(i))
    risk_gap = float(p @ loss - q @ loss)
    # A common metric rescaling must compensate in the loss Lipschitz constant.
    scaled_delta = w1(p, q, 0.001 * locations)
    ok = bool(np.all(np.array(actual) <= np.array(envelope) + ATOL))
    ok &= close(envelope, product) and abs(risk_gap) <= L * actual[-1] + ATOL
    ok &= close((L / 0.001) * scaled_delta, L * actual[-1])
    return ok, {"transport_lp_kappa": kappa, "transport_lp_epsilon": epsilon,
                "actual_w1": actual, "envelope": envelope, "protected_loss_gap": risk_gap,
                "loss_lipschitz_bound": L * actual[-1], "metric_rescaling_product_gap":
                abs((L / 0.001) * scaled_delta - L * actual[-1])}, \
        "Full finite Markov laws and independent transport LPs support R03 v3; the loss-compatible product is invariant to metric rescaling."


def r03_forcing_and_feasibility(rng):
    # Both kernels forget their input: kappa=0; their discrepancy persists.
    baseline = np.array([[1.0, 0], [1.0, 0]])
    forced = np.array([[0.8, 0.2], [0.8, 0.2]])
    p = q = np.array([1.0, 0])
    distances = []
    for _ in range(6):
        p, q = p @ forced, q @ baseline
        distances.append(abs(p[1] - q[1]))
    costs = np.array([0.0, 0.4, 1.7]); floor = 0.12
    threshold = floor * costs.sum() + (1 - len(costs) * floor) * costs.min()
    reference_min = lp(costs, a_eq=[np.ones(3)], b_eq=[1], bounds=[(floor, None)] * 3).fun
    feasibility = []
    for budget in [threshold - 0.01, threshold, threshold + 0.3]:
        result = optimize.linprog(np.zeros(3), A_eq=[np.ones(3)], b_eq=[1],
                                 A_ub=[costs], b_ub=[budget], bounds=[(floor, None)] * 3,
                                 method="highs")
        feasibility.append(bool(result.success))
    ok = close(distances, [0.2] * 6) and close(reference_min, threshold)
    ok &= feasibility == [False, True, True]
    return ok, {"persistent_exact_law_gap": distances, "incorrect_omitted_forcing_envelope": 0.0,
                "six_step_cumulative_gap": float(sum(distances)), "propensity_floor": floor,
                "closed_form_minimum_harm": threshold, "lp_minimum_harm": float(reference_min),
                "budgets_feasible_below_at_above_boundary": feasibility,
                "every_action_safe_possible_at_budget_0": bool(np.all(costs <= 0))}, \
        "Expected boundary: persistent forcing survives contractive kernels; positivity versus expected harm has the exact LP feasibility threshold, distinct from per-action safety."


def r05_sharp_bounds(rng):
    cases, gaps = [], []
    for p, mean, U in [(0.9, 0.9, 1.0), (0.1, 0.1, 1.0), (0.4, 0.8, 2.0), (0.0, 0.7, 1.0), (1.0, 0.7, 1.0)]:
        # Joint table is (r,Z)=(0,0),(0,U),(1,0),(1,U).
        eq = np.array([[1, 1, 1, 1], [0, 0, 1, 1], [0, U, 0, U]])
        objective = np.array([0, 0, 0, U])
        lower = lp(objective, a_eq=eq, b_eq=[1, p, mean], bounds=(0, None)).fun
        upper = -lp(-objective, a_eq=eq, b_eq=[1, p, mean], bounds=(0, None)).fun
        analytic = [max(0, mean - (1 - p) * U), min(mean, p * U)]
        gaps.extend([abs(lower - analytic[0]), abs(upper - analytic[1])])
        cases.append({"p": p, "mean": mean, "U": U, "lp_interval": [float(lower), float(upper)], "formula_interval": analytic})
    z, masses, p = np.array([0.0, 0.3, 1.2, 2.0]), np.array([0.15, 0.25, 0.35, 0.25]), 0.45
    lower = lp(z, a_eq=[np.ones(4)], b_eq=[p], bounds=list(zip(np.zeros(4), masses))).fun
    upper = -lp(-z, a_eq=[np.ones(4)], b_eq=[p], bounds=list(zip(np.zeros(4), masses))).fun

    def rearrange(reverse):
        left, total = p, 0.0
        for i in np.argsort(z)[::-1] if reverse else np.argsort(z):
            take = min(left, masses[i]); total += take * z[i]; left -= take
        return total

    quantile = [rearrange(False), rearrange(True)]
    ok = max(gaps) <= ATOL and close([lower, upper], quantile)
    return ok, {"support_endpoint_coupling_cases": cases, "maximum_lp_formula_gap": max(gaps),
                "known_Z_marginal_lp_interval": [float(lower), float(upper)], "quantile_rearrangement_interval": quantile}, \
        "Explicit coupling LPs attain support bounds and fractional-atom quantile bounds; indivisible atoms would require a different feasible coupling set."


def r05_contextual_gates(rng):
    p, mu, U, nu, mass = np.array([0.9, 0.1, 0.0]), np.array([0.9, 0.1, 0.0]), np.array([1., 1., 0.]), np.array([0.1, 0.1, 0.0]), np.array([0.45, 0.45, 0.1])
    A = mu + nu
    low, high = np.maximum(0, mu - (1 - p) * U), np.minimum(mu, p * U)
    aR, aS = np.zeros(3), np.zeros(3)
    nonzero = A > 0
    aR[nonzero] = (low[nonzero] + high[nonzero]) / (2 * A[nonzero])
    aS[nonzero] = low[nonzero] / A[nonzero]
    independent = []
    for i in range(2):
        fn = lambda a: max(A[i] * (a - low[i] / A[i]) ** 2, A[i] * (a - high[i] / A[i]) ** 2)
        ref = optimize.minimize_scalar(fn, bounds=(0, 1), method="bounded", options={"xatol": 1e-14})
        independent.append(float(ref.x))
    endpoint_m = list(itertools.product(*[(low[i], high[i]) for i in range(3)]))
    regrets = [sum(mass[i] * A[i] * (aR[i] - m[i] / A[i]) ** 2 for i in range(2)) for m in endpoint_m]
    q = np.zeros(3); q[nonzero] = (high[nonzero] - low[nonzero]) ** 2 / (4 * A[nonzero])
    worst_difference = float(mass @ (A * aS ** 2 - 2 * aS * low))
    unsafe_regret_gate_difference = A[1] * aR[1] ** 2  # admissible m_1=0
    pooled_low = max(0, float((mass @ mu) - (1 - mass @ p)))
    # A finite nonrectangular set with the same coordinate intervals has a smaller risk.
    cross = np.array([[0., .5], [1., .5], [.5, 0.], [.5, 1.]])
    actual_cross_risk = max(float(np.mean((np.array([.5, .5]) - m) ** 2)) for m in cross)
    rectangular_outer_risk = 0.25
    ok = close(aR[:2], independent, atol=OPT_TOL) and close(max(regrets), mass @ q)
    ok &= pooled_low == 0 and worst_difference < 0 and unsafe_regret_gate_difference > 0
    ok &= aS[2] == 0 and actual_cross_risk < rectangular_outer_risk
    return ok, {"minimax_regret_gates": aR.tolist(), "scalar_optimization_gates": independent,
                "safe_gates": aS.tolist(), "exact_endpoint_worst_regret": max(regrets),
                "formula_integrated_regret": float(mass @ q), "safe_worst_baseline_difference": worst_difference,
                "pooled_lower_bound": pooled_low, "zero_lower_bound_regret_gate_harm": float(unsafe_regret_gate_difference),
                "nonrectangular_risk": actual_cross_risk, "rectangular_outer_risk": rectangular_outer_risk}, \
        "R05 v4 contextual safe gates recover selective surrogate gains, whereas regret gates need not be safe; rectangular ambiguity is substantive."


def r08_channel_envelope(rng):
    cases = []
    max_gap = 0.0
    for p, u, w, left, right in [(0.4, .3, -1.2, 0, 1), (.6, -.2, 1, .3, .8), (.5, 1, .2, 0, 1), (0, -.2, 1, 0, 1), (1, -.2, 1, 0, 1)]:
        grid = np.unique(np.r_[np.linspace(left, right, 41), p])
        objective = (abs(u + w * grid) - abs(u + w * p)) / 2
        low = lp(objective, a_eq=[np.ones(len(grid)), grid], b_eq=[1, p], bounds=(0, None)).fun
        high = -lp(-objective, a_eq=[np.ones(len(grid)), grid], b_eq=[1, p], bounds=(0, None)).fun
        ceiling = (((right - p) * abs(u + w * left) + (p - left) * abs(u + w * right)) / (right - left) - abs(u + w * p)) / 2
        max_gap = max(max_gap, abs(low), abs(high - ceiling))
        cases.append({"prior": p, "margin": [u, w], "lawful_support": [left, right], "lp_information_interval": [float(low), float(high)], "chord_ceiling": ceiling})
    # Same posterior mean and variance, but unequal expected absolute margins.
    x1, m1 = np.array([.3, .7]), np.array([.5, .5])
    x2, m2 = np.array([.1, .5, .9]), np.array([.125, .75, .125])
    info = [float(m1 @ abs(1 - 2 * x1) / 2), float(m2 @ abs(1 - 2 * x2) / 2)]
    equal_moments = close(m1 @ x1, m2 @ x2) and close(m1 @ (x1 - .5) ** 2, m2 @ (x2 - .5) ** 2)
    ok = max_gap < 2e-9 and equal_moments and abs(info[0] - info[1]) > .09
    return ok, {"posterior_law_lp_cases": cases, "maximum_lp_ceiling_gap": max_gap,
                "equal_mean_variance_information_values": info}, \
        "Finite posterior-law LPs attain the channel-free/support-restricted envelopes; posterior mean and variance alone do not identify information value."


def r08_action_identification(rng):
    H, UR, UK = 0.25, 0.5, 0.0
    differences = [H - release + keep for release, keep in itertools.product([0, UR], [0, UK])]
    intervals = [H - UR, H + UK]
    kR, kK = .1, .2
    Hopt = .25
    optional = [Hopt - max(ir - kR, 0) + max(ik - kK, 0)
                for ir, ik in itertools.product([0, UR], [0, UK])]
    expected_optional = [Hopt - max(UR - kR, 0), Hopt + max(UK - kK, 0)]
    # Keep-only records: V is Bernoulli(1/2), keep signal is constant in both worlds.
    keep_records_A = np.array([.5, .5]); keep_records_B = np.array([.5, .5])
    ok = close([min(differences), max(differences)], intervals)
    ok &= min(differences) < 0 < max(differences) and close(keep_records_A, keep_records_B)
    ok &= close([min(optional), max(optional)], expected_optional)
    return ok, {"release_minus_keep_interval": intervals, "two_world_differences": [H, H - UR],
                "same_keep_only_record_max_gap": float(abs(keep_records_A - keep_records_B).max()),
                "optional_measurement_interval": expected_optional,
                "double_charging_cost_would_shift_interval_by": kR - kK}, \
        "Expected boundary: an unsupported release channel reverses the optimal action without changing keep-only records; optional costs are charged once."


def r14_certificate_collapse(rng):
    delta, alpha = .3, .08
    Q1, Q2 = np.array([1 - delta, delta, 0]), np.array([1 - delta, 0, delta])
    # Four interval types: full [0,1], {0}, {1}, empty. Randomization is explicit.
    n = 12
    objective = np.zeros((3, 4)); objective[:, 0] = Q1
    eq = np.zeros((3, n))
    for i in range(3): eq[i, 4 * i:4 * i + 4] = 1
    cover1, cover0 = np.zeros((3, 4)), np.zeros((3, 4))
    cover1[:, [0, 2]] = Q1[:, None]; cover0[:, [0, 1]] = Q2[:, None]
    ref = lp(objective.ravel(), a_eq=eq, b_eq=np.ones(3),
             a_ub=-np.array([cover1.ravel(), cover0.ravel()]), b_ub=[-(1 - alpha)] * 2,
             bounds=(0, None))
    lower = max(0, 1 - 2 * alpha - delta)
    certificate = ref.x.reshape(3, 4)
    tv = 0.5 * abs(Q1 - Q2).sum()
    # Adjoining a common independent seed preserves TV; mapping all records to one
    # statistic destroys it, so a derived statistic cannot create evidence.
    seed_law = np.array([.2, .8])
    seeded_tv = 0.5 * abs(np.outer(Q1, seed_law) - np.outer(Q2, seed_law)).sum()
    ok = close(ref.fun, lower) and close(tv, delta) and close(seeded_tv, delta)
    ok &= float(cover1.ravel() @ ref.x) >= 1 - alpha - 1e-8
    ok &= float(cover0.ravel() @ ref.x) >= 1 - alpha - 1e-8
    return ok, {"observable_tv": float(tv), "miscoverage_alpha": alpha, "full_interval_mass_lp": float(ref.fun),
                "collapse_lower_bound": lower, "seeded_observable_tv": float(seeded_tv),
                "certificate_randomization_by_symbol": certificate.tolist(), "constant_statistic_tv": 0.0}, \
        "The finite observable experiment attains the coverage-collapse bound, including algorithmic randomization and data processing."


def r14_decision_floor(rng):
    lam, delta = .25, .4
    Q1, Q2 = np.array([1 - delta, delta, 0]), np.array([1 - delta, 0, delta])

    def risks(x):
        actions = x[:-1].reshape(3, 2)
        first = (1 - actions[:, 0]) ** 2 + lam * actions[:, 1] ** 2
        second = (1 - actions[:, 1]) ** 2 + lam * actions[:, 0] ** 2
        return np.array([Q1 @ first, Q2 @ second])

    ref = slsqp(lambda x: x[-1], [0.8, .8, 1, 0, 0, 1, .2], [(0, 1)] * 6 + [(0, None)],
                [{"type": "ineq", "fun": lambda x: x[-1] - risks(x)}])
    bound = (1 - delta) * lam / (1 + lam)
    hard_loss = np.array([[1, 0, 1 + lam], [1, 1 + lam, 0]])
    hard_ref = lp([0, 0, 0, 1], a_eq=[[1, 1, 1, 0]], b_eq=[1],
                  a_ub=np.column_stack([hard_loss, -np.ones(2)]), b_ub=[0, 0],
                  bounds=[(0, None)] * 4)
    hard_formula = min(1, (1 + lam) / 2)
    ok = close(ref.fun, bound, atol=OPT_TOL) and close(hard_ref.fun, hard_formula)
    ok &= hard_ref.fun < 1 and lam / (1 + lam) < hard_ref.fun
    return ok, {"continuous_minimax_optimization": float(ref.fun), "common_mass_lower_bound": bound,
                "maximum_constraint_violation": float(max(0, (risks(ref.x) - ref.x[-1]).max())),
                "randomized_hard_minimax_lp": float(hard_ref.fun), "hard_formula": hard_formula,
                "deterministic_hard_minimax": 1.0, "exact_equivalence_continuous_minimax": lam / (1 + lam)}, \
        "The overlap experiment reaches the risk floor; hard-action lotteries help in their nonconvex class and do not contradict continuous convex-action results."


def r15_finite_jet(rng):
    from numpy.polynomial import Polynomial
    results = []
    for p in [0, 1, 2, 3, 4]:
        n, radius, c, C = p + 1, .7, 2.3, 3.0
        plus = Polynomial([C] + [0] * (n - 1) + [c])
        minus = Polynomial([C] + [0] * (n - 1) + [-c])
        jets_equal = all(close(plus.deriv(j)(0), minus.deriv(j)(0)) for j in range(p + 1))
        minima = [polynomial_extrema(poly, radius)[0] for poly in [plus, minus]]
        actions = np.array([-radius, 0, radius])
        regret = np.vstack([plus(actions) - minima[0], minus(actions) - minima[1]])
        ref = lp([0, 0, 0, 1], a_eq=[[1, 1, 1, 0]], b_eq=[1],
                 a_ub=np.column_stack([regret, -np.ones(2)]), b_ub=[0, 0], bounds=[(0, None)] * 4)
        lower = c * radius ** n * (1 if n % 2 else .5)
        results.append({"p": p, "first_omitted_degree": n, "jets_equal": jets_equal,
                        "finite_randomized_action_minimax_lp": float(ref.fun), "ambiguity_floor": lower})
    ok = all(item["jets_equal"] and close(item["finite_randomized_action_minimax_lp"], item["ambiguity_floor"]) for item in results)
    return ok, {"odd_even_cases": results}, \
        "Expected boundary: identical complete finite jets admit opposite omitted-term responses; explicit finite mixtures reproduce the odd/even regret floors."


def r15_remainder_and_degree(rng):
    from numpy.polynomial import Polynomial
    radius = .6
    Y = Polynomial([1., -.8, 1.1, .7, -.2, .1])
    Q = Polynomial(Y.coef[:3])
    remainder = Y - Q
    minimum_Y, _, zstar = polynomial_extrema(Y, radius)
    _, _, zQ = polynomial_extrema(Q, radius)
    derivative = Y.deriv(3)
    low_deriv, high_deriv, _ = polynomial_extrema(derivative, radius)
    M = max(abs(low_deriv), abs(high_deriv))
    lower_rem, upper_rem, _ = polynomial_extrema(remainder, radius)
    epsilon = M * radius ** 3 / math.factorial(3)
    regret = float(Y(zQ) - minimum_Y)
    state = Polynomial([0, 1])
    for _ in range(3): state = state - state ** 3
    loss = state ** 2
    probes = np.array([-.3, -.07, .0, .21, .3])
    direct = probes.copy()
    for _ in range(3): direct = direct - direct ** 3
    ok = max(abs(lower_rem), abs(upper_rem)) <= epsilon + ATOL and regret <= 2 * epsilon + ATOL
    ok &= loss.degree() == 2 * 3 ** 3 and close(loss(probes), direct ** 2)
    return ok, {"uniform_third_derivative_envelope": M, "maximum_exact_polynomial_remainder": max(abs(lower_rem), abs(upper_rem)),
                "taylor_remainder_bound": epsilon, "taylor_optimizer": zQ, "true_optimizer": zstar,
                "optimizer_regret": regret, "two_remainder_regret_bound": 2 * epsilon,
                "three_step_delta_proxy_loss_degree": int(loss.degree()), "predicted_loss_degree": 2 * 3 ** 3}, \
        "Global polynomial extrema verify a supplied remainder envelope; the coupled scalar recurrence independently exhibits exponential degree growth."


def r17_spectral_gate(rng):
    d, outputs = 5, 3
    X = rng.normal(size=(7, d)); weights = rng.uniform(.1, 1, 7)
    G = X.T @ (weights[:, None] * X)
    margin = rng.normal(size=(d, d)); U = G + .2 * margin @ margin.T
    eigenvalues, eigenvectors = np.linalg.eigh(U)
    eigenvalues, eigenvectors = eigenvalues[::-1], eigenvectors[:, ::-1]
    rank = 2
    factor = eigenvectors[:, :rank] * np.sqrt(eigenvalues[:rank])
    tail = float(eigenvalues[rank])
    C = factor @ factor.T + tail * np.eye(d)
    tight_C = factor @ factor.T + tail * (np.eye(d) - eigenvectors[:, :rank] @ eigenvectors[:, :rank].T)
    k = rng.normal(size=d); k /= np.linalg.norm(k)
    residual = rng.normal(size=outputs); beta = .4
    perturbation = beta * np.outer(k, residual)
    direct_energy = float(np.sum(weights[:, None] * (X @ perturbation) ** 2))
    formula_energy = beta ** 2 * float(residual @ residual) * float(k @ G @ k)
    score = float(residual @ residual) * float(k @ C @ k)
    budget = .11 * score
    safe = min(1, math.sqrt(budget / score))
    safe_actual = float(np.sum(weights[:, None] * (X @ (safe * np.outer(k, residual))) ** 2))
    omitted_tail_k = eigenvectors[:, rank]
    omitted_report = float(np.linalg.norm(factor.T @ omitted_tail_k) ** 2)
    omitted_true = float(omitted_tail_k @ U @ omitted_tail_k)
    quarter = float(np.sum(weights[:, None] * (X @ (perturbation / 2)) ** 2))
    loewner_slack = float(np.linalg.eigvalsh(C - U).min())
    tight_slack = float(np.linalg.eigvalsh(tight_C - U).min())
    ok = close(direct_energy, formula_energy) and loewner_slack >= -ATOL and tight_slack >= -ATOL
    ok &= safe_actual <= budget + ATOL and close(quarter, direct_energy / 4)
    ok &= omitted_report <= ATOL and close(omitted_true, tail) and tail > 0
    return ok, {"direct_frozen_output_energy": direct_energy, "rank_one_identity_energy": formula_energy,
                "low_rank_plus_tail_minimum_loewner_slack": loewner_slack, "tight_eigen_tail_minimum_slack": tight_slack,
                "safe_gate": safe, "budget": budget, "actual_safe_energy": safe_actual,
                "missing_tail_reported_score": omitted_report, "missing_tail_true_score": omitted_true,
                "zero_residual_update_energy": 0.0, "zero_residual_safe_gate": 1.0}, \
        "R17 v3 residual-scaled energy and safe gate hold in frozen trajectories; omitting the spectral tail creates an explicit unsafe direction."


def r19_finite_enumeration(rng):
    cases = [
        (2, np.zeros((0, 2), dtype=int), [np.array([[1, 0]]), np.array([[0, 1]])]),
        (2, np.array([[1, 0, 0]]), [np.array([[1, 1, 0], [0, 1, 0]]), np.array([[1, 0, 0]])]),
        (3, np.array([[1, 0]]), [np.array([[1, 1]]), np.array([[2, 2]])]),
        (3, np.array([[1, 0]]), [np.array([[2, 0]])]),
    ]
    metrics, all_ok = [], True
    for prime, A, branches in cases:
        n = A.shape[1]; B = np.vstack(branches)
        r = gf_rank(np.vstack([A, B]), prime) - gf_rank(A, prime)
        states = np.array(list(itertools.product(range(prime), repeat=n)), dtype=int)
        side = (states @ A.T) % prime
        release = (states @ B.T) % prime
        adjacency = np.zeros((len(states), len(states)), dtype=bool)
        for i in range(len(states)):
            for j in range(i):
                adjacency[i, j] = adjacency[j, i] = np.array_equal(side[i], side[j]) and not np.array_equal(release[i], release[j])
        chromatic, coloring = exact_chromatic(adjacency)
        # Complement-row construction, then exhaustive lookup decoding for every branch.
        C = np.zeros((0, n), dtype=int); existing = A.copy()
        for row in B:
            proposed = np.vstack([existing, row])
            if gf_rank(proposed, prime) > gf_rank(existing, prime):
                C = np.vstack([C, row]); existing = proposed
        code = states @ C.T % prime
        decoded = True
        for branch_id, branch in enumerate(branches):
            lookup = {}
            offset = np.arange(branch.shape[0]) % prime
            for i in range(len(states)):
                key = (tuple(side[i]), tuple(code[i]), branch_id)
                target = tuple((branch @ states[i] + offset) % prime)
                if key in lookup and lookup[key] != target: decoded = False
                lookup[key] = target
        valid_coloring = all(coloring[i] != coloring[j] for i in range(len(states)) for j in range(i) if adjacency[i, j])
        all_ok &= chromatic == prime ** r and C.shape[0] == r and decoded and valid_coloring
        metrics.append({"prime": prime, "full_domain_size": len(states), "quotient_rank": r,
                        "rank_message_count": prime ** r, "exhaustive_graph_chromatic_number": chromatic,
                        "syndrome_symbols": C.shape[0], "all_states_branches_decode": decoded,
                        "minimum_fixed_length_bits": math.ceil(r * math.log2(prime))})
    # Actual reachable graph rather than ambient rank: a singleton needs one message.
    singleton_chromatic, _ = exact_chromatic(np.zeros((1, 1), dtype=bool))
    all_ok &= singleton_chromatic == 1
    return all_ok, {"full_space_prime_field_cases": metrics, "singleton_actual_message_count": singleton_chromatic,
                    "singleton_ambient_rank_message_count": 2}, \
        "Actual finite-domain confusability coloring and exhaustive syndrome decoding reproduce q^r; ambient ranks overcount a restricted singleton domain."


def qwrd_observation_and_query(rng):
    states = np.array(list(itertools.product([-1., 1.], repeat=2)))
    masses = np.ones(4) / 4
    posterior_mean = np.column_stack([states[:, 0], np.zeros(4)])
    W = np.diag([2., .5])
    decoder = np.zeros_like(states)
    error = states - decoder
    obs_error = states - posterior_mean
    bit_error = posterior_mean - decoder
    total = float(np.sum(masses * np.einsum("ni,ij,nj->n", error, W, error)))
    observation = float(np.sum(masses * np.einsum("ni,ij,nj->n", obs_error, W, obs_error)))
    coding = float(np.sum(masses * np.einsum("ni,ij,nj->n", bit_error, W, bit_error)))
    cross = float(np.sum(masses * np.einsum("ni,ij,nj->n", obs_error, W, bit_error)))
    # One lawful bit encodes the first coordinate exactly but cannot remove the second.
    one_bit_distortion = float(np.sum(masses * np.einsum("ni,ij,nj->n", obs_error, W, obs_error)))
    x, query = np.array([1., 2.]), np.array([1., 2.])
    conditional_query_actual = float(np.mean((x * query) ** 2))
    invalid_fixed_gram = float(np.mean(x ** 2) * np.mean(query ** 2))
    ok = close(total, observation + coding) and close(cross, 0) and close(one_bit_distortion, observation)
    ok &= abs(conditional_query_actual - invalid_fixed_gram) > 2
    return ok, {"zero_bit_total_distortion": total, "irreducible_observation_distortion": observation,
                "zero_bit_excess_coding_distortion": coding, "orthogonality_cross_term": cross,
                "one_bit_distortion": one_bit_distortion, "state_dependent_query_actual_distortion": conditional_query_actual,
                "invalid_average_gram_prediction": invalid_fixed_gram}, \
        "Exact finite joint enumeration separates observation from bit error; state-dependent query second moments invalidate a fixed average Gram."


def qwrd_gaussian_and_quantizer(rng):
    lambdas, rate = np.array([4., 1., .25]), 2.3
    level, allocation = waterfill(lambdas, rate)
    formula = float(np.minimum(lambdas, level).sum())
    objective = lambda r: float(np.sum(lambdas * np.exp2(-2 * r)))
    ref = slsqp(objective, np.full(3, rate / 3), [(0, rate)] * 3,
                [{"type": "ineq", "fun": lambda r: rate - r.sum()}])
    # Integrate the actual scalar fixed codebook, including overload tails.
    bits, clipping = 3, 2.5
    levels = np.linspace(-clipping, clipping, 2 ** bits)
    separators = np.r_[-np.inf, (levels[:-1] + levels[1:]) / 2, np.inf]
    actual, quadrature_error = 0.0, 0.0
    for j, reconstruction in enumerate(levels):
        value, err = integrate.quad(lambda x: (x - reconstruction) ** 2 * stats.norm.pdf(x),
                                    separators[j], separators[j + 1], epsabs=1e-12, epsrel=1e-11)
        actual += value; quadrature_error += err
    tail_formula = 2 * ((1 + clipping ** 2) * stats.norm.sf(clipping) - clipping * stats.norm.pdf(clipping))
    tail_quad = 2 * integrate.quad(lambda x: (x - clipping) ** 2 * stats.norm.pdf(x), clipping, np.inf,
                                  epsabs=1e-12, epsrel=1e-11)[0]
    upper = clipping ** 2 / (2 ** bits - 1) ** 2 + tail_formula
    shannon_scalar_lower = 2 ** (-2 * bits)
    # Same covariance, different source: a binary +/-1 source is exact in one bit.
    non_gaussian_distortion, wrongly_exported_bound = 0.0, 0.25
    ok = close(ref.fun, formula, atol=OPT_TOL) and close(allocation.sum(), rate)
    ok &= close(tail_formula, tail_quad) and shannon_scalar_lower - ATOL <= actual <= upper + ATOL
    ok &= quadrature_error < 1e-9 and non_gaussian_distortion < wrongly_exported_bound
    return ok, {"gaussian_eigenvalues": lambdas.tolist(), "rate_bits": rate, "water_level": level,
                "waterfill_allocation": allocation.tolist(), "shannon_distortion_formula": formula,
                "independent_rate_optimization_distortion": float(ref.fun), "scalar_quantizer_bits": bits,
                "scalar_actual_quadrature_distortion": actual, "quadrature_error_estimate": quadrature_error,
                "scalar_shannon_converse": shannon_scalar_lower, "clipping_quantization_upper_bound": upper,
                "tail_formula": tail_formula, "tail_quadrature": tail_quad,
                "binary_same_covariance_one_bit_distortion": non_gaussian_distortion,
                "invalid_gaussian_export_lower_bound": wrongly_exported_bound}, \
        "Independent convex allocation and exact codebook quadrature support the Gaussian converse and constructive upper bound; covariance alone does not justify Gaussian RDF."


def qwrd_recursive_and_fano(rng):
    Hprev, Hnext = np.diag([1., 0.]), np.diag([2., 0.])
    A = np.array([[.6, 0], [.2, .8]])
    errors = np.array([[1., 8.], [-1., -3.], [.4, 2.], [-.4, -2.]])
    innovations = np.array([[.2, 1.], [-.2, -1.], [.1, 0], [-.1, 0]])
    following = errors @ A.T + innovations
    Dprev = float(np.mean(np.einsum("ni,ij,nj->n", errors, Hprev, errors)))
    Dnext = float(np.mean(np.einsum("ni,ij,nj->n", following, Hnext, following)))
    epsilon = float(np.mean(np.einsum("ni,ij,nj->n", innovations, Hnext, innovations)))
    L = float(np.linalg.norm(psd_sqrt(Hnext) @ A @ psd_sqrt(np.linalg.pinv(Hprev)), 2))
    compatible_defect = float(np.linalg.norm(psd_sqrt(Hnext) @ A @ (np.eye(2) - np.linalg.pinv(Hprev) @ Hprev)))
    bridge_A = np.array([[.6, 1.], [.2, .8]])
    bridge_errors = []
    for scale in [1., 10., 100.]:
        invisible = np.array([0., scale]); visible = bridge_A @ invisible
        bridge_errors.append(float(visible @ Hnext @ visible))
    # Enumerate every deterministic two-message encoder on all four binary states.
    source = np.array(list(itertools.product([0, 1], repeat=2)))
    distortions = []
    for assignment in itertools.product([0, 1], repeat=4):
        loss = 0
        for code in [0, 1]:
            group = source[np.array(assignment) == code]
            if len(group):
                for coordinate in range(2):
                    ones = int(group[:, coordinate].sum())
                    loss += min(ones, len(group) - ones)
        distortions.append(loss / 8)
    best_D = min(distortions)
    entropy = -best_D * math.log2(best_D) - (1 - best_D) * math.log2(1 - best_D)
    fano = 2 * (1 - entropy)
    ok = compatible_defect <= ATOL and math.sqrt(Dnext) <= L * math.sqrt(Dprev) + math.sqrt(epsilon) + ATOL
    ok &= close(bridge_errors, [2, 200, 20000]) and close(best_D, .25) and fano <= 1 + ATOL
    return ok, {"compatible_kernel_defect": compatible_defect, "root_mse_actual": math.sqrt(Dnext),
                "root_mse_bound": L * math.sqrt(Dprev) + math.sqrt(epsilon), "bridge_prior_distortion": 0.0,
                "bridge_next_distortions": bridge_errors, "enumerated_encoders": len(distortions),
                "best_one_bit_two_coordinate_symbol_error": best_D, "fano_required_bits_at_that_error": fano,
                "zero_error_message_count": 4}, \
        "The seminorm recursion requires kernel compatibility; an invisible bridge direction yields unbounded next distortion. A finite encoder enumeration supports the coordinate Fano boundary."


def compound_hedge(rng):
    probabilities = np.array([.6, .3, .1, 0.])
    rate, delivery, variance = 1.7, .4, 1.3
    level, allocation = waterfill(probabilities, rate)
    factor = variance * 2 ** (-2 * delivery)
    formula = factor * float(np.minimum(probabilities, level).sum())
    objective = lambda r: factor * float(np.sum(probabilities * np.exp2(-2 * r)))
    ref = slsqp(objective, np.full(4, rate / 4), [(0, rate)] * 4,
                [{"type": "ineq", "fun": lambda r: rate - r.sum()}])
    m = 3
    minimax_formula = variance * 2 ** (-2 * (delivery + rate / m))
    minimax_ref = slsqp(lambda x: x[-1], [rate / m] * m + [minimax_formula + .1],
                       [(0, rate)] * m + [(0, None)],
                       [{"type": "ineq", "fun": lambda x: rate - x[:m].sum()},
                        {"type": "ineq", "fun": lambda x: x[-1] - factor * np.exp2(-2 * x[:m])}])
    fresh = variance * 2 ** (-2 * (delivery + rate))
    tax_ratio = minimax_formula / fresh
    ok = close(ref.fun, formula, atol=OPT_TOL) and close(minimax_ref.fun, minimax_formula, atol=OPT_TOL)
    ok &= close(tax_ratio, 2 ** (2 * rate * (1 - 1 / m))) and allocation[-1] == 0
    return ok, {"prior": probabilities.tolist(), "cache_bits_per_source_vector": rate, "delivery_bits": delivery,
                "bayesian_cache_allocation": allocation.tolist(), "bayesian_formula_distortion": formula,
                "independent_allocation_optimization": float(ref.fun), "minimax_formula": minimax_formula,
                "minimax_epigraph_optimization": float(minimax_ref.fun), "fresh_reencoding_distortion": fresh,
                "immutable_prefix_distortion_ratio": tax_ratio, "rate_tax": rate * (1 - 1 / m)}, \
        "Convex references recover the Bayesian and minimax Gaussian cache boundaries, including aggregate-rate units and the fresh-encoding comparison."


def compound_information_boundaries(rng):
    # Message-only stage 2 cannot add source information: every mapping is enumerated.
    source = list(itertools.product([0, 1], repeat=2))
    M0 = [x[0] for x in source]

    def entropy_of_coordinate_given(records, coordinate):
        groups = {}
        for x, record in zip(source, records):
            groups.setdefault(record, []).append(x[coordinate])
        result = 0.0
        for group in groups.values():
            p = sum(group) / len(group)
            h = 0 if p in [0, 1] else -p * math.log2(p) - (1 - p) * math.log2(1 - p)
            result += len(group) / 4 * h
        return result

    largest_gain = 0.0
    for j in range(2):
        base_entropy = entropy_of_coordinate_given(M0, j)
        for mapping in itertools.product([0, 1, 2], repeat=2):
            records = [(m, mapping[m]) for m in M0]
            largest_gain = max(largest_gain, base_entropy - entropy_of_coordinate_given(records, j))
    R, Delta = 1.0, .5
    correlated_shared_source_distortion = 2 ** (-2 * (R + Delta))
    invalid_independent_formula = 2 ** (-2 * (R / 2 + Delta))
    ok = close(largest_gain, 0) and correlated_shared_source_distortion < invalid_independent_formula
    return ok, {"retained_message_only_refinement_mappings_per_query": 9,
                "largest_added_source_information_bits": largest_gain,
                "perfectly_correlated_common_source_distortion": correlated_shared_source_distortion,
                "invalid_independent_coordinate_prediction": invalid_independent_formula,
                "one_coordinate_hedge_tax": 0.0, "zero_cache_hedge_tax": 0.0}, \
        "Expected boundaries: a retained-message-only delivery cannot refine information; independent-coordinate formulas do not apply to correlated sources."


def active_immediate_expansion(rng):
    S = rng.normal(size=(3, 2)); k = np.array([1., -2., .5]); e = np.array([.8, -.3])
    v = S.T @ k + e
    U = np.outer(k, e) / float(k @ k)
    queries = rng.normal(size=(4, 3)); residuals = rng.normal(size=(4, 2))
    targets = queries @ S - residuals
    weights = np.array([.2, .5, .8, 1.])
    M = np.array([[1., .2], [.2, .7]])

    def protected(state):
        residual = queries @ state - targets
        return .5 * float(np.sum(weights * np.einsum("ni,ij,nj->n", residual, M, residual)))

    coefficient = queries @ k / float(k @ k)
    linear = float(np.sum(weights * coefficient * (residuals @ M @ e)))
    quadratic = float(np.sum(weights * coefficient ** 2) * (e @ M @ e))
    bs = np.array([0., .1, .4, 1.])
    actual = np.array([protected(S + b * U) - protected(S) for b in bs])
    expansion = bs * linear + .5 * bs ** 2 * quadratic
    omitted_error = float(abs(actual[-1] - .5 * quadratic))
    ok = close((S + .4 * U).T @ k, S.T @ k + .4 * e) and close(actual, expansion)
    ok &= abs(linear) > 1e-4 and omitted_error > 1e-4
    return ok, {"normalized_delta_read_identity_max_gap": float(abs((S + .4 * U).T @ k - (S.T @ k + .4 * e)).max()),
                "old_loss_linear_coefficient": linear, "old_loss_quadratic_coefficient": quadratic,
                "direct_old_loss_differences": actual.tolist(), "complete_expansion": expansion.tolist(),
                "omitted_cross_term_error_at_full_write": omitted_error}, \
        "Direct protected-loss evaluation verifies the normalized Delta expansion; noncentered protected residuals make displacement-only stakes incomplete."


def active_channels(rng):
    A, B, prior = 2.7, .8, .23
    channel = np.array([[.8, .2], [.2, .8]])  # rows H=0,H=1
    marginal = (1 - prior) * channel[0] + prior * channel[1]
    posterior = prior * channel[1] / marginal
    soft = posterior * A / (posterior * A + (1 - posterior) * B)
    envelope = posterior * (1 - posterior) * A * B / (posterior * A + (1 - posterior) * B)
    independent = []
    for p in posterior:
        ref = optimize.minimize_scalar(lambda b: p * A * (1 - b) ** 2 + (1 - p) * B * b ** 2,
                                       bounds=(0, 1), method="bounded", options={"xatol": 1e-13})
        independent.append(ref.x)
    hard_direct = float(np.sum(np.minimum(prior * A * channel[1], (1 - prior) * B * channel[0])))
    hard_posteriors = float(marginal @ np.minimum(posterior * A, (1 - posterior) * B))
    prior_risk = prior * (1 - prior) * A * B / (prior * A + (1 - prior) * B)
    soft_risk = float(marginal @ envelope)
    garbling = np.array([[.7, .3], [.3, .7]])
    degraded = channel @ garbling
    marginal_g = (1 - prior) * degraded[0] + prior * degraded[1]
    pg = prior * degraded[1] / marginal_g
    risk_g = float(marginal_g @ (pg * (1 - pg) * A * B / (pg * A + (1 - pg) * B)))
    # Informative channel with all posterior values on one hard-action side.
    weak_prior, weak_channel = .1, np.array([[.6, .4], [.4, .6]])
    weak_marginal = (1 - weak_prior) * weak_channel[0] + weak_prior * weak_channel[1]
    weak_post = weak_prior * weak_channel[1] / weak_marginal
    weak_soft_risk = float(weak_marginal @ (weak_post * (1 - weak_post)))
    weak_hard_risk = float(np.minimum(weak_prior * weak_channel[1], (1 - weak_prior) * weak_channel[0]).sum())
    ok = close(soft, independent, atol=OPT_TOL) and close(marginal @ posterior, prior)
    ok &= close(hard_direct, hard_posteriors) and soft_risk < risk_g < prior_risk
    ok &= close(weak_hard_risk, weak_prior) and weak_soft_risk < weak_prior * (1 - weak_prior)
    return ok, {"posterior_mean": float(marginal @ posterior), "prior": prior,
                "soft_actions_formula": soft.tolist(), "independent_scalar_actions": independent,
                "no_probe_soft_risk": prior_risk, "probe_soft_risk": soft_risk, "garbled_probe_soft_risk": risk_g,
                "hard_risk_integral": hard_direct, "weak_informative_posteriors": weak_post.tolist(),
                "weak_hard_gross_value": weak_prior - weak_hard_risk,
                "weak_soft_gross_value": weak_prior * (1 - weak_prior) - weak_soft_risk}, \
        "Exact binary channels support soft Bayes/Blackwell value; informative probes can have zero hard value while having strictly positive soft value."


def active_minimax_and_cost(rng):
    A, B = 2.7, .8
    expected_b = math.sqrt(A) / (math.sqrt(A) + math.sqrt(B))
    expected_risk = A * B / (math.sqrt(A) + math.sqrt(B)) ** 2
    ref = optimize.minimize_scalar(lambda b: max(A * (1 - b) ** 2, B * b ** 2),
                                   bounds=(0, 1), method="bounded", options={"xatol": 1e-14})
    channel = np.array([[.8, .2], [.2, .8]])

    def state_risks(x):
        return np.array([B * (channel[0] @ (x[:2] ** 2)), A * (channel[1] @ ((1 - x[:2]) ** 2))])

    minimax = slsqp(lambda x: x[-1], [.3, .7, .4], [(0, 1), (0, 1), (0, None)],
                    [{"type": "ineq", "fun": lambda x: x[-1] - state_risks(x)}])

    def bayes_risk(pi):
        joint0, joint1 = (1 - pi) * channel[0], pi * channel[1]
        denominator = A * joint1 + B * joint0
        return float(np.sum(A * B * joint1 * joint0 / denominator))

    least_favorable = optimize.minimize_scalar(lambda pi: -bayes_risk(pi), bounds=(0, 1), method="bounded",
                                              options={"xatol": 1e-13})
    C, error = 1.4, .2
    gross_value = C * (.5 - error) ** 2
    direct_bsc_risk = C * error * (1 - error)
    costs = [gross_value - .01, gross_value, gross_value + .01]
    worthwhile = [direct_bsc_risk + cost < C / 4 - 1e-12 for cost in costs]
    ok = close(ref.x, expected_b, atol=OPT_TOL) and close(ref.fun, expected_risk, atol=OPT_TOL)
    ok &= close(minimax.fun, -least_favorable.fun, atol=OPT_TOL) and worthwhile == [True, False, False]
    return ok, {"no_probe_minimax_action": expected_b, "scalar_reference_action": float(ref.x),
                "no_probe_minimax_risk": expected_risk, "fixed_probe_minimax_epigraph": float(minimax.fun),
                "least_favorable_prior": float(least_favorable.x), "least_favorable_bayes_risk": float(-least_favorable.fun),
                "symmetric_channel_gross_value": gross_value, "probe_cost_cases": costs,
                "strictly_worthwhile_below_at_above_boundary": worthwhile}, \
        "Convex references support the minimax and cost thresholds for a fixed probe; no exchange of probe-selection and prior maximization is assumed."


CHECKS = [
    ("R02-aipw-sharp-identifiability", "R02", r02_aipw),
    ("R02-uniform-value-bound", "R02", r02_value),
    ("R02-overlap-occupancy-coefficient-boundaries", "R02", r02_boundaries),
    ("R03-v3-full-law-wasserstein", "R03", r03_wasserstein),
    ("R03-v3-forcing-safe-logging-feasibility", "R03", r03_forcing_and_feasibility),
    ("R05-v4-sharp-coupling-bounds", "R05", r05_sharp_bounds),
    ("R05-v4-contextual-regret-and-safe-gates", "R05", r05_contextual_gates),
    ("R08-posterior-channel-envelope", "R08", r08_channel_envelope),
    ("R08-unsupported-action-and-optional-cost", "R08", r08_action_identification),
    ("R14-coverage-collapse-finite-lp", "R14", r14_certificate_collapse),
    ("R14-overlap-minimax-action-classes", "R14", r14_decision_floor),
    ("R15-finite-jet-odd-even-ambiguity", "R15", r15_finite_jet),
    ("R15-uniform-remainder-degree-growth", "R15", r15_remainder_and_degree),
    ("R17-v3-residual-scaled-spectral-gate", "R17", r17_spectral_gate),
    ("R19-finite-field-actual-graph-enumeration", "R19", r19_finite_enumeration),
    ("QWRD-observation-and-query-assumptions", "query_weighted_rate_distortion", qwrd_observation_and_query),
    ("QWRD-gaussian-converse-codebook-quadrature", "query_weighted_rate_distortion", qwrd_gaussian_and_quantizer),
    ("QWRD-compatible-recursion-finite-fano", "query_weighted_rate_distortion", qwrd_recursive_and_fano),
    ("compound-hedge-convex-reference", "compound_query_hedge", compound_hedge),
    ("compound-hedge-information-boundaries", "compound_query_hedge", compound_information_boundaries),
    ("active-evidence-immediate-cross-term", "active_evidence", active_immediate_expansion),
    ("active-evidence-soft-hard-blackwell", "active_evidence", active_channels),
    ("active-evidence-minimax-probe-cost", "active_evidence", active_minimax_and_cost),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()
    started = time.perf_counter()
    checks = []
    manifest_path = BASE / "source_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    indexed_sources = {item["path"]: item for item in manifest["sources"]}
    manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    refs = {key: [{"path": path, "sha256": indexed_sources[path]["sha256"],
                   "repository_commit": manifest["commit"], "source_manifest_sha256": manifest_hash}]
            for key, path in SOURCES.items()}
    integrity = {}
    for key, path in SOURCES.items():
        digest = hashlib.sha256((BASE / path).read_bytes()).hexdigest()
        integrity[key] = digest == indexed_sources[path]["sha256"]
    checks.append({"id": "statistics-assigned-source-integrity", "lineage": list(SOURCES),
                   "scope": "Pinned source integrity; read-only byte hashes", "status": "passed" if all(integrity.values()) else "failed",
                   "metrics": {"source_matches_manifest": integrity, "source_manifest_sha256": manifest_hash},
                   "source_refs": [reference for entry in refs.values() for reference in entry],
                   "interpretation": "The numerical audit is bound to the assigned latest pinned source bytes."})
    try:
        global np, optimize, integrate, stats
        import numpy as np
        from scipy import optimize, integrate, stats
    except ImportError as error:
        for check_id, lineage, _ in CHECKS:
            checks.append({"id": check_id, "lineage": lineage, "scope": "Constructed deterministic diagnostic; not a native benchmark or proof",
                           "status": "inconclusive", "metrics": {"dependency_error": str(error)}, "source_refs": refs[lineage],
                           "interpretation": "NumPy/SciPy are required; this script does not install dependencies."})
    else:
        for index, (check_id, lineage, operation) in enumerate(CHECKS):
            check_started = time.perf_counter()
            try:
                if not integrity[lineage]:
                    raise RuntimeError("assigned source hash does not match source_manifest.json")
                # Independent per-check streams make additions insensitive to ordering.
                rng = np.random.default_rng(np.random.SeedSequence([args.seed, index]))
                passed, metrics, interpretation = operation(rng)
                status = "passed" if passed else "failed"
            except Exception as error:
                status, metrics = "failed", {"exception_type": type(error).__name__, "error": str(error)}
                interpretation = "Diagnostic execution failed; inspect the reported exception before interpreting any scientific claim."
            metrics.update({"elapsed_seconds": time.perf_counter() - check_started,
                            "fp64_absolute_tolerance": ATOL, "fp64_relative_tolerance": RTOL,
                            "convex_optimizer_comparison_tolerance": OPT_TOL})
            checks.append({"id": check_id, "lineage": lineage,
                           "scope": "Constructed deterministic numerical diagnostic; not a public benchmark, deployment certificate, or proof",
                           "status": status, "metrics": metrics, "source_refs": refs[lineage], "interpretation": interpretation})
    result = {"suite": "delta_cpu_statistics", "seed": args.seed, "checks": checks,
              "elapsed_seconds": time.perf_counter() - started}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"suite": result["suite"], "output": str(args.output),
                      "status_counts": {status: sum(c["status"] == status for c in checks) for status in ["passed", "failed", "inconclusive"]},
                      "elapsed_seconds": result["elapsed_seconds"]}))
    return 1 if any(check["status"] == "failed" for check in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
