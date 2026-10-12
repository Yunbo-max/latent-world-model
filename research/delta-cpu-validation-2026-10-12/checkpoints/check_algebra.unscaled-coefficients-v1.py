#!/usr/bin/env python3
"""Small FP64 diagnostics for pinned Delta repair mathematics, not model efficacy.

Only the parent/controller is authorized to execute this contribution. Each
boundary check passes when a declared counterexample is reproduced; that status
does not denote an algorithm's success. NumPy/SciPy only; no model or downloads.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time
import traceback

import numpy as np
from scipy.linalg import block_diag, expm, null_space
from scipy.optimize import minimize_scalar


ROOT = Path(__file__).resolve().parents[1]
ATOL = 2e-10
RTOL = 2e-10
FD_TOL = 2e-7
RANK_TOL = 1e-11
SOURCE_NAMES = {
    "R01": "R01_TRANSPORTED_CREDIT_QUOTIENT.v3.md",
    "R04": "R04_CONSOLIDATION_DYNAMICS.v3.md",
    "R06": "R06_SURVIVAL_MARGIN_PLASTICITY.v3.md",
    "R07": "R07_FACTOR_CORE_JOINT_MARGIN.v3.md",
    "R09": "R09_ROBUST_GRAMIAN_CARRIER.v3.md",
    "R10": "R10_INVARIANT_RESIDUAL_CARRIER.v3.md",
    "R11": "R11_LAZY_OVERLAY_CLOSURE.v3.md",
    "R12": "R12_GRAM_COMPONENT_CLOSURE.v3.md",
    "R13": "R13_MINIMUM_ERASURE_LEDGER.v3.md",
    "R16": "R16_SHARED_CARRIER_SCAN.v3.md",
    "R18": "R18_BOUNDED_FIBER_LEAKAGE_LEDGER.v3.md",
    "R20": "R20_SPECTRAL_TRANSFER_CERTIFICATE.v3.md",
}


class DiagnosticFailure(Exception):
    def __init__(self, message, metrics):
        super().__init__(message)
        self.metrics = dict(metrics)


def require(condition, message, metrics):
    if not bool(condition):
        raise DiagnosticFailure(message, metrics)


def close(metrics, label, actual, expected, atol=ATOL, rtol=RTOL):
    actual, expected = np.asarray(actual), np.asarray(expected)
    error = float(np.linalg.norm(actual - expected))
    scale = max(float(np.linalg.norm(actual)), float(np.linalg.norm(expected)))
    metrics[label + "_absolute_error"] = error
    metrics[label + "_relative_error"] = error / max(scale, np.finfo(float).tiny)
    metrics[label + "_allowed_error"] = atol + rtol * scale
    require(np.isfinite(error) and error <= atol + rtol * scale,
            label + " disagrees with independent reference", metrics)


def norm2(x):
    return float(np.linalg.norm(x, 2))


def rank(x):
    s = np.linalg.svd(x, compute_uv=False)
    return int(np.sum(s > RANK_TOL * max(1.0, float(s[0]) if len(s) else 0.0)))


def basis(x):
    x = np.asarray(x, dtype=np.float64)
    if x.shape[1] == 0:
        return np.empty((x.shape[0], 0), dtype=np.float64)
    u, s, _ = np.linalg.svd(x, full_matrices=False)
    return u[:, s > RANK_TOL * max(1.0, float(s[0]) if len(s) else 0.0)]


def psd(rng, n, shift=0.0):
    z = rng.normal(size=(n, n)) / np.sqrt(n)
    return z @ z.T + shift * np.eye(n)


def ordered_product(mats, d):
    """Input is chronological; a later transition multiplies on the left."""
    result = np.eye(d)
    for mat in mats:
        result = mat @ result
    return result


def delta(s, k, v, beta, decay=None):
    z = s if decay is None else decay @ s
    return z + beta * np.outer(k, v - z.T @ k)


def fd_jacobian(fun, x, h):
    columns = []
    for j in range(len(x)):
        direction = np.zeros_like(x)
        direction[j] = h
        columns.append((fun(x + direction) - fun(x - direction)) / (2 * h))
    return np.column_stack(columns)


def constrained_quadratic(h, a, e):
    """Independent dense equality-KKT reference, no inverse-action formula."""
    n, p = h.shape[0], a.shape[0]
    system = np.block([[h, a.T], [a, np.zeros((p, p))]])
    return np.linalg.solve(system, np.r_[np.zeros(n), e])[:n]


def r01_transport(rng):
    m = {}
    dk, dv, horizon = 3, 4, 3
    aa = [0.7 * np.eye(dk) + 0.1 * rng.normal(size=(dk, dk)) for _ in range(horizon)]
    kk = [0.15 * rng.normal(size=(dk, dv)) for _ in range(horizon)]
    gg = [rng.normal(size=(dk, dv)) for _ in range(horizon)]
    bb = [rng.normal(size=(dk, dv)) for _ in range(horizon)]
    credits = [(1, rng.normal(size=(dk, dv))), (3, rng.normal(size=(dk, dv)))]

    def tangent(j, x):
        return aa[j] @ x + kk[j] * np.sum(gg[j] * x)

    # A dense operator assembled by acting on elementary matrices provides an
    # independent transpose/reference, including an explicit vectorization order.
    for j in range(horizon):
        elementary = np.eye(dk * dv).reshape(dk * dv, dk, dv)
        dense = np.column_stack([tangent(j, x).ravel() for x in elementary])
        y = rng.normal(size=(dk, dv))
        analytic = aa[j].T @ y + gg[j] * np.sum(kk[j] * y)
        close(m, f"adjoint_step_{j}", analytic.ravel(), dense.T @ y.ravel())
    x = rng.normal(size=(dk, dv))
    states, zero_states = [x], [np.zeros_like(x)]
    for j in range(horizon):
        states.append(tangent(j, states[-1]) + bb[j])
        zero_states.append(tangent(j, zero_states[-1]) + bb[j])
    transported = []
    for index, (time_index, c) in enumerate(credits):
        d = c.copy()
        for j in reversed(range(time_index)):
            d = aa[j].T @ d + gg[j] * np.sum(kk[j] * d)
        transported.append(d)
        direct = np.sum(c * (states[time_index] - zero_states[time_index]))
        close(m, f"credit_{index}", direct, np.sum(d * x))
    w = basis(np.vstack(transported).T)
    for index, d in enumerate(transported):
        close(m, f"quotient_credit_{index}", np.sum(d * x), np.sum((d @ w) * (x @ w)))
    small = w[:, :-1]
    proj = small @ small.T
    d = max(transported, key=lambda c: np.linalg.norm(c @ (np.eye(dv) - proj)))
    witness = d @ (np.eye(dv) - proj)
    close(m, "too_small_quotient", witness @ small, np.zeros((dk, small.shape[1])))
    m["minimum_right_width"] = w.shape[1]
    m["smaller_width_credit_gap"] = float(np.sum(d * witness))
    require(m["smaller_width_credit_gap"] > 1e-8, "missing quotient direction has no witness", m)
    return m, "Adjoint transport and quotient credits match direct affine rollouts; removing a required right direction loses an ambient credit."


def r01_boundary(rng):
    m = {}
    c = np.zeros((2, 3)); c[0, 0] = 1
    k = np.zeros((2, 3)); k[1, 1] = 1
    g = np.zeros((2, 3)); g[0, 1] = 1
    d = c + g * np.sum(k * c)
    m["raw_envelope_width"] = rank(np.vstack([c, g]))
    m["transported_width"] = rank(d)
    require(m["raw_envelope_width"] == 2 and m["transported_width"] == 1,
            "zero transported coupling did not shrink the raw envelope", m)
    w = np.eye(3)[:, :1]
    hidden = np.zeros((2, 3)); hidden[0, 2] = 1
    suffix_credit = hidden.copy()  # identity continuation with a hidden terminal loss
    close(m, "same_prefix_quotient", hidden @ w, np.zeros((2, 1)))
    m["identity_suffix_credit_gap"] = float(np.sum(suffix_credit * hidden))
    require(m["identity_suffix_credit_gap"] == 1, "formal suffix witness missing", m)
    zero_w = basis(np.zeros((3, 2)))
    require(zero_w.shape[1] == 0, "zero-credit empty quotient not respected", m)
    return m, "Passed boundary reproduction: zero coupling reduces the local envelope, but an arbitrary hidden terminal covector defeats a prefix-chosen proper quotient."


def r04_propagation_risk(rng):
    m = {}
    d, v, p, horizon = 3, 2, 2, 4
    fast0, slow0 = rng.normal(size=(d, v)), rng.normal(size=(d, v))
    bs, bf = rng.normal(size=(d * v, p)), rng.normal(size=(d * v, p))
    z = rng.normal(size=p)
    # Column-major vec is the source's interface contract.
    cs, cf = (bs @ z).reshape(d, v, order="F"), (bf @ z).reshape(d, v, order="F")
    keys = [rng.normal(size=d) for _ in range(horizon)]
    keys = [k / np.linalg.norm(k) for k in keys]
    values = [rng.normal(size=v) for _ in range(horizon)]
    decay = [np.diag(rng.uniform(0.5, 0.95, d)) for _ in range(horizon)]
    erase = [np.eye(d) - 0.4 * np.outer(k, k) for k in keys]
    aa = [e @ dd for e, dd in zip(erase, decay)]
    fast, changed_fast, changed_slow = fast0.copy(), fast0 - cf, slow0 + cs
    r, product = np.zeros((d, d)), np.eye(d)
    t_maps = []
    for j in range(horizon):
        def step(f, s):
            fd = decay[j] @ f
            return fd + 0.4 * np.outer(keys[j], values[j] - (fd + s).T @ keys[j])
        fast, changed_fast = step(fast, slow0), step(changed_fast, changed_slow)
        r = aa[j] @ r + erase[j] @ (np.eye(d) - decay[j])
        product = aa[j] @ product
        t = np.kron(np.eye(v), product) @ (bs - bf) + np.kron(np.eye(v), r) @ bs
        t_maps.append(t)
        close(m, f"interface_rollout_{j}", changed_fast + changed_slow - fast - slow0,
              (t @ z).reshape(d, v, order="F"))
    # Exact matched migration with no differential decay has no total effect.
    f, fc = fast0.copy(), fast0 - cs
    for j in range(horizon):
        f = f + 0.4 * np.outer(keys[j], values[j] - (f + slow0).T @ keys[j])
        fc = fc + 0.4 * np.outer(keys[j], values[j] - (fc + slow0 + cs).T @ keys[j])
    close(m, "no_decay_no_effect", fc + slow0 + cs, f + slow0)

    q = [rng.normal(size=d) for _ in range(horizon)]
    ll = [np.kron(np.eye(v), qi.reshape(1, -1)) @ ti for qi, ti in zip(q, t_maps)]
    residual = [rng.normal(size=v) for _ in range(horizon)]
    weights = [psd(rng, v, 0.2) for _ in range(horizon)]
    probs = np.array([0.1, 0.2, 0.3, 0.4])
    h0, lam = psd(rng, p, 0.8), 0.3
    gram = sum(pr * l.T @ w @ l for pr, l, w in zip(probs, ll, weights))
    linear = sum(pr * l.T @ w @ ri for pr, l, w, ri in zip(probs, ll, weights, residual))
    kk = gram + lam * h0
    optimal = -np.linalg.solve(kk, linear)
    # Direct stacked weighted least squares is a different calculation of the
    # minimizer and does not form the normal equations being tested.
    designs, rhs = [], []
    for pr, l, w, ri in zip(probs, ll, weights, residual):
        rootw = np.linalg.cholesky(w).T
        designs.append(np.sqrt(pr) * rootw @ l)
        rhs.append(-np.sqrt(pr) * rootw @ ri)
    designs.append(np.sqrt(lam) * np.linalg.cholesky(h0).T)
    rhs.append(np.zeros(p))
    ls_solution = np.linalg.lstsq(np.vstack(designs), np.concatenate(rhs), rcond=None)[0]
    close(m, "joint_risk_minimizer", optimal, ls_solution)

    def risk(action):
        return sum(pr * ((ri + l @ action) @ w @ (ri + l @ action) - ri @ w @ ri)
                   for pr, l, w, ri in zip(probs, ll, weights, residual)) + lam * action @ h0 @ action
    close(m, "direct_optimal_risk_change", risk(optimal), -linear @ np.linalg.solve(kk, linear))
    protect = np.array([[1.0, 0.3]])
    n = null_space(protect)
    protected = -n @ np.linalg.solve(n.T @ kk @ n, n.T @ linear)
    kkt = np.block([[kk, protect.T], [protect, np.zeros((1, 1))]])
    reference = np.linalg.solve(kkt, np.r_[-linear, 0.0])[:p]
    close(m, "protected_action_kkt", protected, reference)
    close(m, "protected_output", protect @ protected, np.zeros(1))
    m["optimal_risk_change"] = float(risk(optimal))
    m["representability_immediate_error"] = float(np.linalg.norm(cs - cf))
    return m, "Full fast/slow rollouts confirm the ordered migration interface; joint and protected quadratic actions match independent least-squares/KKT references."


def r04_survival_boundary(rng):
    m = {}
    s, c, lam = 0.65, 1.7, 0.07
    for probability in [0.2, s, 0.9]:
        def objective(z):
            prediction = s * c + (1 - s) * c * z
            return probability * (prediction - c) ** 2 + (1 - probability) * prediction ** 2 + lam * z ** 2
        analytic = np.clip((1 - s) * c * c * (probability - s) /
                           ((1 - s) ** 2 * c * c + lam), 0, 1)
        result = minimize_scalar(objective, bounds=(0, 1), method="bounded", options={"xatol": 1e-12})
        require(result.success, "bounded scalar reference did not converge", m)
        candidates = [0.0, 1.0, float(result.x)]
        direct = min(candidates, key=objective)
        close(m, f"threshold_action_p_{probability}", analytic, direct, atol=2e-7, rtol=2e-7)
        m[f"action_p_{probability}"] = float(analytic)
    # A declared correlated validity/horizon law reverses the factorized decision.
    probs = np.array([0.6, 0.4]); survives = np.array([0.9, 0.1]); valid = np.array([1.0, 0.0])
    joint_numerator = float(np.sum(probs * (1 - survives) * (valid - survives)))
    mean_s, mean_valid = float(probs @ survives), float(probs @ valid)
    naive_numerator = (1 - mean_s) * (mean_valid - mean_s)
    m["joint_migration_numerator"] = joint_numerator
    m["factorized_migration_numerator"] = naive_numerator
    require(joint_numerator < 0 < naive_numerator, "joint-law wrong-decision witness missing", m)
    naive_action = naive_numerator / ((1 - mean_s) ** 2 + lam)
    joint_risk = lambda z: float(np.sum(probs * ((survives + (1 - survives) * z - valid) ** 2
                                               - (survives - valid) ** 2)) + lam * z * z)
    m["naive_action_excess_risk_over_zero"] = joint_risk(naive_action)
    require(m["naive_action_excess_risk_over_zero"] > 0, "factorized action is not harmful in witness", m)
    return m, "Passed boundary reproduction: migration switches at p=s; independent mean validity/survival can prescribe a harmful positive migration under a correlated law."


def r06_survival_plasticity(rng):
    m = {}
    d, v, horizon = 4, 3, 5
    eta = np.linspace(0.35, 0.6, horizon)
    aa = []
    for j, margin in enumerate(eta):
        k = rng.normal(size=d); k /= np.linalg.norm(k)
        rho = (1 - margin) * 0.85
        a = np.eye(d) - rho * np.outer(k, k)
        aa.append(a)
        singular = np.linalg.svd(a, compute_uv=False)
        close(m, f"sigma_min_{j}", singular[-1], 1 - rho)
        close(m, f"sigma_max_{j}", singular[0], 1.0)
        s = rng.normal(size=(d, v)); target = rng.normal(size=v)
        before = target - s.T @ k
        after = target - delta(s, k, target, rho).T @ k
        close(m, f"current_key_residual_{j}", after, (1 - rho) * before)
        require(np.linalg.norm(after) + ATOL >= margin * np.linalg.norm(before), "plasticity floor violated", m)
    initial = np.outer(rng.normal(size=d), rng.normal(size=v))
    transported = initial.copy()
    for a in aa:
        transported = a @ transported
    ratio = np.linalg.norm(transported) / np.linalg.norm(initial)
    alpha = float(np.prod(eta))
    m.update(survival_ratio=float(ratio), certified_lower_ratio=alpha)
    require(alpha - ATOL <= ratio <= 1 + ATOL, "two-sided survival bound failed", m)
    unit = np.eye(d)[:, 0]
    endpoint = np.outer(unit, np.ones(v))
    aligned = endpoint.copy(); orthogonal = np.outer(np.eye(d)[:, 1], np.ones(v))
    for margin in eta:
        a = np.eye(d) - (1 - margin) * np.outer(unit, unit)
        aligned, orthogonal = a @ aligned, a @ orthogonal
    close(m, "aligned_lower_endpoint", np.linalg.norm(aligned) / np.linalg.norm(endpoint), alpha)
    close(m, "orthogonal_upper_endpoint", np.linalg.norm(orthogonal) / np.linalg.norm(endpoint), 1.0)
    # Sharp interval-model Kantorovich/PPS factor, with both KKT caps inactive.
    alpha = 0.2
    envelope = np.array([1 / (1 + alpha), alpha / (1 + alpha)])
    ratios = np.array([alpha, 1.0]); signal = envelope * ratios; budget = 0.25
    propensity = budget * envelope / envelope.sum()
    oracle = budget * signal / signal.sum()
    require(np.max(propensity) < 1 and np.max(oracle) < 1, "fixture activates PPS caps", m)
    actual = np.sum(signal ** 2 / propensity) / np.sum(signal ** 2 / oracle)
    bound = (1 + alpha) ** 2 / (4 * alpha)
    close(m, "sharp_allocation_factor", actual, bound)
    m["allocation_factor"] = float(actual)
    # d=1 and zero-key cases do not use the d>=2 maximum-eigenvalue shortcut.
    close(m, "scalar_dimension_norm", norm2(np.array([[0.4]])), 0.4)
    close(m, "zero_key_factor", np.eye(d) - 0.8 * np.outer(np.zeros(d), np.zeros(d)), np.eye(d))
    return m, "Rank-one singular values, direct current-key residuals and ordered products satisfy the two-sided certificate; both survival and allocation endpoint bounds are attained."


def r06_boundary(rng):
    m = {}
    k = np.array([1.0, 0.0]); overwrite = np.eye(2) - np.outer(k, k)
    close(m, "overwrite_annihilation", overwrite @ k, np.zeros(2))
    nonunit = 2 * k; beta = 0.2
    actual_margin = np.linalg.svd(np.eye(2) - beta * np.outer(nonunit, nonunit), compute_uv=False)[-1]
    m.update(actual_nonunit_margin=float(actual_margin), raw_beta_assumed_margin=1 - beta)
    require(actual_margin < 1 - beta - 0.1, "raw-beta normalization counterexample missing", m)
    singular_decay = np.diag([0.0, 1.0])
    capped_erase = np.eye(2) - 0.3 * np.outer(k, k)
    close(m, "singular_decay_destroys_survival", capped_erase @ singular_decay @ k, np.zeros(2))
    expansive = np.diag([2.0, 1.0])
    m["expansive_decay_survival_ratio"] = float(np.linalg.norm(capped_erase @ expansive @ k))
    require(m["expansive_decay_survival_ratio"] > 1, "expansive-decay envelope failure missing", m)
    return m, "Passed boundary reproduction: overwrite, nonunit keys, singular decay and expansive decay invalidate the unqualified margin/envelope extension."


def r07_factor_joint(rng):
    m = {}
    d, v, actions, horizon = 4, 3, 3, 3
    kfactor, efactor = rng.normal(size=(d, actions)), rng.normal(size=(v, actions))
    aa, bb = [], []
    for _ in range(horizon):
        key = rng.normal(size=d); key /= np.linalg.norm(key)
        aa.append((np.eye(d) - 0.4 * np.outer(key, key)) @ np.diag(rng.uniform(0.6, 0.95, d)))
        bb.append(rng.normal(size=(d, v)))
    s0 = rng.normal(size=(d, v)); action = rng.uniform(0.1, 0.9, actions)
    base, chosen, z = s0.copy(), s0 + kfactor @ np.diag(action) @ efactor.T, kfactor.copy()
    rho, reg = rng.normal(size=actions), psd(rng, actions, 0.1)
    linear, hessian = rho.copy(), reg.copy()
    direct_change = float(rho @ action + 0.5 * action @ reg @ action)
    for t in range(horizon + 1):
        q, y, w = rng.normal(size=d), rng.normal(size=v), psd(rng, v, 0.2)
        c = z.T @ q
        gamma = efactor @ np.diag(c)
        close(m, f"factor_memory_{t}", chosen - base, z @ np.diag(action) @ efactor.T)
        close(m, f"factor_read_{t}", chosen.T @ q - base.T @ q, gamma @ action)
        r = base.T @ q - y
        linear += gamma.T @ w @ r
        hadamard = np.outer(c, c) * (efactor.T @ w @ efactor)
        close(m, f"hadamard_gram_{t}", hadamard, gamma.T @ w @ gamma)
        hessian += hadamard
        new_r = chosen.T @ q - y
        direct_change += 0.5 * (new_r @ w @ new_r - r @ w @ r)
        if t < horizon:
            base, chosen, z = aa[t] @ base + bb[t], aa[t] @ chosen + bb[t], aa[t] @ z
    close(m, "joint_qp_vs_direct_rollout", direct_change, linear @ action + 0.5 * action @ hessian @ action)
    m["joint_hessian_minimum_eigenvalue"] = float(np.linalg.eigvalsh(hessian)[0])
    require(m["joint_hessian_minimum_eigenvalue"] >= -ATOL, "Gram Hessian is not PSD", m)
    # Identical response columns make independent gates overcorrect.
    h = np.array([[1.1, 1.0], [1.0, 1.1]]); g = -np.ones(2)
    joint = -np.linalg.solve(h, g); independent = -g / np.diag(h)
    direct_loss = lambda a: 0.5 * (a.sum() - 1) ** 2 + 0.05 * (a @ a)
    m["independent_gate_excess_loss"] = float(direct_loss(independent) - direct_loss(joint))
    close(m, "direct_joint_stationarity", np.full(2, joint.sum() - 1) + 0.1 * joint, np.zeros(2))
    require(m["independent_gate_excess_loss"] > 0.1, "cross-Hessian counterexample missing", m)
    return m, "Frozen affine response and Hadamard cross-Hessian match direct state/loss rollouts; independent scalar gates are worse on an explicit coupled-write fixture."


def r07_feedback_jacobian(rng):
    m = {}
    d, v, updater_width = 2, 2, 2
    width = d * v + updater_width
    def params(rows):
        return rng.normal(scale=0.25, size=(rows, width)), rng.normal(scale=0.2, size=rows)
    wk, bk = params(d); wv, bv = params(v); wb, bb = params(1); wd, bd = params(d)
    mu = rng.normal(scale=0.2, size=(updater_width, updater_width))
    ms = rng.normal(scale=0.2, size=(updater_width, d * v)); bu = rng.normal(scale=0.1, size=updater_width)
    x = rng.normal(scale=0.4, size=width)
    sigmoid = lambda z: 1 / (1 + np.exp(-z))

    def components(state):
        s, u = state[:d * v].reshape(d, v), state[d * v:]
        k, value = np.tanh(wk @ state + bk), np.tanh(wv @ state + bv)
        beta = float(sigmoid(wb @ state + bb)[0])
        decay_logit = wd @ state + bd
        decay = np.exp(-np.logaddexp(0, decay_logit))
        decayed = decay[:, None] * s
        residual = value - decayed.T @ k
        post = decayed + beta * np.outer(k, residual)
        next_u = np.tanh(mu @ u + ms @ post.ravel() + bu)
        return s, u, k, value, beta, decay_logit, decay, decayed, residual, post, next_u

    def full_map(state):
        *_, post, next_u = components(state)
        return np.r_[post.ravel(), next_u]

    s, u, key, value, beta, dl, decays, decayed, residual, post, next_u = components(x)
    columns = []
    for direction in np.eye(width):
        ds, du = direction[:d * v].reshape(d, v), direction[d * v:]
        dk = (1 - key * key) * (wk @ direction)
        dv = (1 - value * value) * (wv @ direction)
        dbeta = beta * (1 - beta) * float((wb @ direction)[0])
        ddecay = -decays * sigmoid(dl) * (wd @ direction)
        dz = decays[:, None] * ds + ddecay[:, None] * s
        de = dv - dz.T @ key - decayed.T @ dk
        dpost = dz + dbeta * np.outer(key, residual) + beta * np.outer(dk, residual) + beta * np.outer(key, de)
        dnext_u = (1 - next_u * next_u) * (mu @ du + ms @ dpost.ravel())
        columns.append(np.r_[dpost.ravel(), dnext_u])
    analytic = np.column_stack(columns)
    fd_errors = []
    for h in [1e-4, 1e-5, 1e-6]:
        error = np.linalg.norm(analytic - fd_jacobian(full_map, x, h))
        m[f"central_difference_error_h_{h}"] = float(error)
        fd_errors.append(float(error))
    require(max(fd_errors) < FD_TOL * max(1.0, norm2(analytic)), "complete feedback Jacobian disagrees with finite differences", m)
    frozen_a = (np.eye(d) - beta * np.outer(key, key)) @ np.diag(decays)
    frozen_memory = np.column_stack([(frozen_a @ e.reshape(d, v)).ravel() for e in np.eye(d * v)])
    m["actual_vs_frozen_memory_block_gap"] = float(np.linalg.norm(analytic[:d * v, :d * v] - frozen_memory))
    require(m["actual_vs_frozen_memory_block_gap"] > 1e-3, "fixture failed to expose coefficient-feedback paths", m)

    # Exact R07 sign reversal, evaluated through the actual Delta update rather
    # than by evaluating the paper's polynomial on both sides.
    true_next = lambda a: float(delta(np.array([[a]]), np.ones(1), np.ones(1), a)[0, 0])
    true_loss = lambda a: 0.5 * (a + 1.5) ** 2 + 0.5 * (true_next(a) - 1) ** 2
    frozen_loss = lambda a: 0.5 * (a + 1.5) ** 2 + 0.5 * (a - 1) ** 2
    h = 1e-6
    # One-sided derivative keeps the exact counterexample inside a in [0,1].
    derivative = (-3 * true_loss(0) + 4 * true_loss(h) - true_loss(2 * h)) / (2 * h)
    frozen_derivative = (-3 * frozen_loss(0) + 4 * frozen_loss(h) - frozen_loss(2 * h)) / (2 * h)
    close(m, "true_action_derivative", derivative, -0.5, atol=FD_TOL, rtol=FD_TOL)
    close(m, "frozen_action_derivative", frozen_derivative, 0.5, atol=FD_TOL, rtol=FD_TOL)
    action = 0.01
    m["true_small_action_loss_change"] = float(true_loss(action) - true_loss(0))
    m["frozen_small_action_loss_change"] = float(frozen_loss(action) - frozen_loss(0))
    require(m["true_small_action_loss_change"] < 0 < m["frozen_small_action_loss_change"], "feedback sign reversal missing", m)
    close(m, "true_polynomial_change", true_loss(action) - true_loss(0),
          -0.5 * action + 3.5 * action ** 2 - 2 * action ** 3 + 0.5 * action ** 4)
    return m, "Complete smooth memory+updater Jacobian, including state-dependent key/value/gate/decay and updater feedback, matches finite differences. Passed boundary reproduction: the frozen gate reverses the action decision."


def r09_gramian_carrier(rng):
    m = {}
    d, horizon = 5, 4
    aa = []; u = []; weights = rng.uniform(0.2, 1.0, horizon)
    for _ in range(horizon):
        key = rng.normal(size=d); key /= np.linalg.norm(key)
        aa.append((np.eye(d) - 0.4 * np.outer(key, key)) @ np.diag(rng.uniform(0.6, 0.95, d)))
        u.append(rng.normal(size=(d, 1)))
    p, gram, factors = np.eye(d), np.zeros((d, d)), []
    x = rng.normal(size=d); displacement = x.copy(); direct = 0.0
    for a, stage, weight in zip(aa, u, weights):
        p = a @ p; displacement = a @ displacement
        factor = np.sqrt(weight) * p.T @ stage
        factors.append(factor); gram += factor @ factor.T
        direct += weight * np.linalg.norm(stage.T @ displacement) ** 2
    close(m, "transported_gramian_energy", direct, x @ gram @ x)
    carrier = basis(np.hstack(factors))
    close(m, "factor_gramian_range", carrier @ carrier.T, basis(gram) @ basis(gram).T)
    key, gamma, mu = rng.normal(size=d), 0.7, 0.3
    core = carrier.T @ gram @ carrier
    perpendicular = key - carrier @ (carrier.T @ key)
    y = carrier @ np.linalg.solve(mu * np.eye(carrier.shape[1]) + core, carrier.T @ key) + perpendicular / mu
    reduced = gamma * y / (key @ y)
    reference = constrained_quadratic(gram + mu * np.eye(d), key.reshape(1, -1), np.array([gamma]))
    close(m, "core_inverse_action", reduced, reference)
    # Projection reduction for an explicit ambiguous family with proper carrier.
    v = np.eye(d)[:, :2]; family = [v @ np.diag([4.0, 1.0]) @ v.T, v @ np.diag([1.0, 4.0]) @ v.T]
    current_key = np.array([1.0, 1.0, 0.0, 0.0, 1.0])
    w = basis(np.column_stack([v, current_key]))
    trial = rng.normal(size=d); projected = w @ w.T @ trial
    close(m, "robust_projection_constraint", current_key @ trial, current_key @ projected)
    for i, g in enumerate(family):
        close(m, f"robust_projection_damage_{i}", trial @ g @ trial, projected @ g @ projected)
        require(projected @ (g + mu * np.eye(d)) @ projected <= trial @ (g + mu * np.eye(d)) @ trial + ATOL,
                "projecting outside span(k,V) increased robust risk", m)
    m["realized_carrier_width"] = carrier.shape[1]
    m["proper_robust_action_span_width"] = w.shape[1]
    return m, "Transported factors reproduce direct protected-read energy; range, core inverse action and robust projection reduction agree with ambient references."


def r09_boundary(rng):
    m = {}
    d, beta = 4, 0.6
    q = np.ones(d); factors, grams = [], []
    for i in range(d):
        k = np.eye(d)[:, i]; a = np.eye(d) - beta * np.outer(k, k)
        z = a.T @ q; factors.append(z); grams.append(np.outer(z, z))
    zz = np.column_stack(factors)
    close(m, "rank_one_family_factor_matrix", zz, np.ones((d, d)) - beta * np.eye(d))
    m["realized_gramian_ranks"] = [rank(g) for g in grams]
    m["common_carrier_width"] = rank(zz)
    require(m["realized_gramian_ranks"] == [1] * d and rank(zz) == d,
            "realized-rank-one/common-full-width witness missing", m)
    key = np.ones(2)
    g1, g2 = np.diag([0.1, 4.0]), np.diag([4.0, 0.1])
    actions = [constrained_quadratic(g + 0.2 * np.eye(2), key.reshape(1, -1), np.ones(1)) for g in [g1, g2]]
    m["same_carrier_different_core_action_gap"] = float(np.linalg.norm(actions[0] - actions[1]))
    require(m["same_carrier_different_core_action_gap"] > 0.5, "carrier-only anisotropy ambiguity missing", m)
    return m, "Passed boundary reproduction: every realized Gramian has rank one while the prefix-robust carrier is full; a known carrier alone leaves the action unidentified."


def r10_carrier_leakage(rng):
    m = {}
    d, r, v, horizon = 5, 2, 2, 4
    u = np.eye(d)[:, :r]; p = u @ u.T; identity = np.eye(d)
    coordinates = rng.normal(size=(r, v)); residual = u @ coordinates + 0.1 * rng.normal(size=(d, v))
    initial_error = residual - u @ coordinates; error = initial_error.copy()
    bound = norm2(error); factors, defects = [], []
    for t in range(horizon):
        decay = np.diag(rng.uniform(0.5, 0.8, d)); key = rng.normal(size=d); key /= np.linalg.norm(key)
        beta = 0.4; a = (identity - beta * np.outer(key, key)) @ decay
        core = u.T @ a @ u; leakage = (identity - p) @ a @ u
        formula = u.T @ decay @ u - beta * np.outer(u.T @ key, key @ decay @ u)
        close(m, f"ordered_core_{t}", core, formula)
        close(m, f"leakage_norm_{t}", norm2(leakage), beta * np.linalg.norm((identity - p) @ key) * np.linalg.norm(key @ decay @ u))
        injection = 0.15 * rng.normal(size=(d, v)); old_coordinates = coordinates.copy()
        defect = leakage @ old_coordinates + (identity - p) @ injection
        residual = a @ residual + injection
        coordinates = core @ coordinates + u.T @ injection
        error = a @ error + defect
        close(m, f"direct_error_recurrence_{t}", residual - u @ coordinates, error)
        bound = norm2(a) * bound + norm2(leakage) * norm2(old_coordinates) + norm2((identity - p) @ injection)
        require(norm2(error) <= bound + ATOL, "carrier error norm certificate failed", m)
        factors.append(a); defects.append(defect)
    unrolled = ordered_product(factors, d) @ initial_error
    for i, defect in enumerate(defects):
        unrolled += ordered_product(factors[i + 1:], d) @ defect
    close(m, "variation_of_constants", error, unrolled)
    m["final_error_operator_norm"] = norm2(error); m["final_error_norm_bound"] = float(bound)
    # Positive control: invariant carrier and carrier-valued injections are exact.
    c = rng.normal(size=(r, v)); full = u @ c
    for _ in range(3):
        key = u @ rng.normal(size=r); key /= np.linalg.norm(key)
        a = (identity - 0.3 * np.outer(key, key)) @ np.diag(rng.uniform(0.6, 0.9, d))
        injection = u @ rng.normal(size=(r, v))
        full, c = a @ full + injection, u.T @ a @ u @ c + u.T @ injection
    close(m, "invariant_exact_carrier", full, u @ c)
    return m, "Ordered Delta carrier/leakage and error recurrences match full residual propagation; zero leakage plus carrier-valued injections yields exact compression."


def r10_boundary(rng):
    m = {}
    d, beta, offset = 4, 0.4, 0.2
    seed = np.ones(d); aa, keys = [], []
    for i in range(d):
        key = np.eye(d)[:, i] + offset * np.ones(d); key /= np.linalg.norm(key)
        keys.append(key); aa.append(np.eye(d) - beta * np.outer(key, key))
    m["one_step_invariant_hull_width"] = rank(np.column_stack([seed] + [a @ seed for a in aa]))
    m["key_family_width"] = rank(np.column_stack(keys))
    m["noncommuting_factor_gap"] = float(np.linalg.norm(aa[0] @ aa[1] - aa[1] @ aa[0]))
    require(m["one_step_invariant_hull_width"] == d and m["noncommuting_factor_gap"] > 0.01,
            "noncommuting full-width invariant-hull witness missing", m)
    x = np.array([[0.2, 0.4], [0.4, 0.8]])
    quantized = np.rint(x); defect = x - quantized
    m["prequantization_rank"] = rank(x); m["new_defect_rank"] = rank(defect)
    close(m, "quantization_defect_determinant", np.linalg.det(defect), -0.2)
    require(rank(x) == 1 and rank(defect) == 2, "elementwise new-defect rank increase missing", m)
    return m, "Passed boundary reproduction: a noncommuting rank-one Delta family forces full carrier width, and rank-one data can inject rank-two elementwise quantization defects."


def r11_overlay_order(rng):
    m = {}
    d, v, r = 4, 3, 2
    s = rng.normal(size=(d, v)); left, right = rng.normal(size=(d, r)), rng.normal(size=(v, r))
    base, corrected = s.copy(), s + left @ right.T
    for t in range(4):
        key = rng.normal(size=d); key /= np.linalg.norm(key); value = rng.normal(size=v); beta = 0.4
        correction = left @ right.T
        close(m, f"corrected_residual_{t}", value - corrected.T @ key,
              value - base.T @ key - correction.T @ key)
        base, corrected = delta(base, key, value, beta), delta(corrected, key, value, beta)
        left = left - beta * np.outer(key, key @ left)
        close(m, f"lazy_overlay_{t}", corrected - base, left @ right.T)
        require(rank(left @ right.T) <= r, "passive overlay rank grew", m)
    ki, kj = np.array([1., 0., 0., 0.]), np.array([1., 1., 0., 0.])
    vi, vj = rng.normal(size=v), rng.normal(size=v); bi, bj = 0.4, 0.3
    ai, aj = np.eye(d) - bi * np.outer(ki, ki), np.eye(d) - bj * np.outer(kj, kj)
    plus = lambda state: delta(delta(state, ki, vi, bi), kj, vj, bj)
    minus = lambda state: delta(delta(state, kj, vj, bj), ki, vi, bi)
    gap = plus(s) - minus(s)
    ei, ej = vi - s.T @ ki, vj - s.T @ kj
    explicit = bi * bj * (ki @ kj) * (np.outer(ki, ej) - np.outer(kj, ei))
    close(m, "two_write_order_gap", gap, explicit)
    existing = rng.normal(size=(d, v)); matrix_gap = aj @ ai - ai @ aj
    close(m, "corrected_prestate_gap", plus(s + existing) - minus(s + existing), gap + matrix_gap @ existing)
    selector_mean, observed_sign = 0.2, -1.0
    edit = (selector_mean - observed_sign) / 2
    actual = minus(s + existing) + edit * (plus(s + existing) - minus(s + existing)) - minus(s)
    average = (aj @ ai + ai @ aj) / 2
    expected = (average + selector_mean * matrix_gap / 2) @ existing + edit * gap
    close(m, "repeated_order_edit", actual, expected)
    naive = ai @ aj @ existing + edit * gap
    close(m, "omitted_MC_term", actual - naive, edit * matrix_gap @ existing)
    m["naive_independent_injection_error"] = float(np.linalg.norm(actual - naive))
    require(m["naive_independent_injection_error"] > 1e-3, "corrected-prestate order dependence missing", m)
    return m, "Lazy overlays match dense common-path differences; direct adjacent Delta writes verify the order-gap factor and the consequential corrected-prestate MC term."


def r11_rank_boundary(rng):
    m = {}
    d = v = 4; accumulated = np.zeros((d, v))
    for block in range(2):
        ki = np.eye(d)[:, 2 * block]; kj = ki + np.eye(d)[:, 2 * block + 1]
        vi, vj = -np.eye(v)[:, 2 * block + 1], np.eye(v)[:, 2 * block]
        zero = np.zeros((d, v))
        gap = delta(delta(zero, ki, vi, 1), kj, vj, 1) - delta(delta(zero, kj, vj, 1), ki, vi, 1)
        local = gap[2 * block:2 * block + 2, 2 * block:2 * block + 2]
        close(m, f"genuine_gap_block_{block}", local, np.array([[1., 1.], [0., 1.]]))
        require(rank(gap) == 2, "genuine pair gap is not rank two", m)
        accumulated += gap
    m["accumulated_rank"] = rank(accumulated)
    require(m["accumulated_rank"] == 4, "two-gap cumulative rank boundary failed", m)
    u, singular, vh = np.linalg.svd(accumulated, full_matrices=False)
    approximate = (u[:, :2] * singular[:2]) @ vh[:2]
    close(m, "rank_two_unavoidable_tail", np.linalg.norm(accumulated - approximate) ** 2, np.sum(singular[2:] ** 2))
    m["rank_two_tail_energy"] = float(np.sum(singular[2:] ** 2))
    require(m["rank_two_tail_energy"] > 0.1, "rank-two truncation did not lose a genuine gap", m)
    protected = np.eye(d)[:, :2]
    projected = protected @ protected.T @ accumulated
    close(m, "protected_query_minimum_rank", projected.T @ protected, accumulated.T @ protected)
    m["protected_query_required_rank"] = rank(projected)
    shared_right = rng.normal(size=v)
    shared = sum(np.outer(rng.normal(size=d), shared_right) for _ in range(8))
    require(rank(shared) == 1, "shared-right injections failed to remain rank one", m)
    return m, "Passed boundary reproduction: two actual disjoint Delta order gaps attain rank four and a positive rank-two tail, while many shared-right injections retain rank one."


def graph_carrier(keys, protected):
    gram = keys.T @ keys
    selected = set(np.flatnonzero(np.any(protected.T @ keys != 0, axis=0)).tolist())
    frontier = list(selected)
    while frontier:
        i = frontier.pop()
        for j in np.flatnonzero(gram[i] != 0):
            if int(j) not in selected:
                selected.add(int(j)); frontier.append(int(j))
    return basis(np.column_stack([protected, keys[:, sorted(selected)]])), sorted(selected)


def r12_gram_closure(rng):
    m = {}
    d, v = 6, 2; eye = np.eye(d)
    keys = np.column_stack([eye[:, 0], eye[:, 0] + eye[:, 1], eye[:, 1] + eye[:, 2],
                            eye[:, 3], eye[:, 3] + eye[:, 4], eye[:, 5]])
    protected = eye[:, :1]
    u, selected = graph_carrier(keys, protected)
    # Independent least-fixed-point iteration uses full operators, no graph.
    fixed = basis(protected)
    for _ in range(d + 1):
        expanded = basis(np.column_stack([fixed] + [(eye - 0.2 * np.outer(k, k)) @ fixed for k in keys.T]))
        if expanded.shape[1] == fixed.shape[1]:
            fixed = expanded; break
        fixed = expanded
    close(m, "graph_vs_operator_fixed_point", u @ u.T, fixed @ fixed.T)
    m["selected_components_vertices"] = selected; m["least_carrier_width"] = u.shape[1]
    require(selected == [0, 1, 2] and u.shape[1] == 3, "finite-family graph certificate wrong", m)
    s = rng.normal(size=(d, v)); y = u.T @ s
    for t, index in enumerate([0, 3, 1, 4, 2, 5, 0, 2]):
        key, value, beta = keys[:, index], rng.normal(size=v), 0.2
        h = u.T @ key
        s = delta(s, key, value, beta)
        y = y - beta * np.outer(h, h @ y) + beta * np.outer(h, value)
        close(m, f"autonomous_reduced_state_{t}", y, u.T @ s)
        close(m, f"protected_decoder_{t}", (u.T @ protected).T @ y, protected.T @ s)
    return m, "Graph components match an independent full-operator invariant fixed point; the autonomous reduced recurrence exactly reproduces full protected reads for the declared dictionary."


def r12_bridge_boundary(rng):
    m = {}
    e1, e2 = np.eye(2).T
    first = delta(np.zeros((2, 1)), e2, np.array([1.0]), 1.0)
    second = delta(np.zeros((2, 1)), e2, np.array([-1.0]), 1.0)
    close(m, "same_retained_prefix", e1 @ first, e1 @ second)
    bridge = e1 + e2
    first_after = delta(first, bridge, np.zeros(1), 0.5)
    second_after = delta(second, bridge, np.zeros(1), 0.5)
    gap = float((e1 @ first_after - e1 @ second_after)[0])
    m["future_bridge_protected_read_gap"] = gap
    require(abs(gap) > 0.5, "discarded write did not become observable through the bridge", m)
    u, _ = graph_carrier(np.column_stack([e2, bridge]), e1[:, None])
    require(u.shape[1] == 2, "bridge family did not enlarge closure to full width", m)
    eps = 1e-8; near = eps * e1 + e2
    u, selected = graph_carrier(np.column_stack([e1, near]), e1[:, None])
    leakage = norm2(np.outer(e1, e1) @ (np.eye(2) - 0.5 * np.outer(near, near)) @ np.outer(e2, e2))
    m["nonzero_small_edge"] = eps; m["threshold_discarded_cross_operator_norm"] = leakage
    require(u.shape[1] == 2 and selected == [0, 1] and leakage > 1e-12,
            "nonzero-edge threshold boundary missing", m)
    return m, "Passed boundary reproduction: an unseen bridge reveals already discarded history; treating a small nonzero Gram edge as zero loses exact closure."


def r13_minimum_ledger(rng):
    m = {}
    d, v, p = 4, 3, 3
    key = rng.normal(size=d); key /= np.linalg.norm(key)
    decay = np.diag([0.9, 0.6, 0.8, 0.7])
    a = (np.eye(d) - np.outer(key, key)) @ decay
    b = np.outer(key, rng.normal(size=v)); q = rng.normal(size=(d, p)); c0 = rng.normal(size=(p, v))
    n = null_space(a, rcond=RANK_TOL)
    require(n.shape[1] == 1, "overwrite kernel is not one dimensional", m)
    expected_n = np.linalg.solve(decay, key); expected_n /= np.linalg.norm(expected_n)
    close(m, "ordered_overwrite_kernel", n @ n.T, np.outer(expected_n, expected_n))
    uu, singular, vh = np.linalg.svd(q.T @ n, full_matrices=False)
    ell = rank(q.T @ n)
    l = n @ vh[:ell].T; kdecoder = uu[:, :ell] * singular[:ell]
    remainder = q.T - kdecoder @ l.T
    xdecoder = remainder @ np.linalg.pinv(a, rcond=RANK_TOL)
    offset = c0 - xdecoder @ b
    close(m, "minimum_ledger_coefficients", xdecoder @ a + kdecoder @ l.T, q.T)
    for t in range(3):
        s = rng.normal(size=(d, v)); post = a @ s + b; ledger = l.T @ s
        close(m, f"affine_ledger_recovery_{t}", xdecoder @ post + kdecoder @ ledger + offset, q.T @ s + c0)
    invisible = n @ rng.normal(size=(1, v))
    close(m, "same_poststate_without_ledger", a @ invisible, np.zeros((d, v)))
    m["no_ledger_protected_ambiguity"] = float(np.linalg.norm(q.T @ invisible))
    require(m["no_ledger_protected_ambiguity"] > 0.1, "erased protected quotient witness missing", m)
    projection = n @ n.T; erased = q.T @ projection
    no_ledger_coefficients = q.T - (q.T @ np.linalg.pinv(a, rcond=RANK_TOL)) @ a
    close(m, "zero_budget_optimal_tail", np.linalg.norm(no_ledger_coefficients), np.linalg.norm(erased))
    m["minimum_side_rows"] = ell
    m["cross_column_minimum_scalars"] = rank(np.kron(np.eye(v), q.T @ n))
    require(ell == 1 and m["cross_column_minimum_scalars"] == v, "minimum ledger scalar count wrong", m)
    return m, "The minimal lost-coordinate ledger recovers full affine protected targets; the overwritten kernel, insufficient-budget tail and cross-column scalar lower bound match independent ambient calculations."


def r13_spectral_boundary(rng):
    m = {}
    a = np.diag([1e-3, 0.7, 0.9]); q = np.eye(3); tau = 0.05
    w, singular, vh = np.linalg.svd(a); v = vh.T; high = singular >= tau
    x = q.T @ v[:, high] @ np.diag(1 / singular[high]) @ w[:, high].T
    low = q.T @ (np.eye(3) - v[:, high] @ v[:, high].T)
    close(m, "spectral_cut_exact_hybrid", x @ a + low, q.T)
    m.update(exact_kernel_side_width=3 - rank(a), stable_cut_side_width=rank(low),
             exact_no_ledger_decoder_norm=norm2(np.linalg.inv(a)), stable_decoder_norm=norm2(x),
             stable_decoder_norm_bound=norm2(q) / tau)
    require(m["exact_kernel_side_width"] == 0 and m["stable_cut_side_width"] == 1 and norm2(x) <= norm2(q) / tau + ATOL,
            "spectral-cut state/conditioning distinction missing", m)
    state = rng.normal(size=(3, 2)); noise = 1e-4 * rng.normal(size=(3, 2))
    close(m, "stable_hybrid_state", x @ (a @ state) + low @ state, state)
    amplification = norm2(x @ noise)
    require(amplification <= norm2(x) * norm2(noise) + ATOL, "decoded noise bound failed", m)
    z = np.ones((2, 1)); a1, a2 = np.diag([0.5, 1.0]), np.diag([1.0, 0.5])
    s1, s2 = np.linalg.solve(a1, z), np.linalg.solve(a2, z)
    close(m, "hidden_modes_same_poststate", a1 @ s1, a2 @ s2)
    m["hidden_mode_protected_target_gap"] = float(abs(s1[0, 0] - s2[0, 0]))
    require(m["hidden_mode_protected_target_gap"] == 1, "hidden realized-mode ambiguity missing", m)
    inverse_factor = np.diag([2.0, 1.0]); grown = np.array([1.0, 0.0]); fixed = np.array([0.0, 1.0])
    for _ in range(8):
        grown, fixed = inverse_factor @ grown, inverse_factor @ fixed
    close(m, "switching_orthogonal_fixed_covector", fixed, np.array([0.0, 1.0]))
    m["parallel_inverse_transport_growth"] = float(np.linalg.norm(grown))
    require(m["parallel_inverse_transport_growth"] == 256, "inverse-covector growth missing", m)
    return m, "Passed boundary reproduction: an invertible near-overwrite needs no exact ledger yet has large inverse amplification; spectral-cut storage trades state for stability, and hidden modes prevent a common decoder."


def flow_factors(lam, key, tau):
    generator = lam + np.outer(key, key)
    a, e = expm(-tau * lam), expm(-tau * generator)
    eigenvalues, vectors = np.linalg.eigh(generator)
    phi = np.full_like(eigenvalues, tau)
    nonzero = np.abs(eigenvalues) > 1e-14
    phi[nonzero] = -np.expm1(-tau * eigenvalues[nonzero]) / eigenvalues[nonzero]
    f = vectors @ (phi * (vectors.T @ key))
    return a, e, f


def r16_scan(rng):
    m = {}
    d, r, v, horizon = 5, 2, 3, 4
    u = np.eye(d)[:, :r]; p = u @ u.T; aa, ee, ff, values = [], [], [], []
    for j in range(horizon):
        lam = block_diag(psd(rng, r, 0.1), np.diag(rng.uniform(0.1, 0.6, d - r)))
        key = u @ rng.normal(size=r); tau = 0.1 + 0.05 * j
        a, e, f = flow_factors(lam, key, tau)
        # Constant-input ODE solved by a lifted exponential independently checks
        # the spectral p_tau evaluation, including its affine source.
        augmented = np.zeros((d + 1, d + 1)); augmented[:d, :d] = -(lam + np.outer(key, key)); augmented[:d, d] = key
        lifted = expm(tau * augmented)
        close(m, f"flow_source_lifted_ode_{j}", f, lifted[:d, d])
        close(m, f"two_sided_common_support_{j}", e - a, p @ (e - a) @ p)
        aa.append(a); ee.append(e); ff.append(f); values.append(rng.normal(size=v))
    initial = rng.normal(size=(d, v)); sequential = initial.copy()
    for e, f, val in zip(ee, ff, values):
        sequential = e @ sequential + np.outer(f, val)

    # A chunk is (complement action, carrier core, carrier affine source).
    chunks = [(a @ (np.eye(d) - p), u.T @ e @ u, np.outer(u.T @ f, val))
              for a, e, f, val in zip(aa, ee, ff, values)]
    def combine(later, earlier):
        return later[0] @ earlier[0], later[1] @ earlier[1], later[1] @ earlier[2] + later[2]
    left = combine(chunks[3], combine(chunks[2], combine(chunks[1], chunks[0])))
    balanced = combine(combine(chunks[3], chunks[2]), combine(chunks[1], chunks[0]))
    for i in range(3):
        close(m, f"affine_scan_associativity_{i}", left[i], balanced[i])
    scan = balanced[0] @ initial + u @ (balanced[1] @ u.T @ initial + balanced[2])
    close(m, "shared_carrier_scan_vs_sequential", scan, sequential)
    actual_product, base_product = ordered_product(ee, d), ordered_product(aa, d)
    telescope, dual, left_factors, right_factors = np.zeros((d, d)), np.zeros((d, d)), [], []
    for j in range(horizon):
        correction = ee[j] - aa[j]
        qs, ep = ordered_product(aa[j + 1:], d), ordered_product(ee[:j], d)
        es, qp = ordered_product(ee[j + 1:], d), ordered_product(aa[:j], d)
        telescope += qs @ correction @ ep; dual += es @ correction @ qp
        us, singular, vh = np.linalg.svd(correction, full_matrices=False)
        keep = singular > RANK_TOL
        lf, rf = us[:, keep] * singular[keep], vh[keep].T
        left_factors.append(qs @ lf); right_factors.append(ep.T @ rf)
    close(m, "ordered_product_telescope", actual_product - base_product, telescope)
    close(m, "dual_product_telescope", actual_product - base_product, dual)
    close(m, "lazy_product_factor_ledger", actual_product - base_product,
          np.hstack(left_factors) @ np.hstack(right_factors).T)
    # Transported recompression error for the contractive natural flow.
    exact, approximate, baseline, bound = np.zeros((d, d)), np.zeros((d, d)), np.eye(d), 0.0
    for j in range(horizon):
        previous_error = exact - approximate
        exact = ee[j] @ exact + (ee[j] - aa[j]) @ baseline
        proposed = ee[j] @ approximate + (ee[j] - aa[j]) @ baseline
        us, singular, vh = np.linalg.svd(proposed, full_matrices=False)
        next_approximate = np.outer(us[:, 0] * singular[0], vh[0])
        discarded = proposed - next_approximate
        close(m, f"recompression_error_transport_{j}", exact - next_approximate,
              ee[j] @ previous_error + discarded)
        approximate, baseline = next_approximate, aa[j] @ baseline
        bound += float(np.linalg.norm(discarded))
    m["recompressed_product_error"] = float(np.linalg.norm(exact - approximate))
    m["discarded_tail_sum_bound"] = bound
    require(m["recompressed_product_error"] <= bound + ATOL, "natural-flow recompression bound failed", m)
    return m, "Shared-carrier affine scans agree with sequential lifted-ODE flow for different chunkings; ordered telescopes/factor ledger and transported recompression identities agree with dense products."


def r16_rank_boundary(rng):
    m = {}
    d, horizon = 5, 4; aa, ee, sources = [], [], []
    for j in range(horizon):
        a, e, f = flow_factors(np.zeros((d, d)), np.eye(d)[:, j], 0.2 + 0.1 * j)
        aa.append(a); ee.append(e); sources.append(f)
        require(rank(e - a) == 1, "orthogonal flow correction is not rank one", m)
    m["one_token_maximum_correction_rank"] = 1
    m["chunk_correction_rank"] = rank(ordered_product(ee, d) - np.eye(d))
    m["affine_source_carrier_width"] = rank(np.column_stack(sources))
    require(m["chunk_correction_rank"] == horizon and m["affine_source_carrier_width"] == horizon,
            "one-token/cumulative-width counterexample missing", m)
    u = np.eye(3)[:, :1]; p = u @ u.T
    lam = np.array([[1.0, 0.3, 0.0], [0.3, 1.0, 0.0], [0.0, 0.0, 1.0]])
    a, e, f = flow_factors(lam, u[:, 0], 0.4)
    m["nonreducing_decay_outside_correction"] = float(np.linalg.norm((np.eye(3) - p) @ (e - a)))
    m["nonreducing_decay_outside_source"] = float(np.linalg.norm((np.eye(3) - p) @ f))
    require(m["nonreducing_decay_outside_correction"] > 1e-3 and m["nonreducing_decay_outside_source"] > 1e-3,
            "failure of shared reducing carrier was not observable", m)
    return m, "Passed boundary reproduction: rank-one token corrections accumulate to width H; a key inside U is insufficient when the symmetric decay does not reduce U."


def r18_fiber_energy(rng):
    m = {}
    n, threatened, kept = 5, 3, 1
    a = np.diag([1., 1., 0., 0., 0.]); k = np.eye(n)[:, 2:]; entrance = psd(rng, n, 0.1)
    ledger = basis(rng.normal(size=(threatened, kept))); unpreserved = null_space(ledger.T)
    projector = np.eye(threatened) - ledger @ ledger.T; radius = 1.4
    grams = []; traces = []
    for path in range(3):
        transitions = [rng.normal(scale=0.15, size=(n, n)) + 0.6 * np.eye(n) for _ in range(3)]
        reads = [rng.normal(size=(2, n)) for _ in range(3)]
        weights = rng.uniform(0.2, 0.9, 3)
        transport = entrance @ k; zrows = []
        for j, (transition, read, weight) in enumerate(zip(transitions, reads, weights)):
            zrows.append(np.sqrt(weight) * read @ transport)
            transport = transition @ transport  # read precedes this edge's transition
        z = np.vstack(zrows); gram = z.T @ z
        grams.append(gram); traces.append((transitions, reads, weights))
        _, singular, vh = np.linalg.svd(z @ unpreserved, full_matrices=False)
        alpha = radius * unpreserved @ vh[0]
        close(m, f"same_augmented_fiber_post_{path}", a @ k @ alpha, np.zeros(n))
        close(m, f"same_augmented_fiber_ledger_{path}", ledger.T @ alpha, np.zeros(kept))
        difference = entrance @ k @ alpha; direct = 0.0
        for transition, read, weight in zip(transitions, reads, weights):
            direct += weight * np.linalg.norm(read @ difference) ** 2
            difference = transition @ difference
        spectral = radius ** 2 * np.linalg.eigvalsh(projector @ gram @ projector)[-1]
        close(m, f"attained_fiber_energy_{path}", direct, spectral)
        close(m, f"independent_restricted_svd_{path}", spectral, radius ** 2 * singular[0] ** 2)
    envelope = sum(grams)
    eigenvalues, vectors = np.linalg.eigh(envelope)
    common = vectors[:, -kept:]; residual_projector = np.eye(threatened) - common @ common.T
    worst = max(float(np.linalg.eigvalsh(residual_projector @ g @ residual_projector)[-1]) for g in grams)
    certificate = float(eigenvalues[-kept - 1])
    require(worst <= certificate + ATOL, "common PSD-envelope certificate failed", m)
    for i, g in enumerate(grams):
        require(np.linalg.eigvalsh(envelope - g)[0] >= -ATOL, "chosen sum envelope does not dominate a path", m)
    m.update(common_ledger_worst_leakage=worst, common_envelope_tail_certificate=certificate,
             pairwise_radius=radius, full_ledger_residual_leakage=0.0)
    full = np.eye(threatened)
    close(m, "full_ledger_zero_residual_projector", np.eye(threatened) - full @ full.T, np.zeros((threatened, threatened)))
    return m, "Actual paired continuation rollouts attain the residual-fiber spectral maximum, independently checked by a restricted SVD; a sum-Gramian envelope safely upper-bounds the common ledger."


def r18_boundary(rng):
    m = {}
    ga, gb = np.diag([1., 0.]), np.diag([0., 1.]); envelope = np.eye(2)
    angle = np.pi / 4; direction = np.array([-np.sin(angle), np.cos(angle)])
    attained = max(direction @ ga @ direction, direction @ gb @ direction)
    angles = np.linspace(0, np.pi, 2049)
    direct_grid = np.maximum(np.sin(angles) ** 2, np.cos(angles) ** 2)
    close(m, "complementary_paths_robust_optimum", attained, 0.5)
    close(m, "angular_reference_minimum", float(np.min(direct_grid)), 0.5)
    m.update(path_specific_rank_one_tail_lower_bound=0.0, robust_common_rank_one_minimum=float(attained),
             envelope_rank_one_tail=float(np.linalg.eigvalsh(envelope)[0]))
    require(m["envelope_rank_one_tail"] > attained + 0.4, "envelope/robust-optimum distinction missing", m)
    # A pair of individually unit-radius coefficients has pairwise radius two.
    first, second = direction, -direction
    pair = first - second
    energy1 = max(direction @ ga @ direction, direction @ gb @ direction)
    energy2 = max(pair @ ga @ pair, pair @ gb @ pair)
    close(m, "pairwise_radius_energy_scaling", energy2, 4 * energy1)
    m["individual_unit_radius_pair_energy"] = float(energy2)
    require(energy2 > energy1, "individual-vs-pairwise-radius boundary missing", m)
    # State-dependent values can re-encode a component a frozen overwrite erases.
    complete = lambda s: float(delta(np.array([[s]]), np.ones(1), np.array([s]), 1.0)[0, 0])
    h = 1e-6
    close(m, "state_dependent_value_map_derivative", (complete(h) - complete(-h)) / (2 * h), 1.0,
          atol=FD_TOL, rtol=FD_TOL)
    m["frozen_overwrite_memory_derivative"] = 0.0
    return m, "Passed boundary reproduction: pathwise tail zero is insufficient for a common ledger; the envelope bound is conservative, pairwise radius matters, and state-dependent values invalidate a frozen overwrite kernel."


def r20_transfer(rng):
    m = {}
    n, constraints, sketch_rank = 6, 2, 2
    a = rng.normal(size=(constraints, n)); e = np.array([0.8, -0.2])
    z = rng.normal(scale=0.4, size=(n, sketch_rank)); lam = 0.4
    hhat = lam * np.eye(n) + z @ z.T
    x0 = a.T @ np.linalg.solve(a @ a.T, e)
    null = null_space(a); projector = null @ null.T
    projected = x0 - projector @ z @ np.linalg.solve(lam * np.eye(sketch_rank) + z.T @ projector @ z, z.T @ x0)
    reference = constrained_quadratic(hhat, a, e)
    close(m, "projected_woodbury_vs_dense_kkt", projected, reference)
    close(m, "projected_action_feasibility", a @ projected, e)
    ew, ev = np.linalg.eigh(hhat); root = (ev * np.sqrt(ew)) @ ev.T
    eigenbasis, _ = np.linalg.qr(rng.normal(size=(n, n)))
    lower, upper = 0.5, 1.8
    generalized = eigenbasis @ np.diag(np.linspace(lower, upper, n)) @ eigenbasis.T
    future = root @ generalized @ root
    actual = constrained_quadratic(future, a, e)
    ratio = float((projected @ future @ projected) / (actual @ future @ actual))
    bound = (upper + lower) ** 2 / (4 * upper * lower)
    m.update(random_future_risk_ratio=ratio, sharp_competitive_bound=bound)
    require(1 - ATOL <= ratio <= bound + ATOL, "relative spectral-transfer bound failed", m)
    # Sharp one-constraint endpoint cases and symmetric-delta form.
    unit = np.ones(2) / np.sqrt(2)
    for delta_radius in [0.0, 0.1, 0.6, 0.95]:
        future = np.diag([1 - delta_radius, 1 + delta_radius])
        oracle = constrained_quadratic(future, unit.reshape(1, -1), np.ones(1))
        ratio = float((unit @ future @ unit) / (oracle @ future @ oracle))
        close(m, f"sharp_delta_factor_{delta_radius}", ratio, 1 / (1 - delta_radius ** 2))
    zero = constrained_quadratic(hhat, a, np.zeros(constraints))
    close(m, "zero_target_action", zero, np.zeros(n))
    m["zero_target_ratio"] = "undefined_0_over_0; action equality checked"
    return m, "Projected Woodbury matches a dense KKT solve; independently solved future quadratics obey the spectral transfer bound, with equality at the two-dimensional sharp endpoints."


def r20_boundary(rng):
    m = {}
    constraint = np.array([[1.0, 0.0]]); target = np.ones(1); eps = 0.1; b = 3.0
    hhat = np.eye(2); future = np.array([[b * b + eps, b], [b, 1.0]])
    prefix = constrained_quadratic(hhat, constraint, target)
    oracle = constrained_quadratic(future, constraint, target)
    close(m, "difference_space_curvature_match", np.array([0., 1.]) @ future @ np.array([0., 1.]), 1.0)
    ratio = (prefix @ future @ prefix) / (oracle @ future @ oracle)
    close(m, "base_tangent_cross_term_risk_ratio", ratio, (b * b + eps) / eps)
    m["difference_only_certificate_risk_ratio"] = float(ratio)
    # Identical prefix sketch with an unconstrained future outside its span.
    z = np.array([[1.0], [0.0]]); regularizer = 1.0
    surrogate = regularizer * np.eye(2) + z @ z.T
    unseen = np.array([0.0, 1.0]); rho, claimed_delta = 4.0, 0.2
    alternate = surrogate + rho * np.outer(unseen, unseen)
    relative = np.diag([1 / np.sqrt(2), 1.0]) @ alternate @ np.diag([1 / np.sqrt(2), 1.0])
    m["same_prefix_relative_future_maximum"] = float(np.linalg.eigvalsh(relative)[-1])
    m["prefix_claimed_relative_upper_bound"] = 1 + claimed_delta
    require(m["same_prefix_relative_future_maximum"] > 1 + claimed_delta,
            "unrestricted same-prefix spectral premise failure missing", m)
    # Matching curvature does not constrain an omitted linear term or a finite
    # nonlinear excursion. Direct function values reproduce both boundaries.
    linear_loss = lambda u: 0.5 * (u - b) ** 2
    m["matching_curvature_linear_term_regret"] = float(linear_loss(0) - linear_loss(b))
    nonlinear = lambda u: b * (1 - u ** 3) ** 2 + 0.5 * u ** 2
    h = 1e-3
    curvature = (nonlinear(h) + nonlinear(-h) - 2 * nonlinear(0)) / h ** 2
    close(m, "matching_local_nonlinear_curvature", curvature, 1.0, atol=1e-5, rtol=1e-5)
    m["nonlinear_zero_action_loss"] = float(nonlinear(0)); m["nonlinear_finite_action_loss"] = float(nonlinear(1))
    require(m["matching_curvature_linear_term_regret"] > 0 and nonlinear(0) > nonlinear(1),
            "loss-class boundary witnesses missing", m)
    return m, "Passed boundary reproduction: a ker(A)-only sandwich misses base/tangent coupling; the same prefix cannot certify an unrestricted future, and matching curvature alone controls neither linear terms nor finite nonlinear edits."


CHECKS = [
    ("A01", "R01", "affine_credit_identity_and_minimal_right_quotient", "3-4,7", r01_transport),
    ("A02", "R01", "boundary_reproduction_zero_coupling_and_prefix_hidden_credit", "5-6", r01_boundary),
    ("A03", "R04", "frozen_fast_slow_interfaces_and_joint_risk", "2-3", r04_propagation_risk),
    ("A04", "R04", "boundary_reproduction_survival_threshold_and_correlated_law", "4-5", r04_survival_boundary),
    ("A05", "R06", "finite_horizon_survival_plasticity_and_sharp_allocation", "2-4", r06_survival_plasticity),
    ("A06", "R06", "boundary_reproduction_overwrite_normalization_and_decay", "5", r06_boundary),
    ("A07", "R07", "frozen_joint_response_and_cross_hessian", "2-3", r07_factor_joint),
    ("A08", "R07", "complete_feedback_jacobian_fd_and_frozen_sign_reversal", "5-6", r07_feedback_jacobian),
    ("A09", "R09", "transported_gramian_carrier_and_inverse_action", "2-4", r09_gramian_carrier),
    ("A10", "R09", "boundary_reproduction_realized_rank_one_common_full_width", "5-6", r09_boundary),
    ("A11", "R10", "invariant_core_leakage_and_error_transport", "2-4", r10_carrier_leakage),
    ("A12", "R10", "boundary_reproduction_noncommuting_hull_and_quantized_defect", "5-6", r10_boundary),
    ("A13", "R11", "lazy_overlay_adjacent_order_gap_and_corrected_prestate", "2-4", r11_overlay_order),
    ("A14", "R11", "boundary_reproduction_sharp_cumulative_rank_and_tail", "5", r11_rank_boundary),
    ("A15", "R12", "graph_certificate_operator_fixedpoint_and_autonomous_reads", "2-4", r12_gram_closure),
    ("A16", "R12", "boundary_reproduction_future_bridge_and_small_nonzero_edge", "6-7", r12_bridge_boundary),
    ("A17", "R13", "minimum_erasure_ledger_exact_decoder_and_rank_tail", "2-3,5", r13_minimum_ledger),
    ("A18", "R13", "boundary_reproduction_spectral_cut_hidden_mode_inverse_growth", "4,6-7", r13_spectral_boundary),
    ("A19", "R16", "shared_carrier_affine_scan_telescope_and_recompression", "2,4-5,7", r16_scan),
    ("A20", "R16", "boundary_reproduction_cumulative_width_and_nonreducing_decay", "3,6", r16_rank_boundary),
    ("A21", "R18", "paired_fiber_rollout_spectral_equality_and_psd_envelope", "1-3", r18_fiber_energy),
    ("A22", "R18", "boundary_reproduction_common_path_gap_radius_and_reencoding", "3-5", r18_boundary),
    ("A23", "R20", "projected_woodbury_kkt_and_sharp_spectral_transfer", "1-3", r20_transfer),
    ("A24", "R20", "boundary_reproduction_wrong_domain_prefix_and_loss_class", "4-6", r20_boundary),
]


def serializable(value):
    if isinstance(value, dict):
        return {str(k): serializable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serializable(v) for v in value]
    if isinstance(value, np.ndarray):
        return serializable(value.tolist())
    if isinstance(value, np.generic):
        return serializable(value.item())
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=20261012)
    args = parser.parse_args()
    start = time.perf_counter()
    manifest_bytes = (ROOT / "source_manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    pinned = {item["path"]: item["sha256"] for item in manifest["sources"]}
    seeds = np.random.SeedSequence(args.seed).spawn(len(CHECKS))
    records = []
    for (check_id, lineage, scope, sections, function), seed in zip(CHECKS, seeds):
        source_path = "source_snapshots/repairs/" + SOURCE_NAMES[lineage]
        record = {"id": check_id, "lineage": lineage, "scope": scope, "status": "failed", "metrics": {},
                  "source_refs": [{"path": source_path, "sha256": pinned.get(source_path), "sections": sections}],
                  "interpretation": ""}
        try:
            actual_hash = hashlib.sha256((ROOT / source_path).read_bytes()).hexdigest()
            require(source_path in pinned and actual_hash == pinned[source_path],
                    "pinned source bytes differ from exact source manifest", {"actual_source_sha256": actual_hash})
            metrics, interpretation = function(np.random.default_rng(seed))
            record.update(status="passed", metrics=serializable(metrics), interpretation=interpretation)
        except DiagnosticFailure as exc:
            record.update(metrics=serializable(exc.metrics), interpretation="Unexpected diagnostic failure: " + str(exc))
        except Exception as exc:
            record.update(metrics={"exception_type": type(exc).__name__, "traceback": traceback.format_exc()},
                          interpretation="Unexpected implementation exception: " + str(exc))
        records.append(record)
    result = {"suite": "delta_pinned_algebra_fp64_v1", "seed": args.seed, "checks": records,
              "elapsed_seconds": time.perf_counter() - start,
              "source_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
              "source_commit": manifest.get("commit"), "dtype": "float64",
              "tolerances": {"absolute": ATOL, "relative": RTOL, "finite_difference": FD_TOL, "rank": RANK_TOL},
              "evidence_scope": "Synthetic numerical theorem diagnostics and boundary reproduction; no language-model/native efficacy, superiority, novelty, causal prefix coverage, or deployment claim."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(serializable(result), ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"suite": result["suite"], "seed": args.seed,
                      "passed": sum(r["status"] == "passed" for r in records),
                      "failed": sum(r["status"] == "failed" for r in records), "output": str(args.output)}))
    return 1 if any(r["status"] == "failed" for r in records) else 0


if __name__ == "__main__":
    raise SystemExit(main())
