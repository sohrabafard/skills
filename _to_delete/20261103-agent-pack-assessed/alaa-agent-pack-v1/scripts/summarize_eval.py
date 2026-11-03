#!/usr/bin/env python3
"""Summarize measured JSONL. Reject synthetic data by default. Python 3.11+."""
import argparse, json, math, statistics
from collections import defaultdict
from pathlib import Path
def wilson(k,n):
    z=1.96; d=1+z*z/n; c=(k/n+z*z/(2*n))/d
    h=z*math.sqrt(k/n*(1-k/n)/n+z*z/(4*n*n))/d
    return [round(c-h,4),round(c+h,4)]
def summarize(rows,allow_synthetic=False):
    if not rows: raise ValueError('No measured runs supplied')
    groups=defaultdict(list); seen=set()
    for r in rows:
        for key in ('case_id','model','effort','run','attempts','accepted','first_attempt_accepted','critical_failure','cost_usd','wall_seconds','human_minutes','language_or_domain','evidence','synthetic'):
            if key not in r: raise ValueError(f'Missing field: {key}')
        for key in ('accepted','first_attempt_accepted','critical_failure','synthetic'):
            if type(r[key]) is not bool: raise ValueError(f'{key} must be boolean')
        if r['synthetic'] and not allow_synthetic: raise ValueError('Synthetic rows rejected; no benchmark was run')
        for key in ('run','attempts'):
            if type(r[key]) is not int or r[key]<1: raise ValueError(f'{key} must be positive integer')
        for key in ('cost_usd','wall_seconds','human_minutes'):
            v=r[key]
            if v is None and key=='cost_usd': continue
            if type(v) not in (int,float) or not math.isfinite(v) or v<0: raise ValueError(f'Invalid {key}')
        if not r['evidence']: raise ValueError('Evidence reference required')
        if r['critical_failure'] and r['accepted']: raise ValueError('Critical failure cannot be accepted')
        if r['first_attempt_accepted'] and not r['accepted']: raise ValueError('Inconsistent acceptance flags')
        key=(r['case_id'],r['model'],r['effort'],r['run'])
        if key in seen: raise ValueError('Duplicate run: '+str(key))
        seen.add(key); groups[(r['language_or_domain'],r['model'],r['effort'])].append(r)
    out=[]
    for (domain,model,effort),rs in sorted(groups.items()):
        n=len(rs); k=sum(r['accepted'] for r in rs)
        costs=[r['cost_usd'] for r in rs if r['cost_usd'] is not None]
        complete=len(costs)==n
        out.append(dict(domain=domain,model=model,effort=effort,runs=n,
          case_ids=sorted({r['case_id'] for r in rs}),accepted=k,
          acceptance_rate=k/n,first_attempt_rate=sum(r['first_attempt_accepted'] for r in rs)/n,
          approximate_wilson_95=wilson(k,n),critical_failures=sum(r['critical_failure'] for r in rs),
          median_wall_seconds=statistics.median(r['wall_seconds'] for r in rs),
          total_human_minutes=sum(r['human_minutes'] for r in rs),
          known_cost_usd=sum(costs),cost_complete=complete,
          total_cost_per_accepted_usd=(sum(costs)/k if k and complete else None)))
    return dict(warning='Compare matched case sets. Wilson intervals assume independence; repeated cases require paired/cluster-aware analysis. No causal or language ranking is inferred.',groups=out)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('results',type=Path);p.add_argument('--allow-synthetic',action='store_true');a=p.parse_args()
    rows=[json.loads(s) for s in a.results.read_text().splitlines() if s.strip()]
    try: result=summarize(rows,a.allow_synthetic)
    except ValueError as e: p.error(str(e))
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
