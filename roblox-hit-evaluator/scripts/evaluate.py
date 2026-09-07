#!/usr/bin/env python3
"""Qilu Roblox hit evaluator. Python 3.10+, standard library only.
No network, scheduling, installations, or repository changes.
All scoring constants are exploratory rules, NOT calibrated probabilities.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

VERSION = 'qilu-hit-v0.1'
UTC = timezone.utc
# key: (dimension, weight, breakpoints). Rubrics accept only 0/25/50/75/100.
MODEL = {
    'ccu_g7': ('G', 15, [(0,0),(.5,10),(1,30),(1.5,45),(2,60),(3,75),(5,90),(8,100)]),
    'ccu_floor_g7': ('G', 5, [(0,0),(.5,15),(1,40),(1.2,60),(1.5,80),(2,100)]),
    'visits_accel7': ('G', 5, [(0,0),(.5,15),(1,40),(1.5,65),(2,85),(3,100)]),
    'favorites_accel7': ('G', 5, [(0,0),(.5,15),(1,40),(1.5,65),(2,85),(3,100)]),
    'core_loop': ('C', 8, None),
    'replay_depth': ('C', 8, None),
    'design_difference': ('C', 9, None),
    'decision_depth': ('D', 8, None),
    'community_participation': ('D', 7, None),
    'yt_creators7': ('V', 7, [(0,0),(1,15),(3,30),(5,45),(10,60),(15,75),(30,90),(50,100)]),
    'yt_videos_g7': ('V', 6, [(0,0),(.5,15),(1,40),(1.5,65),(2,85),(3,100)]),
    'yt_velocity_ratio': ('V', 4, [(0,0),(.5,15),(1,40),(1.5,65),(2,85),(3,100)]),
    'shareable_moments': ('V', 3, None),
    'content_updates14': ('U', 3, [(0,0),(1,60),(2,80),(3,90),(4,100)]),
    'post_update_baseline': ('U', 7, [(0,0),(.5,15),(1,40),(1.2,65),(1.5,85),(2,100)]),
}
VALID_STATUSES = {'observed','derived','unknown','not_collected','unavailable',
                  'conflicting','stale','partial','not_applicable'}
KNOWN = {'observed','derived'}
FAMILIES = ('roblox_identity','roblox_history','gameplay','updates','youtube','community')
ATTEMPT_STATUSES = {'success','partial','unavailable','blocked','not_configured',
                    'budget_exhausted','not_attempted'}


def dt(s: str) -> datetime:
    if not isinstance(s, str):
        raise ValueError('Timestamp must be an ISO-8601 string with timezone')
    value = datetime.fromisoformat(s.replace('Z','+00:00'))
    if value.tzinfo is None:
        raise ValueError('Naive timestamp: supply UTC offset or Z')
    return value.astimezone(UTC)


def iso(t: datetime) -> str:
    return t.astimezone(UTC).isoformat().replace('+00:00','Z')


def number(value: Any) -> bool:
    return isinstance(value, (int,float)) and not isinstance(value,bool) and math.isfinite(value)


def read_json(path: str | Path) -> dict:
    with Path(path).open(encoding='utf-8-sig') as f:
        obj = json.load(f)
    if not isinstance(obj,dict):
        raise ValueError('Expected JSON object')
    return obj


def write_new(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2,allow_nan=False)
        f.write('\n')


def digest(obj: Any) -> str:
    data = json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)
    return hashlib.sha256(data.encode()).hexdigest()


def step_score(value: float, breakpoints: list) -> float:
    result = breakpoints[0][1]
    for threshold, points in breakpoints:
        if value >= threshold:
            result = points
    return float(result)


def score(a: dict) -> dict:
    if a.get('model_version') != VERSION:
        raise ValueError(f'model_version must be {VERSION}')
    cutoff = dt(a['data_as_of'])
    game = a.get('game',{})
    uid = str(game.get('universe_id',''))
    if not uid.isdigit() or int(uid) <= 0:
        raise ValueError('A verified positive universe_id is required (do not use place_id)')
    evidence = {}
    for e in a.get('evidence',[]):
        eid = e.get('id')
        if not isinstance(eid,str) or not eid or eid in evidence:
            raise ValueError('Evidence IDs must be nonempty and unique')
        for field in ('source','locator','claim','kind','observed_at','collected_at'):
            if not e.get(field):
                raise ValueError(f'{eid}: missing {field}')
        # v0.1 is prospective only. Historical reconstruction is not treated as a prediction.
        if dt(e['observed_at']) > cutoff or dt(e['collected_at']) > cutoff:
            raise ValueError(f'{eid}: evidence after data_as_of (look-ahead)')
        evidence[eid] = e

    def check_refs(refs: Any, owner: str) -> None:
        if not isinstance(refs,list) or not refs or any(r not in evidence for r in refs):
            raise ValueError(f'{owner}: missing or unresolved evidence_ids')

    verified = game.get('identity_verified') is True
    if verified:
        check_refs(game.get('identity_evidence_ids'), 'game identity')
    else:
        return {'model_version':VERSION,'status':'IDENTITY_UNRESOLVED','score':None,
                'reason':'Resolve universe identity before assessing the game.'}
    metrics = a.get('metrics',{})
    if set(metrics) != set(MODEL):
        raise ValueError(f'Metric keys mismatch. Missing={sorted(set(MODEL)-set(metrics))}; '
                         f'extra={sorted(set(metrics)-set(MODEL))}')
    dims = {d:{'weight':0,'observed_weight':0,'contribution':0.0,'score':None} for d in 'GCDVU'}
    known_weight = 0
    total = 0.0
    rows, missing, warnings = [], [], []
    for key, (dim, weight, points) in MODEL.items():
        m = metrics[key]
        status = m.get('status')
        if status not in VALID_STATUSES:
            raise ValueError(f'{key}: invalid status {status}')
        if not str(m.get('reason','')).strip():
            raise ValueError(f'{key}: reason is required, including for unknown values')
        dims[dim]['weight'] += weight
        accepted = status in KNOWN
        if not accepted:
            if m.get('value') is not None:
                raise ValueError(f'{key}: non-observed values must be null; keep partial samples in diagnostics')
            missing.append(key)
            rows.append({'metric':key,'dimension':dim,'weight':weight,'status':status,
                         'score':None,'reason':m['reason']})
            continue
        value = m.get('value')
        if not number(value) or value < 0:
            raise ValueError(f'{key}: expected finite nonnegative number')
        check_refs(m.get('evidence_ids'),key)
        if points is None:
            if value not in {0,25,50,75,100}:
                raise ValueError(f'{key}: rubric must be one of 0,25,50,75,100')
            # A statement in promotional copy is not observed player behaviour.
            only_promotional = all(evidence[r]['kind'] in {'description','marketing','title'}
                                   for r in m['evidence_ids'])
            if only_promotional:
                raise ValueError(f'{key}: description-only inference must remain unknown')
        else:
            if not m.get('method') or not m.get('window_start') or not m.get('window_end'):
                raise ValueError(f'{key}: calculation method and window are required')
            start,end = dt(m['window_start']),dt(m['window_end'])
            if start >= end or end > cutoff:
                raise ValueError(f'{key}: invalid or future window')
            if key in {'yt_creators7','content_updates14'} and int(value) != value:
                raise ValueError(f'{key}: count must be an integer')
        s = value if points is None else step_score(value,points)
        c = weight * s / 100
        total += c
        known_weight += weight
        dims[dim]['observed_weight'] += weight
        dims[dim]['contribution'] += c
        rows.append({'metric':key,'dimension':dim,'weight':weight,'status':status,
                     'value':value,'score':s,'contribution':round(c,3),
                     'evidence_ids':m['evidence_ids'],'reason':m['reason']})
    for item in dims.values():
        k = item['observed_weight']
        item['coverage'] = round(k/item['weight'],3)
        item['score'] = round(100*item['contribution']/k,1) if k else None
        item['contribution'] = round(item['contribution'],3)
    observed_score = round(100*total/known_weight,1) if known_weight else None
    dimensional_count = sum(d['observed_weight']>0 for d in dims.values())
    g7_known = metrics['ccu_g7']['status'] in KNOWN
    eligible = known_weight >= 60 and dimensional_count >= 3 and g7_known
    full_score = observed_score if eligible else None
    attempts = a.get('collection_log',[])
    by_family = defaultdict(list)
    for item in attempts:
        if item.get('family') not in FAMILIES or item.get('status') not in ATTEMPT_STATUSES:
            raise ValueError('collection_log: invalid family/status')
        if not item.get('detail'):
            raise ValueError('collection_log: detail required')
        by_family[item['family']].append(item)
    unattempted = [f for f in FAMILIES if not any(x['status']!='not_attempted' for x in by_family[f])]
    unresolved_collection = [f for f in FAMILIES if not any(x['status']=='success' for x in by_family[f])]
    if unattempted:
        warnings.append('Source families not attempted: '+', '.join(unattempted))
    # Evidence coverage measures available weighted inputs, not truth or accuracy.
    grade = 'HIGH' if known_weight>=80 else 'MEDIUM' if known_weight>=60 else 'LOW'
    if not eligible:
        status = 'EARLY_CANDIDATE' if any(dims[d]['score'] is not None and dims[d]['score']>=65
                                         for d in ('C','D','V')) else 'INSUFFICIENT_EVIDENCE'
    elif full_score >= 75 and known_weight >= 80 and not unattempted:
        status = 'HIGH_POTENTIAL'
    elif full_score >= 60:
        status = 'WATCHLIST'
    elif full_score >= 45:
        status = 'LOW_PRIORITY'
    else:
        status = 'WEAK_CURRENT_EVIDENCE'
    if not g7_known:
        warnings.append('No valid 7-day trajectory. Structural evidence is not a validated growth signal.')
    if a.get('diagnostics',{}).get('paid_promotion') is True:
        warnings.append('Paid promotion observed: growth cannot be attributed to organic demand alone.')
    baseline = a.get('diagnostics',{}).get('baseline_ccu')
    if baseline is not None and (not number(baseline) or baseline<0):
        raise ValueError('baseline_ccu must be nonnegative or null')
    if baseline is not None:
        check_refs(a.get('diagnostics',{}).get('baseline_evidence_ids'), 'baseline_ccu')
    primary_threshold = max(10000, 3*baseline) if baseline is not None else None
    vote = ('POSITIVE' if status=='HIGH_POTENTIAL' else
            'NEGATIVE' if eligible and known_weight>=80 and full_score<45 and not unattempted else 'ABSTAIN')
    # Freeze full UTC days beginning after the cutoff. They form a reproducible 30-day window.
    outcome_start = cutoff.replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(days=1)
    prediction = {
        'model_version':VERSION,'assessment_hash':digest(a),'game_universe_id':uid,
        'frozen_at':iso(cutoff),'outcome_window_start':iso(outcome_start),
        'outcome_window_end':iso(outcome_start+timedelta(days=30)),
        'horizon_days':30,'primary_target':'sustained_breakout_30d',
        'example_only':a.get('example_only') is True,
        'baseline_ccu':baseline,'daily_median_threshold':primary_threshold,
        'required_consecutive_days':3,'scale_hit_daily_median_threshold':100000,
        'peak_diagnostic_threshold':100000,'vote':vote,
        'score':full_score,'observed_weight':known_weight,'is_probability':False,
        'sampling_policy':{'min_hour_bins':18,'max_missing_hour_run':4,'timezone':'UTC'},
    }
    if primary_threshold is None:
        prediction['vote'] = 'ABSTAIN'
        warnings.append('Baseline CCU unavailable: relative-growth outcome cannot be frozen; scale target remains measurable.')
    if a.get('example_only') is True:
        warnings.append('SYNTHETIC EXAMPLE: do not use in real prediction performance statistics.')
    prediction['prediction_hash'] = digest(prediction)
    return {
        'model_version':VERSION,'data_as_of':iso(cutoff),'game':game,'status':status,
        'example_only':a.get('example_only') is True,
        'score':full_score,'observed_subscore':observed_score,
        'weighted_evidence_coverage':round(known_weight/100,3),
        'evidence_sufficiency':grade,
        'score_bounds':[round(total,1),round(total+100-known_weight,1)],
        'bounds_meaning':'Missing-data best/worst bounds, NOT a confidence interval or probability.',
        'dimensions':dims,'metric_scores':rows,'missing_metrics':missing,
        'collection_status':'COMPLETE_WITHIN_DECLARED_SCOPE' if not unresolved_collection else 'PARTIAL',
        'unattempted_families':unattempted,'unresolved_families':unresolved_collection,
        'warnings':warnings,'probability':None,'prediction':prediction,
        'seo_assessment':a.get('seo_assessment',{'status':'NOT_REQUESTED'}),
        'next_action':'Investigate the highest-weight missing input that could change the decision. Do not auto-build.'
    }


def read_history(path: str, uid: str, asof: datetime) -> list[dict]:
    rows = []
    with Path(path).open(encoding='utf-8-sig') as f:
        for n,line in enumerate(f,1):
            if not line.strip(): continue
            r = json.loads(line)
            if str(r.get('universe_id')) != str(uid):
                raise ValueError(f'History line {n}: mixed universe IDs')
            observed = dt(r['observed_at'])
            if observed > asof:
                raise ValueError(f'History line {n}: observation after cutoff')
            if not r.get('source'):
                raise ValueError(f'History line {n}: source required')
            if r.get('collected_at') and dt(r['collected_at']) > asof:
                raise ValueError(f'History line {n}: collected after cutoff')
            for field in ('playing','visits','favorites'):
                v = r.get(field)
                if v is not None and (not number(v) or v<0):
                    raise ValueError(f'History line {n}: invalid {field}')
            r['_time'] = observed
            rows.append(r)
    sources = {r['source'] for r in rows}
    if len(sources)>1:
        raise ValueError('History mixes sources; reconcile into a single declared measurement series first')
    # Reject contradicting duplicate timestamps, rather than averaging disagreeing measurements.
    seen = {}
    for r in rows:
        key = r['_time']
        if key in seen and any(seen[key].get(k) != r.get(k) for k in ('playing','visits','favorites')):
            raise ValueError('Conflicting duplicate history timestamps')
        seen[key] = r
    return sorted(seen.values(),key=lambda r:r['_time'])


def quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered: raise ValueError('Empty quantile')
    idx = (len(ordered)-1)*q
    low, high = math.floor(idx), math.ceil(idx)
    return ordered[low] + (ordered[high]-ordered[low])*(idx-low)


def daily(rows: list[dict], asof: datetime) -> dict[str,dict]:
    buckets = defaultdict(lambda:defaultdict(list))
    for r in rows:
        t = r['_time']
        if t.date() >= asof.date() or r.get('playing') is None: continue
        buckets[t.date().isoformat()][t.hour].append(r['playing'])
    result = {}
    for day,bins in buckets.items():
        longest = run = 0
        for h in range(24):
            run = run+1 if h not in bins else 0
            longest = max(longest,run)
        values = [statistics.median(bins[h]) for h in sorted(bins)]
        valid = len(bins)>=18 and longest<=4
        result[day] = {'date':day,'valid':valid,'hour_bins':len(bins),
                       'coverage':round(len(bins)/24,4),'longest_missing_hours':longest,
                       'median':statistics.median(values) if valid else None,
                       'p20':quantile(values,.2) if valid else None,
                       'sampled_peak':max(v for items in bins.values() for v in items)}
    return result


def safe_ratio(n: Any, d: Any) -> float | None:
    return n/d if number(n) and number(d) and n>=0 and d>0 else None


def counter_week_ratio(rows: list[dict], cutoff: datetime, field: str) -> dict:
    boundary = cutoff.replace(hour=0,minute=0,second=0,microsecond=0)
    chosen = []
    for days in (14,7,0):
        target = boundary-timedelta(days=days)
        candidates = [r for r in rows if r.get(field) is not None and abs((r['_time']-target).total_seconds())<=7200]
        if not candidates: return {'value':None,'reason':'Missing a counter boundary within ±2 hours'}
        chosen.append(min(candidates,key=lambda r:abs((r['_time']-target).total_seconds())))
    a,b,c=chosen
    duration1=(b['_time']-a['_time']).total_seconds()
    duration2=(c['_time']-b['_time']).total_seconds()
    if min(duration1,duration2)<=0 or abs(duration2/duration1-1)>.025:
        return {'value':None,'reason':'Counter windows differ in duration by more than 2.5%'}
    previous=b[field]-a[field]; current=c[field]-b[field]
    series=[r[field] for r in rows if a['_time']<=r['_time']<=c['_time'] and r.get(field) is not None]
    if any(y<x for x,y in zip(series,series[1:])):
        return {'value':None,'reason':'Counter decreased: reconcile removals/reset before growth calculation',
                'previous_net_delta':previous,'current_net_delta':current}
    return {'value':safe_ratio(current,previous),'previous_delta':previous,'current_delta':current,
            'boundary_times':[iso(r['_time']) for r in chosen],
            'reason':'Consecutive 7-day net increment ratio; not unique users or retention'}


def derive(rows: list[dict], asof: datetime) -> dict:
    days=daily(rows,asof)
    last=(asof.date()-timedelta(days=1)).isoformat()
    old=(asof.date()-timedelta(days=8)).isoformat()
    recent=days.get(last,{})
    previous=days.get(old,{})
    return {'data_as_of':iso(asof),'model_version':VERSION,'daily':days,
            'baseline_ccu':recent.get('median'),
            'ccu_g7':safe_ratio(recent.get('median'),previous.get('median')),
            'ccu_floor_g7':safe_ratio(recent.get('p20'),previous.get('p20')),
            'comparison_days':[old,last],
            'visits_accel7':counter_week_ratio(rows,asof,'visits'),
            'favorites_accel7':counter_week_ratio(rows,asof,'favorites'),
            'warning':'Derived numbers are not yet a complete assessment. Attach raw-source evidence IDs.'}


def review(prediction: dict, rows: list[dict], asof: datetime) -> dict:
    p=dict(prediction)
    actual_hash=p.pop('prediction_hash',None)
    if not actual_hash or digest(p)!=actual_hash:
        raise ValueError('Frozen prediction hash mismatch')
    if p.get('model_version')!=VERSION:
        raise ValueError('Review with the model version used to freeze the prediction')
    start,end=dt(p['outcome_window_start']),dt(p['outcome_window_end'])
    if asof < dt(p['frozen_at']): raise ValueError('Review before prediction')
    result_days=daily(rows,asof)
    expected=[(start+timedelta(days=n)).date().isoformat() for n in range(p['horizon_days'])]
    complete=sum(result_days.get(d,{}).get('valid',False) for d in expected)
    matured=asof>=end
    def outcome(threshold: float|None) -> dict:
        if threshold is None: return {'status':'UNAVAILABLE','reason':'No frozen baseline'}
        streak=0
        dates=[]
        for day in expected:
            item=result_days.get(day,{})
            if item.get('valid') and item['median']>=threshold:
                streak+=1; dates.append(day)
                if streak>=p['required_consecutive_days']:
                    return {'status':'HIT','reached_on':day,'qualifying_days':dates[-streak:],
                            'threshold':threshold,'matured':matured}
            else: streak=0; dates=[]
        return {'status':'PENDING' if not matured else ('NOT_HIT' if complete==len(expected) else 'INCOMPLETE'),
                'threshold':threshold,'matured':matured}
    scoped=[r for r in rows if start<=r['_time']<min(end,asof) and r.get('playing') is not None]
    peak=max((r['playing'] for r in scoped),default=None)
    primary=outcome(p['daily_median_threshold'])
    result={'prediction_hash':actual_hash,'review_as_of':iso(asof),'matured':matured,
            'covered_days':complete,'expected_days':len(expected),
            'sustained_breakout_30d':primary,
            'scale_hit_30d':outcome(p['scale_hit_daily_median_threshold']),
            'peak_100k':{'sampled_peak':peak,'status':('OBSERVED' if peak is not None and peak>=100000 else 'NOT_OBSERVED'),
                         'note':'NOT_OBSERVED is not proof that no instantaneous peak occurred.'},
            'evaluation_label':None}
    if matured and primary['status'] in {'HIT','NOT_HIT'} and not p.get('example_only'):
        hit=primary['status']=='HIT'; vote=p['vote']
        result['evaluation_label']=('ABSTAIN' if vote=='ABSTAIN' else
                                    'TP' if vote=='POSITIVE' and hit else
                                    'FP' if vote=='POSITIVE' else
                                    'FN' if hit else 'TN')
    return result


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('score'); s.add_argument('assessment'); s.add_argument('--out',required=True)
    d=sub.add_parser('derive'); d.add_argument('history'); d.add_argument('--universe-id',required=True)
    d.add_argument('--as-of',required=True); d.add_argument('--out',required=True)
    r=sub.add_parser('review'); r.add_argument('scored_report'); r.add_argument('history')
    r.add_argument('--as-of',required=True); r.add_argument('--out',required=True)
    args=parser.parse_args()
    try:
        if args.cmd=='score': obj=score(read_json(args.assessment))
        elif args.cmd=='derive':
            cutoff=dt(args.as_of); obj=derive(read_history(args.history,args.universe_id,cutoff),cutoff)
        else:
            cutoff=dt(args.as_of); report=read_json(args.scored_report); p=report['prediction']
            obj=review(p,read_history(args.history,p['game_universe_id'],cutoff),cutoff)
        write_new(args.out,obj)
        print(json.dumps({'status':'WRITTEN','path':str(Path(args.out).resolve())},ensure_ascii=False))
        return 0
    except (ValueError,KeyError,TypeError,OSError,json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr); return 2

if __name__=='__main__':
    raise SystemExit(main())
