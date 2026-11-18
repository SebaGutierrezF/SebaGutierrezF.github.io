from __future__ import annotations
import sys
from pathlib import Path
import tempfile
import unittest
from process_demo.engine import evaluate,load_csv,make_account_index,process_files,summarize
from process_demo.report import write_evidence

ROOT=Path(__file__).resolve().parents[1]

class ProcessTests(unittest.TestCase):
    def setUp(self):
        self.accounts={'C1':{'status':'ACTIVE','plan':'BASIC'},
                       'C2':{'status':'INACTIVE','plan':'PLUS'}}
    def request(self,**kw):
        return {'request_id':kw.get('request_id','R1'),'account_id':kw.get('account_id','C1'),
                'action':kw.get('action','CHANGE_PLAN'),'target_plan':kw.get('target_plan','PRO'),
                'approved':kw.get('approved','true')}
    def test_eligible_dry_run(self):
        d=evaluate([self.request()],self.accounts)
        self.assertEqual(d[0].outcome,'WOULD_EXECUTE')
        self.assertEqual(summarize(d)['external_mutations'],0)
    def test_duplicate_detected(self):
        d=evaluate([self.request(),self.request()],self.accounts)
        self.assertEqual([x.outcome for x in d],['WOULD_EXECUTE','SKIP_DUPLICATE'])
    def test_unapproved_held(self):
        self.assertEqual(evaluate([self.request(approved='false')],self.accounts)[0].outcome,'HOLD_NOT_APPROVED')
    def test_unknown_account_review(self):
        self.assertEqual(evaluate([self.request(account_id='MISSING')],self.accounts)[0].outcome,'REVIEW_UNKNOWN_ACCOUNT')
    def test_unexpected_plan_review(self):
        self.assertEqual(evaluate([self.request(action='ACTIVATE')],self.accounts)[0].outcome,'REVIEW_UNEXPECTED_PLAN')
    def test_concurrent_account_conflict(self):
        d=evaluate([self.request(),self.request(request_id='R2')],self.accounts)
        self.assertEqual(d[1].outcome,'HOLD_ACCOUNT_CONFLICT')
    def test_invalid_plan_review(self):
        self.assertEqual(evaluate([self.request(target_plan='GOLD')],self.accounts)[0].outcome,'REVIEW_INVALID_PLAN')
    def test_inactive_plan_change_held(self):
        self.assertEqual(evaluate([self.request(account_id='C2')],self.accounts)[0].outcome,'HOLD_INACTIVE_ACCOUNT')
    def test_csv_validation(self):
        with tempfile.TemporaryDirectory() as td:
            x=Path(td)/'bad.csv';x.write_text('wrong,columns\n1,2\n',encoding='utf-8')
            with self.assertRaises(ValueError): load_csv(x,('account_id','status','plan'))
    def test_duplicate_accounts_rejected(self):
        with self.assertRaises(ValueError):make_account_index([
            {'account_id':'X','status':'ACTIVE','plan':'BASIC'},
            {'account_id':'X','status':'ACTIVE','plan':'PRO'}])
    def test_end_to_end_report(self):
        decisions=process_files(ROOT/'data/requests.csv',ROOT/'data/accounts.csv')
        summary=summarize(decisions)
        self.assertEqual(summary['total'],10)
        self.assertEqual(summary['would_execute'],3)
        self.assertEqual(summary['external_mutations'],0)
        with tempfile.TemporaryDirectory() as td:
            write_evidence(decisions,Path(td))
            self.assertEqual(len((Path(td)/'audit.jsonl').read_text().splitlines()),10)
            self.assertIn('DRY RUN', (Path(td)/'report.html').read_text(encoding='utf-8'))
    def test_html_escapes_unsafe_values(self):
        from process_demo.engine import Decision
        from process_demo.report import render_report
        d=[Decision(2,'R1','C1','ACTIVATE','REVIEW_INVALID_ID','<script>alert(1)</script>')]
        html=render_report(d,summarize(d),'test')
        self.assertNotIn('<script>',html)
        self.assertIn('&lt;script&gt;',html)
    def test_invalid_approval_review(self):
        self.assertEqual(evaluate([self.request(approved='maybe')],self.accounts)[0].outcome,'REVIEW_INVALID_APPROVAL')
    def test_existing_state_skipped(self):
        self.assertEqual(evaluate([self.request(action='ACTIVATE',target_plan='')],self.accounts)[0].outcome,'SKIP_ALREADY_SATISFIED')

if __name__=='__main__':unittest.main()
