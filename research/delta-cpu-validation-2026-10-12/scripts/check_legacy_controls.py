"""Independent small-matrix checks of retained historical Delta controls."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.linalg import expm, sqrtm


def run(seed):
    rng=np.random.default_rng(seed);checks=[]
    def add(id,metric,ok,source,interpretation,claim_status='numerically_supported'):
        checks.append(dict(id=id,lineage='historical/control',scope='constructed mathematical diagnostic',status='passed' if ok else 'failed',metrics=metric,source_refs=[source],interpretation=interpretation,claim_status=claim_status))
    k=rng.normal(size=5);k/=np.linalg.norm(k);a=.7*k+rng.normal(size=5)*.2
    c=float(k@a);s=float(np.linalg.norm(a-c*k));B=np.array([[1-c,-s],[0,1.]])
    A=np.eye(5)-np.outer(k,a);sv=np.linalg.svd(A,compute_uv=False)
    eig=np.linalg.eigvalsh(B.T@B);formula=np.sqrt(max(eig));err=abs(sv[0]-max(1.,formula))
    add('legacy.oblique-exact-singular-values',{'error':err,'norm':float(sv[0])},err<1e-12 and sv[0]>1,'rejected/NOGO_OBLIQUE_03.md','The independent2D block and full SVD agree; bare oblique erase expands.')
    w=np.array([1.,.2]);r=np.array([.6,1.]);c=float(r@w);e=w/np.linalg.norm(w);a=c/np.linalg.norm(w)**2;b=(r-(r@e)*e)/np.linalg.norm(w);P=np.eye(2)-np.outer(e,e)
    H=a*np.outer(e,e)+np.outer(e,b)+np.outer(b,e)+np.outer(b,b)/a+2*P;A=np.eye(2)-np.outer(w,r)
    slack=H-A.T@H@A;reference=(2-c)*np.outer(r,r)
    err=np.linalg.norm(slack-reference)
    add('legacy.spd-nondegenerate-certificate',{'slack_error':float(err),'min_eigen_H':float(np.linalg.eigvalsh(H)[0]),'min_eigen_slack':float(np.linalg.eigvalsh(slack)[0])},err<1e-12 and np.linalg.eigvalsh(H)[0]>0 and np.linalg.eigvalsh(slack)[0]>-1e-12,'rejected/LYAPUNOV_OBLIQUE_METRIC.md','Nonzero w,r with0<c<=2 support the scoped construction.')
    # The archived iff omits zero-factor identity degeneracies.
    w=np.zeros(2);r=np.array([1.,0.]);A=np.eye(2)-np.outer(w,r);H=np.eye(2);c=float(r@w)
    exists=np.linalg.norm(H-A.T@H@A)==0.0;printed_condition=0<c<=2
    add('legacy.spd-zero-factor-assumption-gap',{'certificate_exists':bool(exists),'stated_c_condition':bool(printed_condition),'c':c,'slack_norm':float(np.linalg.norm(H-A.T@H@A))},exists and not printed_condition,'rejected/LYAPUNOV_OBLIQUE_METRIC.md','Concrete boundary counterexample to an unqualified iff. Repair: handle wr^T=0 separately,or explicitly require both factors nonzero.','archived_statement_needs_degeneracy_clause')
    k=np.array([1.,0.]);beta=.4;D=np.diag([.8,.3]);A=np.eye(2)-beta*np.outer(k,k);S=rng.normal(size=(2,3));v=rng.normal(size=3)
    # Same-key gap is in chronology of affine writes,even when matrices commute.
    v1=rng.normal(size=3);v2=rng.normal(size=3)
    forward=A@(A@S+beta*np.outer(k,v1))+beta*np.outer(k,v2)
    reverse=A@(A@S+beta*np.outer(k,v2))+beta*np.outer(k,v1)
    gap=beta**2*np.outer(k,v2-v1)
    err=np.linalg.norm(forward-reverse-gap)
    add('legacy.affine-write-order-gap',{'formula_error':float(err),'gap_norm':float(np.linalg.norm(gap))},err<1e-12 and np.linalg.norm(gap)>1e-4,'rejected/AFFINE_MAGNUS_COMMUTATOR_CONTROL.md','Commuting homogeneous factors do not make affine writes commute.')
    tau=.7;key=np.array([1.,.4]);target=np.array([.2,-.3,.8]);state=rng.normal(size=(2,3));kk=float(key@key)
    exact=expm(-tau*np.outer(key,key))@state+(1-np.exp(-tau*kk))/kk*np.outer(key,target)
    delta=state+(1-np.exp(-tau*kk))/kk*np.outer(key,target-state.T@key)
    err=np.linalg.norm(exact-delta)
    add('legacy.exact-flow-delta-equivalence',{'error':float(err)},err<1e-12,'rejected/EXACT_FLOW_IMPLICIT_DELTA_CONTROL.md','Matrix exponential integration and scalar-gated Delta agree on a frozen local target.')
    contraction=np.array([[.6]]);aux=np.sqrt(1-.6**2);U=np.array([[.6,aux],[aux,-.6]]);z=np.array([1.,0.]);first=U@z;second=U@first
    add('legacy.unitary-reused-slot',{'first_primary':float(first[0]),'second_primary':float(second[0]),'intended_second':.36},abs(first[0]-.6)<1e-12 and abs(second[0]-.36)>.5,'rejected/NOGO_UNITARY_DILATION.md','Reusing the same auxiliary slot returns erased content; a one-step unitary dilation does not reproduce all powers.')
    k=rng.normal(size=4);e=rng.normal(size=3);q=rng.normal(size=4);c=rng.normal(size=2);r=rng.normal(size=2)
    u=np.kron(k,c);query=np.kron(q,r);actual=(query@u)*e;expected=(q@k)*(r@c)*e
    add('legacy.tensor-address-interference',{'error':float(np.linalg.norm(actual-expected))},np.linalg.norm(actual-expected)<1e-12,'rejected/PROVENANCE_TENSOR_DELTA.md','Direct tensor addressing matches product interference; added provenance coordinates are not free.')
    Q=np.eye(2);S=rng.normal(size=(2,3));A=np.diag([.5,.9]);W=rng.normal(size=(2,3));direct=A@(S+W);rollback=direct-A@W;reference=A@S
    add('legacy.frozen-affine-rollback',{'error':float(np.linalg.norm(rollback-reference))},np.linalg.norm(rollback-reference)<1e-12,'rejected/RETROACTIVE_ROLLBACK_DELTA.md','Transported subtraction restores the no-write branch only for the common affine path.')
    # D01 two common-affine branches are representable by a low-rank difference.
    S=rng.normal(size=(3,2));k=rng.normal(size=3);e=rng.normal(size=2);W=np.outer(k,e);A=rng.normal(size=(3,3));B=rng.normal(size=(3,2));p=.3
    mixture=p*(A@(S+W)+B)+(1-p)*(A@S+B);compressed=A@S+B+p*np.outer(A@k,e)
    add('D01.shared-affine-mixture',{'error':float(np.linalg.norm(mixture-compressed))},np.linalg.norm(mixture-compressed)<1e-12,'cards/D01.json','Exact common-path mixture identity,not evidence of novelty.')
    # D03 normalized inverse-metric edit versus independently solved KKT system.
    P=rng.normal(size=(3,3));G=P.T@P+np.eye(3);k=rng.normal(size=3);u=np.linalg.solve(G,k);u/=k@u
    KKT=np.block([[G,k[:,None]],[k[None,:],np.zeros((1,1))]]);sol=np.linalg.solve(KKT,np.r_[np.zeros(3),1.])[:3]
    add('D03.inverse-metric-kkt',{'error':float(np.linalg.norm(u-sol)),'constraint_error':float(abs(k@u-1))},np.linalg.norm(u-sol)<1e-12,'cards/D03.json','Independent equality-constrained quadratic optimum; metric existence/causal estimation not tested.')
    # D06 determinant budget yields product singular-value lower bound when factors are contractions.
    mats=[]
    for j in range(5):
        k=rng.normal(size=3);k/=np.linalg.norm(k);mats.append(np.eye(3)-.1*np.outer(k,k))
    product=np.eye(3)
    for A in mats:product=A@product
    budget=-sum(np.linalg.slogdet(A)[1] for A in mats);lower=np.exp(-budget);actual=np.linalg.svd(product,compute_uv=False)[-1]
    add('D06.logdet-lower-bound',{'min_singular':float(actual),'lower_bound':float(lower)},actual+1e-12>=lower,'cards/D06.json','Bound holds for this positive determinant contraction path; utility/semantics are outside scope.')
    # D07 source-survival ratio is independent of the nonzero value residual norm.
    P=rng.normal(size=(3,3));k=rng.normal(size=3);e=rng.normal(size=2);W=np.outer(k,e)
    ratio=np.linalg.norm(P@W)**2/np.linalg.norm(W)**2;reference=np.linalg.norm(P@k)**2/np.linalg.norm(k)**2
    add('D07.source-survival-factorization',{'error':float(abs(ratio-reference))},abs(ratio-reference)<1e-12,'cards/D07.json','Source norm diagnostic does not establish query visibility or valid-knowledge retention.')
    return checks


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--seed',type=int,default=0);a=p.parse_args();t=time.perf_counter();checks=run(a.seed)
    result=dict(suite='legacy-controls',seed=a.seed,checks=checks,elapsed_seconds=time.perf_counter()-t,data_kind='constructed mathematical diagnostic')
    f=Path(a.output);f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'checks':len(checks),'failed':sum(x['status']=='failed' for x in checks),'assumption_repairs':sum(x.get('claim_status')=='archived_statement_needs_degeneracy_clause' for x in checks)}))
    raise SystemExit(any(x['status']=='failed' for x in checks))
