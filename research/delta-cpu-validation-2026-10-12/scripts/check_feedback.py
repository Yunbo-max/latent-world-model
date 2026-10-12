"""Constructed Delta diagnostics; these are not language-model benchmark results."""
import argparse
import json
from pathlib import Path
import time
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def run(seed):
    rng = np.random.default_rng(seed)
    checks, profiles = [], []
    # This declared feedback reads S[0,0] to gate a subsequent e2 write.
    # Both branches have the same exogenous k,v; the gate is state-dependent.
    def rollout(beta, gamma=1.0):
        s = np.zeros((2, 1))
        s[0, 0] = beta
        immediate = s[1, 0]
        gate = sigmoid(gamma * s[0, 0])
        s[1, 0] += gate * (1.0 - s[1, 0])
        return immediate, s[1, 0]
    rows = []
    for gamma in [0.0, 0.1, 1.0, 4.0]:
        _, baseline = rollout(0.0, gamma)
        for beta in [0.0, 0.1, 0.5, 1.0]:
            immediate, later = rollout(beta, gamma)
            rows.append(dict(gamma=gamma, beta=beta, immediate_damage=immediate**2,
                             later_damage=(later-baseline)**2,
                             new_write_residual=(1-beta)**2))
    witness = next(r for r in rows if r['gamma'] == 1.0 and r['beta'] == 1.0)
    # Implement distinct decision rules on the declared witness. The oracle is
    # deliberately given the future analytic response,so it is an audit control.
    budget=.01;local_score=0.0
    local_beta=1.0 if local_score==0 else min(1.0,np.sqrt(budget/local_score))
    oracle_beta=min(1.,np.log((.5+np.sqrt(budget))/(.5-np.sqrt(budget))))
    arms=[]
    for name,b in [('no-write',0.),('ordinary-Delta',1.),('local-protection-gate',local_beta),('future-informed-audit-control',oracle_beta)]:
        immediate,later=rollout(b,1.)
        arms.append(dict(arm=name,beta=float(b),immediate_damage=float(immediate**2),later_damage=float((later-.5)**2),new_write_residual=float((1-b)**2),information='declared prefix/local' if name!='future-informed-audit-control' else 'extra future analytic response;not deployable'))
    checks.append(dict(id='feedback.actual-four-arm-audit',lineage='R03',scope='four declared rules on the constructed two-step witness',
        status='passed' if arms[2]['later_damage']>budget and arms[3]['later_damage']<=budget+1e-12 else 'failed',
        metrics=dict(budget=budget,arms=arms),source_refs=['repairs/R03_WASSERSTEIN_FREE_RUNNING_SAFETY.v3.md'],
        interpretation='The implemented local-only rule violates a later budget in this witness. The future-informed audit control is charged as extra information and is not a same-information method superiority comparison.'))
    checks.append(dict(id='feedback.local-zero-later-positive', lineage='R03', scope='constructed two-step scalar-gate Delta counterexample',
        status='passed' if witness['immediate_damage'] == 0.0 and witness['later_damage'] > 0.01 else 'failed',
        metrics=dict(witness=witness, grid=rows), source_refs=['repairs/R03_WASSERSTEIN_FREE_RUNNING_SAFETY.v3.md'],
        interpretation='A zero local protected displacement does not certify zero later displacement when a later gate reads the edited state. This refutes only the local-to-global extension.'))
    beta, gamma, h = 0.3, 1.7, 1e-5
    finite = (rollout(beta+h, gamma)[1]-rollout(beta-h, gamma)[1])/(2*h)
    g = sigmoid(gamma*beta)
    analytic = gamma*g*(1-g)
    error = abs(finite-analytic)
    checks.append(dict(id='feedback.future-gate-derivative', lineage='STEP2',scope='complete two-step output sensitivity versus frozen gate',
        status='passed' if error < 1e-8 and analytic > 0.1 else 'failed',
        metrics=dict(finite_difference=finite,complete_derivative=analytic,frozen_derivative=0.0,absolute_error=error,step=h),
        source_refs=['STEP2_COUPLED_UPDATER_STABILITY.md'],interpretation='Finite differences detect the gate-feedback term missed by a frozen future gate.'))
    for dk, dv in [(8,16), (16,32), (32,32)]:
        k = rng.normal(size=dk); k /= np.linalg.norm(k)
        e = rng.normal(size=dv); G = rng.normal(size=(dk,dv))/10
        beta = .4; A = np.eye(dk)-beta*np.outer(k,k); K = np.outer(k,e)
        X = rng.normal(size=(dk,dv))
        def factor():
            return A@X+K*np.sum(G*X)
        def dense():
            J = np.kron(A,np.eye(dv))+np.outer(K.ravel(),G.ravel())
            return (J@X.ravel()).reshape(dk,dv)
        reference = dense(); actual = factor()
        rel = np.linalg.norm(reference-actual)/max(1.,np.linalg.norm(reference))
        checks.append(dict(id=f'feedback.matrixfree-{dk}x{dv}',lineage='R01',scope='same declared linearized Delta gate map',
            status='passed' if rel < 1e-12 else 'failed',metrics=dict(relative_error=float(rel),dk=dk,dv=dv),
            source_refs=['repairs/R01_TRANSPORTED_CREDIT_QUOTIENT.v3.md'],interpretation='Agreement with an explicitly formed Jacobian in C-order coordinates; not a new algorithm claim.'))
        # Warm both paths; pair and randomize order, retain every timing.
        factor(); dense()
        timings=[]
        for repetition in range(7):
            order=['factor','dense']; rng.shuffle(order); row={'repetition':repetition,'order':order}
            for arm in order:
                t=time.perf_counter(); result=factor() if arm=='factor' else dense(); row[arm+'_seconds']=time.perf_counter()-t
                row[arm+'_norm']=float(np.linalg.norm(result))
            timings.append(row)
        profiles.append(dict(dk=dk,dv=dv,scope='construct plus apply one declared Jacobian; not complete training or quotient basis construction',
            factor_stored_bytes=int(A.nbytes+K.nbytes+G.nbytes+X.nbytes),dense_jacobian_bytes=int((dk*dv)**2*8),
            relative_error=float(rel),timings=timings,interpretation='Exploratory single-thread timings on a shared host; contention remains possible. Dense explicit Jacobian is an independent reference, not the strongest reverse-mode baseline.'))
    return checks, profiles


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--seed',type=int,default=0);args=ap.parse_args()
    t=time.perf_counter();checks,profiles=run(args.seed)
    result=dict(suite='feedback',seed=args.seed,checks=checks,profiles=profiles,elapsed_seconds=time.perf_counter()-t,
                data_kind='constructed mathematical diagnostic',language_model_or_novelty_claim=False)
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'checks':len(checks),'failed':sum(c['status']=='failed' for c in checks),'output':str(path)}))
    raise SystemExit(1 if any(c['status']=='failed' for c in checks) else 0)
