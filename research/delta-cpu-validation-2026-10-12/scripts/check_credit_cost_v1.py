"""Same-path Delta tangent cost audit against batched matrix-free JVP/VJP.

Declared reachable value carrier only; fixed exogenous keys/targets, state-dependent
scalar gate. Future paths are supplied equally to every arm: this is an offline
development audit, not a prefix predictor or a native language-model benchmark.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np


def sigmoid(x):
    return 1. / (1. + np.exp(-x))


def fixture(d, v, r, n, objectives, horizon, seed):
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(v, r))
    basis = np.linalg.qr(raw, mode='reduced')[0]
    initial = rng.normal(size=(d, v)) * .1
    state = initial.copy()
    inputs = []
    # Choose the nominal target using the nominal state, then store it as fixed
    # exogenous data. Perturbed rollouts NEVER recompute targets from their state.
    for _ in range(horizon):
        key = rng.normal(size=d); key /= np.linalg.norm(key)
        gate_weight = rng.normal(size=(d, v)) / np.sqrt(d * v)
        offset = float(rng.normal(scale=.1))
        decay = .97
        pre = decay * state
        beta = sigmoid(float(np.sum(gate_weight * pre)) + offset)
        target = pre.T @ key + basis @ rng.normal(size=r)
        residual = target - pre.T @ key
        state = pre + beta * np.outer(key, residual)
        inputs.append((key, gate_weight, offset, decay, target))
    start_keys = rng.normal(size=(n, d))
    start_keys /= np.linalg.norm(start_keys, axis=1)[:, None]
    start_values = rng.normal(size=(n, r))
    x0 = start_keys[:, :, None] * (start_values @ basis.T)[:, None, :]
    credits = rng.normal(size=(objectives, d, v)) / np.sqrt(d * v)
    return dict(raw_basis=raw, inputs=inputs, initial=initial, x0=x0, credits=credits,
                basis=basis, d=d, v=v, r=r, n=n, objectives=objectives, horizon=horizon, seed=seed)


def trace(f, initial=None):
    state = f['initial'].copy() if initial is None else initial.copy()
    stages = []
    for key, g, offset, decay, target in f['inputs']:
        pre = decay * state
        beta = sigmoid(float(np.sum(g * pre)) + offset)
        e = target - pre.T @ key
        stages.append((key, g, decay, beta, beta * (1-beta), e))
        state = pre + beta * np.outer(key, e)
    return stages, state


def jvp(stages, x):
    x = x.copy()
    for k, g, decay, beta, derivative, e in stages:
        dx = decay * x
        key_read = np.einsum('d,ndv->nv', k, dx)
        gate_read = derivative * np.einsum('dv,ndv->n', g, dx)
        x = dx - beta * k[None, :, None] * key_read[:, None, :]
        x += gate_read[:, None, None] * k[None, :, None] * e[None, None, :]
    return x


def vjp(stages, z):
    z = z.copy()
    for k, g, decay, beta, derivative, e in reversed(stages):
        key_read = np.einsum('d,mdv->mv', k, z)
        write_read = derivative * np.einsum('d,v,mdv->m', k, e, z)
        z = decay * (z - beta * k[None, :, None] * key_read[:, None, :]
                     + write_read[:, None, None] * g[None, :, :])
    return z


def project(f, stages):
    # Account the prefix basis QR again in the compressed path: conservative
    # additional construction cost, rather than a free suffix-derived basis.
    basis = np.linalg.qr(f['raw_basis'], mode='reduced')[0]
    projected = [(k, g @ basis, decay, beta, derivative, e @ basis)
                 for k, g, decay, beta, derivative, e in stages]
    start = f['x0'] @ basis
    credits = f['credits'] @ basis
    return basis, projected, start, credits


def path(f, arm):
    stages, state = trace(f)  # common complete memory forward is charged to all.
    if arm == 'direct_jvp':
        values = np.einsum('mdv,ndv->mn', f['credits'], jvp(stages, f['x0']))
    elif arm == 'direct_vjp':
        values = np.einsum('mdv,ndv->mn', vjp(stages, f['credits']), f['x0'])
    else:
        basis, reduced, start, credits = project(f, stages)
        if arm == 'core_jvp':
            values = np.einsum('mdv,ndv->mn', credits, jvp(reduced, start))
        elif arm == 'core_vjp':
            values = np.einsum('mdv,ndv->mn', vjp(reduced, credits), start)
        else:
            raise ValueError(arm)
    return values, state


def run():
    checks, profiles = [], []
    source = 'source_snapshots/repairs/R01_TRANSPORTED_CREDIT_QUOTIENT.v3.md'
    def add(cid, metrics, ok, text):
        checks.append(dict(id=cid, lineage='R01', scope='same fixed-path constructed Delta credit diagnostic',
                           status='passed' if ok else 'failed', metrics=metrics, source_refs=[source], interpretation=text))
    cases = [(32, 16, 3, 1, 1, 8), (64, 32, 4, 4, 4, 12), (128, 32, 4, 16, 16, 12),
             (64, 32, 4, 16, 1, 12), (64, 32, 4, 1, 16, 12)]
    arms = ['direct_jvp', 'direct_vjp', 'core_jvp', 'core_vjp']
    for ci, dims in enumerate(cases):
        f = fixture(*dims, seed=13000+ci)
        stages, _ = trace(f)
        values = {arm: path(f, arm)[0] for arm in arms}
        reference = values['direct_jvp']
        errors = {arm: float(np.linalg.norm(value-reference)/max(1.,np.linalg.norm(reference)))
                  for arm, value in values.items()}
        add(f'credit-cost.case-{ci}.four-arm-equality', {'dimensions':dims, 'relative_errors':errors},
            max(errors.values()) < 1e-11,
            'Batched direct JVP and adjoint VJP agree with both projected implementations for the declared reachable carrier. Memory remains full sized; no ambient-state quotient claim follows.')
        # Every raw randomized timing is retained. Timings are exploratory on a
        # shared host; no individual repeat is required to win.
        for arm in arms:path(f, arm)
        rng = np.random.default_rng(14000+ci)
        rows=[]
        for repeat in range(9):
            order=arms.copy();rng.shuffle(order);row={'repeat':repeat,'order':order}
            for arm in order:
                begin=time.perf_counter()
                for _ in range(3):out,state=path(f,arm)
                row[arm+'_seconds']=(time.perf_counter()-begin)/3
                row[arm+'_checksum']=float(out.sum()+state.sum())
            rows.append(row)
        medians={arm:float(np.median([row[arm+'_seconds'] for row in rows])) for arm in arms}
        # Additional projected-state and metadata footprint, not an equal-bit
        # preservation comparison. Both arms keep the same full Delta memory.
        _,reduced,start,credit=project(f,stages)
        core_bytes=f['basis'].nbytes+start.nbytes+credit.nbytes+sum(g.nbytes+e.nbytes for _,g,_,_,_,e in reduced)
        profiles.append(dict(case=ci,dimensions=dims,medians_seconds=medians,paired_raw_timings=rows,
            best_direct_seconds=min(medians['direct_jvp'],medians['direct_vjp']),
            best_core_seconds=min(medians['core_jvp'],medians['core_vjp']),
            best_core_over_best_direct_ratio=min(medians['core_jvp'],medians['core_vjp'])/min(medians['direct_jvp'],medians['direct_vjp']),
            full_delta_memory_bytes=f['initial'].nbytes,
            direct_direction_bytes=f['x0'].nbytes,direct_costate_bytes=f['credits'].nbytes,
            core_extra_arrays_bytes=core_bytes,
            common_input_arrays_bytes=f['x0'].nbytes+f['credits'].nbytes+sum(k.nbytes+g.nbytes+t.nbytes for k,g,_,_,t in f['inputs']),
            scope='Time includes full Delta replay,core basis QR and per-stage projection,all propagation and output contractions; fixture generation common and outside timing. Both strong direct orientations exposed; shared host is not timing-isolated.'))
    f=fixture(*cases[0],seed=13000);stages,nominal=trace(f);h=1e-5
    plus=trace(f,f['initial']+h*f['x0'][0])[1]
    minus=trace(f,f['initial']-h*f['x0'][0])[1]
    finite=np.einsum('mdv,dv->m',f['credits'],(plus-minus)/(2*h))
    analytic=path(f,'direct_jvp')[0][:,0]
    err=float(np.linalg.norm(finite-analytic)/max(1.,np.linalg.norm(analytic)))
    add('credit-cost.full-feedback-finite-difference',{'step':h,'relative_error':err},err<1e-8,
        'Perturbed rollouts retain fixed targets/keys but regenerate state-dependent gates; this validates complete scalar-gate feedback on the declared path only.')
    # Explicit proof witness for the distinction between reachable and ambient.
    adj=vjp(stages,f['credits'])[0];w=f['basis'];hidden=adj-(adj@w)@w.T
    hidden_credit=float(np.sum(adj*hidden));retained=float(np.linalg.norm(hidden@w))
    core_credit=float(np.sum((adj@w)*(hidden@w)))
    add('credit-cost.reachable-not-ambient-witness',
        {'discarded_tangent_quotient_norm':retained,'full_credit':hidden_credit,'quotient_credit':core_credit},
        retained<1e-12 and hidden_credit>1e-4 and abs(core_credit)<1e-12,
        'The carrier is exact only for declared reachable tangents; an omitted ambient perturbation has invisible quotient but nonzero credit. Full-state sufficiency is not established.')
    # Violating the residual-carrier premise creates a real propagation gap.
    k,g,decay,beta,derivative,e=stages[-1]
    off=np.eye(f['v'])[0]-(np.eye(f['v'])[0]@w)@w.T;off/=np.linalg.norm(off)
    broken=stages[:-1]+[(k,g,decay,beta,derivative,e+off)]
    basis,reduced,start,credits=project(f,broken)
    direct=np.einsum('mdv,ndv->mn',f['credits'],jvp(broken,f['x0']))
    clipped=np.einsum('mdv,ndv->mn',credits,jvp(reduced,start))
    gap=float(np.linalg.norm(direct-clipped))
    add('credit-cost.out-of-carrier-residual-failure',{'credit_gap':gap,'off_carrier_residual_norm':1.},gap>1e-6,
        'Exactness fails when a later residual leaves the declared carrier. This is an assumption failure,not a refutation of the conditional projection identity.')
    status=Path('/proc/self/status').read_text()
    threads=next(int(line.split()[1]) for line in status.splitlines() if line.startswith('Threads:'))
    return checks,profiles,threads


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();start=time.perf_counter()
    checks,profiles,threads=run()
    result=dict(suite='Delta-credit-cost-v1',checks=checks,profiles=profiles,observed_self_threads=threads,
        elapsed_seconds=time.perf_counter()-start,data_kind='constructed fixed-path development audit',
        limitations=['Not a deployed prefix-only critic,learned updater,native benchmark,LM or RSI result.',
          'Carrier is specified before fixture generation; full future path is equally supplied offline to all arms.',
          'No exclusive host reservation; median timing ratios are exploratory,not a population speedup claim.',
          'Full memory,common input traces and additional basis/projection buffers are disclosed;this is not matched-bit memory preservation.'])
    Path(a.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'checks':len(checks),'failed':sum(c['status']=='failed' for c in checks),
                      'cost_ratios':[p['best_core_over_best_direct_ratio'] for p in profiles]}))
    raise SystemExit(any(c['status']=='failed' for c in checks))
