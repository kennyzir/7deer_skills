from __future__ import annotations
import copy
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
from unittest.mock import patch
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import evaluate as ev
import collect_public as cp


def sample():
    a=json.loads((ROOT/'examples/synthetic-assessment.json').read_text(encoding='utf-8'))
    a['example_only']=False  # synthetic unit-test fixture; not a real-world forecast
    return a


def full():
    a=sample()
    for k,(_,_,breaks) in ev.MODEL.items():
        a['metrics'][k]['value']=100 if breaks is None else breaks[-1][0]
    return a


def history(start,days=30,playing=100):
    return [{'universe_id':'999999999999','observed_at':ev.iso(start+timedelta(days=d,hours=h)),
             'collected_at':ev.iso(start+timedelta(days=d,hours=h)),
             'playing':playing,'visits':100000+(d*24+h)*100,'favorites':1000+(d*24+h),
             'source':'synthetic_test','_time':start+timedelta(days=d,hours=h)}
            for d in range(days) for h in range(24)]

class ScoringTests(unittest.TestCase):
    def test_weights_100(self): self.assertEqual(sum(v[1] for v in ev.MODEL.values()),100)
    def test_model_export_matches(self):
        m=json.loads((ROOT/'references/model.json').read_text())
        self.assertEqual(set(m['metrics']),set(ev.MODEL))
        for k,v in ev.MODEL.items(): self.assertEqual(m['metrics'][k]['weight'],v[1])
    def test_complete_score(self):
        r=ev.score(full()); self.assertEqual(r['score'],100)
        self.assertEqual(r['status'],'HIGH_POTENTIAL'); self.assertEqual(r['score_bounds'],[100,100])
        self.assertIsNone(r['probability'])
    def test_example_score(self): self.assertEqual(ev.score(sample())['score'],72.7)
    def test_unknown_not_zero(self):
        a=full()
        for m in a['metrics'].values(): m.update(status='unknown',value=None)
        r=ev.score(a)
        self.assertIsNone(r['score']); self.assertIsNone(r['observed_subscore'])
        self.assertEqual(r['score_bounds'],[0,100]); self.assertEqual(r['weighted_evidence_coverage'],0)
    def test_early_game_not_rejected(self):
        a=full()
        for k,v in ev.MODEL.items():
            if v[0]=='G': a['metrics'][k].update(status='not_applicable',value=None)
        r=ev.score(a)
        self.assertEqual(r['status'],'EARLY_CANDIDATE'); self.assertIsNone(r['score'])
        self.assertEqual(r['observed_subscore'],100); self.assertEqual(r['score_bounds'],[70,100])
    def test_unknown_numeric_rejected(self):
        a=sample(); a['metrics']['ccu_g7']['status']='unknown'
        with self.assertRaises(ValueError): ev.score(a)
    def test_nan_rejected(self):
        a=sample(); a['metrics']['ccu_g7']['value']=float('nan')
        with self.assertRaises(ValueError): ev.score(a)
    def test_bool_rejected(self):
        a=sample(); a['metrics']['ccu_g7']['value']=True
        with self.assertRaises(ValueError): ev.score(a)
    def test_fractional_count_rejected(self):
        a=sample(); a['metrics']['yt_creators7']['value']=3.5
        with self.assertRaises(ValueError): ev.score(a)
    def test_unresolved_identity(self):
        a=sample(); a['game']['identity_verified']=False
        self.assertEqual(ev.score(a)['status'],'IDENTITY_UNRESOLVED')
    def test_missing_evidence(self):
        a=sample(); a['metrics']['ccu_g7']['evidence_ids']=['DOES_NOT_EXIST']
        with self.assertRaises(ValueError): ev.score(a)
    def test_duplicate_evidence(self):
        a=sample(); a['evidence']*=2
        with self.assertRaises(ValueError): ev.score(a)
    def test_future_evidence(self):
        a=sample(); a['evidence'][0]['observed_at']='2026-09-07T00:00:00Z'
        with self.assertRaises(ValueError): ev.score(a)
    def test_future_collection(self):
        a=sample(); a['evidence'][0]['collected_at']='2026-09-07T00:00:00Z'
        with self.assertRaises(ValueError): ev.score(a)
    def test_future_metric(self):
        a=sample(); a['metrics']['ccu_g7']['window_end']='2026-09-08T00:00:00Z'
        with self.assertRaises(ValueError): ev.score(a)
    def test_description_only_rejected(self):
        a=sample(); a['evidence'][0]['kind']='description'
        with self.assertRaises(ValueError): ev.score(a)
    def test_arbitrary_rubric_rejected(self):
        a=sample(); a['metrics']['core_loop']['value']=89
        with self.assertRaises(ValueError): ev.score(a)
    def test_missing_metric_rejected(self):
        a=sample(); del a['metrics']['core_loop']
        with self.assertRaises(ValueError): ev.score(a)
    def test_seo_does_not_change_score(self):
        a=full(); before=ev.score(a)
        a['seo_assessment']={'score':0,'search_volume':0,'no_domain':True}
        self.assertEqual(ev.score(a)['score'],before['score'])
        self.assertEqual(ev.score(a)['status'],before['status'])
    def test_unattempted_source_not_complete(self):
        a=full(); a['collection_log']=[]
        r=ev.score(a); self.assertEqual(r['collection_status'],'PARTIAL')
        self.assertEqual(r['status'],'WATCHLIST')
    def test_missing_baseline_abstains(self):
        a=full(); a['diagnostics']['baseline_ccu']=None
        r=ev.score(a); self.assertIsNone(r['prediction']['daily_median_threshold'])
        self.assertEqual(r['prediction']['vote'],'ABSTAIN')
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.json'; ev.write_new(p,{})
            with self.assertRaises(FileExistsError): ev.write_new(p,{'overwrite':True})
    def test_timezone_required(self):
        with self.assertRaises(ValueError): ev.dt('2026-09-06T12:00:00')

class HistoryTests(unittest.TestCase):
    def setUp(self): self.start=ev.dt('2026-08-23T00:00:00Z')
    def test_hour_aggregation_avoids_frequency_bias(self):
        rows=history(self.start,1,100)
        for i in range(1,59):
            r=copy.deepcopy(rows[0]); r['_time']=self.start+timedelta(minutes=i); r['playing']=10000; rows.append(r)
        d=ev.daily(rows,self.start+timedelta(days=1))['2026-08-23']
        self.assertEqual(d['median'],100)
    def test_sparse_day_unknown(self):
        rows=history(self.start,1)[:4]
        self.assertFalse(ev.daily(rows,self.start+timedelta(days=1))['2026-08-23']['valid'])
    def test_long_gap_unknown(self):
        rows=history(self.start,1)[6:]
        self.assertFalse(ev.daily(rows,self.start+timedelta(days=1))['2026-08-23']['valid'])
    def test_current_day_excluded(self):
        rows=history(self.start,1)
        self.assertEqual(ev.daily(rows,self.start+timedelta(hours=12)),{})
    def test_zero_denominator_not_infinity(self): self.assertIsNone(ev.safe_ratio(100,0))
    def test_no_fake_seven_day_growth(self):
        rows=history(self.start,3)
        self.assertIsNone(ev.derive(rows,self.start+timedelta(days=3))['ccu_g7'])
    def test_valid_growth(self):
        rows=history(self.start,8)
        for r in rows:
            if r['_time'].date()==(self.start+timedelta(days=7)).date(): r['playing']=500
        self.assertEqual(ev.derive(rows,self.start+timedelta(days=8))['ccu_g7'],5)
    def test_counter_reset_unknown(self):
        rows=history(self.start,15)
        rows[200]['visits']=1
        self.assertIsNone(ev.counter_week_ratio(rows,self.start+timedelta(days=14),'visits')['value'])
    def test_mixed_identity_rejected(self):
        row=history(self.start,1)[0]; row.pop('_time'); row['universe_id']='123'
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.jsonl'; p.write_text(json.dumps(row)+'\n')
            with self.assertRaises(ValueError): ev.read_history(str(p),'999999999999',self.start+timedelta(days=1))
    def test_mixed_source_rejected(self):
        rows=history(self.start,1)[:2]
        for r in rows: r.pop('_time')
        rows[1]['source']='other'
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.jsonl'; p.write_text('\n'.join(json.dumps(r) for r in rows))
            with self.assertRaises(ValueError): ev.read_history(str(p),'999999999999',self.start+timedelta(days=1))

class OutcomeTests(unittest.TestCase):
    def setUp(self):
        self.pred=ev.score(full())['prediction']; self.start=ev.dt(self.pred['outcome_window_start'])
        self.end=ev.dt(self.pred['outcome_window_end'])
    def test_pending_is_not_failure(self):
        r=ev.review(self.pred,history(self.start,2),self.start+timedelta(days=2))
        self.assertEqual(r['sustained_breakout_30d']['status'],'PENDING'); self.assertIsNone(r['evaluation_label'])
    def test_hit(self):
        r=ev.review(self.pred,history(self.start,30,30000),self.end)
        self.assertEqual(r['sustained_breakout_30d']['status'],'HIT'); self.assertEqual(r['evaluation_label'],'TP')
        self.assertEqual(r['scale_hit_30d']['status'],'NOT_HIT')
    def test_one_spike_not_sustained_hit(self):
        rows=history(self.start,30,100); rows[10]['playing']=200000
        r=ev.review(self.pred,rows,self.end)
        self.assertEqual(r['sustained_breakout_30d']['status'],'NOT_HIT')
        self.assertEqual(r['peak_100k']['status'],'OBSERVED')
    def test_missing_outcome_is_not_failure(self):
        rows=history(self.start,29,100)
        r=ev.review(self.pred,rows,self.end)
        self.assertEqual(r['sustained_breakout_30d']['status'],'INCOMPLETE'); self.assertIsNone(r['evaluation_label'])
    def test_three_days_must_be_consecutive(self):
        rows=history(self.start,30,100)
        for r in rows:
            if (r['_time']-self.start).days in {1,3,5}: r['playing']=30000
        self.assertEqual(ev.review(self.pred,rows,self.end)['sustained_breakout_30d']['status'],'NOT_HIT')
    def test_hash_tamper_rejected(self):
        p=copy.deepcopy(self.pred); p['daily_median_threshold']=1
        with self.assertRaises(ValueError): ev.review(p,[],self.end)
    def test_synthetic_example_not_performance(self):
        a=full(); a['example_only']=True; p=ev.score(a)['prediction']
        r=ev.review(p,history(self.start,30,30000),self.end)
        self.assertIsNone(r['evaluation_label'])

class CollectorTests(unittest.TestCase):
    def test_canonical_place_id(self): self.assertEqual(cp.place_id('https://www.roblox.com/games/123/Test'),'123')
    def test_ssrf_url_rejected(self):
        with self.assertRaises(ValueError): cp.place_id('http://127.0.0.1/games/123')
    def test_lookalike_host_rejected(self):
        with self.assertRaises(ValueError): cp.place_id('https://www.roblox.com.evil.test/games/123')
    def test_missing_key_fallback(self):
        class Args: pass
        with patch.dict('os.environ',{},clear=True):
            self.assertEqual(cp.youtube(Args(),None)['status'],'NOT_CONFIGURED')
    def test_network_failure_logged(self):
        with tempfile.TemporaryDirectory() as td:
            reader=cp.Reader(Path(td))
            with patch('urllib.request.urlopen',side_effect=urllib.error.URLError('offline')):
                data,record=reader.get('https://games.roblox.com/v1/games?universeIds=123')
            self.assertIsNone(data); self.assertEqual(record['status'],'failed')
            self.assertTrue((Path(td)/'raw/001.json').exists())
    def test_secret_redacted(self):
        with tempfile.TemporaryDirectory() as td:
            reader=cp.Reader(Path(td)); secret='TEST_API_SECRET'
            with patch('urllib.request.urlopen',side_effect=urllib.error.URLError(secret)):
                reader.get('https://www.googleapis.com/youtube/v3/search?key='+secret,secret)
            self.assertNotIn(secret,(Path(td)/'raw/001.json').read_text())

if __name__=='__main__': unittest.main()
