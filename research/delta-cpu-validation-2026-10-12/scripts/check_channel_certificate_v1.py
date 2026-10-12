"""Finite likelihood worlds and certificate endpoints; constructed CPU diagnostics."""
import argparse
import json
from pathlib import Path
import numpy as np


def terminal_risk(kernel, prior=.5):
    # Rows: latent V=0,1; columns: observed symbol. Action0 loses V;
    # action1 loses1-V. Sum joint losses and optimize after each observation.
    joint = np.array([1-prior, prior])[:, None] * kernel
    return float(np.minimum(joint[1], joint[0]).sum())


def run():
    checks = []
    def add(cid, lineage, metrics, ok, interpretation):
        source = 'source_snapshots/repairs/' + ('R08_SHARP_CHANNEL_FREE_RELEASE.v3.md' if lineage == 'R08' else 'R17_RESIDUAL_SCALED_SPECTRAL_CERTIFICATE.v3.md')
        checks.append(dict(id=cid, lineage=lineage, source_refs=[source], status='passed' if ok else 'failed', metrics=metrics,
                           scope='constructed development diagnostic', interpretation=interpretation))
    keep = np.full((2, 2), .5)
    world_a_release = keep.copy()
    world_b_release = np.eye(2)
    # Behavior always keeps; log both observed Y and V-dependent keep loss.
    logged_a = .5 * keep
    logged_b = .5 * keep
    difference_a = .25 + terminal_risk(world_a_release) - terminal_risk(keep)
    difference_b = .25 + terminal_risk(world_b_release) - terminal_risk(keep)
    add('R08-v2.full-likelihood-two-worlds', 'R08',
        {'logged_joint_laws_equal': bool(np.array_equal(logged_a, logged_b)), 'joint_log_probabilities': logged_a.tolist(),
         'world_a_release_minus_keep': difference_a, 'world_b_release_minus_keep': difference_b},
        np.array_equal(logged_a, logged_b) and abs(difference_a-.25)<1e-14 and abs(difference_b+.25)<1e-14,
        'Two complete valid likelihood worlds have identical keep-only records,including observed keep loss,and opposite optimal unsupported release actions. Logging V does not identify an untried channel.')
    rho = .3
    channel = np.array([[1-rho, rho, 0], [1-rho, 0, rho]])
    joint = .5 * channel
    masses = joint.sum(axis=0)
    posterior = joint[1] / masses
    information = .5 - terminal_risk(channel)
    add('R08-v2.likelihood-mixture-bayes-plausibility', 'R08',
        {'posterior_values': posterior.tolist(), 'symbol_masses': masses.tolist(), 'posterior_mean': float(masses @ posterior), 'gross_information_value': information},
        abs(masses @ posterior-.5)<1e-14 and abs(information-rho*.5)<1e-14,
        'Explicit conditional kernels attain an intermediate EVSI rather than inserting an arbitrary posterior sample list.')
    differences = []
    for rho in [0., .2, .5, 1.]:
        shared = np.array([[1-rho,rho,0.],[1-rho,0.,rho]])
        differences.append(.25+terminal_risk(shared)-terminal_risk(shared))
    add('R08-v2.linked-channel-rectangular-gap', 'R08',
        {'shared_family_action_differences': differences, 'rectangular_outer_interval': [-.25,.75]},
        max(abs(x-.25) for x in differences)<1e-14,
        'When keep and release must share the same kernel and loss,information values cancel. Independently rectangular extremes are an outer bound,not a sharp identified set for this linked family.')
    u = np.diag([9.,2.,.25]);g=.5*u
    queries = np.diag(np.sqrt(np.diag(g)))
    k=np.array([.8,.6,0.]);e=np.array([3.,4.]);tau=.4
    rows=[]
    for rank in [0,1,3]:
        eigenvalues=np.diag(u)
        factor=np.zeros((3,rank))
        for j in range(rank):factor[j,j]=np.sqrt(eigenvalues[j])
        tail=0. if rank==3 else eigenvalues[rank]
        score=float(np.linalg.norm(factor.T@k)**2+tail*np.linalg.norm(k)**2)
        beta=min(1.,np.sqrt(tau/(np.linalg.norm(e)**2*score)))
        delta=beta*np.outer(k,e)
        direct_energy=float(np.linalg.norm(queries.T@delta)**2)
        bound=float(beta**2*np.linalg.norm(e)**2*score)
        rows.append(dict(rank=rank,tail=tail,score=score,beta=float(beta),direct_query_energy=direct_energy,certificate_bound=bound))
    add('R17-v2.rank-zero-full-and-low-endpoints','R17',{'cases':rows,'dense_score':float(k@u@k)},
        all(x['direct_query_energy']<=x['certificate_bound']+1e-12 and x['certificate_bound']<=tau+1e-12 for x in rows)
        and abs(rows[0]['score']-9)<1e-14 and abs(rows[-1]['score']-float(k@u@k))<1e-12,
        'Rank0 isotropic and full-rank zero-tail implementations preserve the conditional one-sided bound. U is a declared fixed certificate; no deployed prefix calibration is constructed.')
    dense=float(k@g@k);regularizer=.7
    beta=.23;h=1e-4
    energy=lambda b:float(np.linalg.norm(queries.T@(b*np.outer(k,e)))**2)
    objective=lambda b:float(np.linalg.norm(e-b*e)**2+regularizer*energy(b))
    curvature=(objective(beta+h)-2*objective(beta)+objective(beta-h))/h**2
    exact_curvature=2*np.linalg.norm(e)**2*(1+regularizer*dense)
    add('R17-v2.actual-energy-versus-objective-curvature','R17',
        {'direct_energy':energy(beta),'gram_energy':float(beta**2*np.linalg.norm(e)**2*dense),'objective_curvature_fd':float(curvature),
         'objective_curvature_exact':float(exact_curvature),'energy_coefficient':float(np.linalg.norm(e)**2*dense)},
        abs(energy(beta)-beta**2*np.linalg.norm(e)**2*dense)<1e-12 and abs(curvature-exact_curvature)/exact_curvature<1e-6,
        'Interference energy and scalar fit-plus-interference objective curvature have distinct factors and units; a certificate score alone is not the full objective Hessian.')
    return checks


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks=run()
    Path(args.output).write_text(json.dumps(dict(suite='channel-certificate-v1',data_kind='constructed mathematical diagnostic',checks=checks,
        limitations=['No real logged channel identified;no prefix calibration or native score.', 'No causal transition of latent validity or nonlinear continuation tested.']),indent=2,allow_nan=False)+'\n')
    print(json.dumps({'checks':len(checks),'failed':sum(c['status']=='failed' for c in checks)}))
    raise SystemExit(any(c['status']=='failed' for c in checks))
