import importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts/summarize_eval.py'
s=importlib.util.spec_from_file_location('summary',p); m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def row(**kw):
    r=dict(case_id='PY01',model='gpt-6.1-terra',effort='medium',run=1,attempts=1,
       accepted=True,first_attempt_accepted=True,critical_failure=False,cost_usd=1.,
       wall_seconds=10,human_minutes=2,language_or_domain='python',evidence='fixture',synthetic=True)
    r.update(kw);return r
class SummaryTests(unittest.TestCase):
    def test_rejects_synthetic(self):
        with self.assertRaises(ValueError):m.summarize([row()])
    def test_counts_failure_cost(self):
        out=m.summarize([row(),row(run=2,accepted=False,first_attempt_accepted=False,cost_usd=2)],True)['groups'][0]
        self.assertEqual(out['total_cost_per_accepted_usd'],3)
        self.assertEqual(out['acceptance_rate'],.5)
    def test_missing_cost_not_zero(self):
        out=m.summarize([row(cost_usd=None)],True)['groups'][0]
        self.assertIsNone(out['total_cost_per_accepted_usd']);self.assertFalse(out['cost_complete'])
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):m.summarize([row(),row()],True)
    def test_critical_not_accepted(self):
        with self.assertRaises(ValueError):m.summarize([row(critical_failure=True)],True)
    def test_negative_rejected(self):
        with self.assertRaises(ValueError):m.summarize([row(wall_seconds=-1)],True)
    def test_first_attempt_flags(self):
        with self.assertRaises(ValueError):m.summarize([row(accepted=False)],True)
    def test_interval(self):
        lo,hi=m.wilson(3,10);self.assertLess(lo,.3);self.assertGreater(hi,.3)
    def test_empty(self):
        with self.assertRaises(ValueError):m.summarize([])
if __name__=='__main__':unittest.main()
