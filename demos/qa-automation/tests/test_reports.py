from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from junit_to_portfolio import parse_junit, write_report

class ReporterTests(unittest.TestCase):
    def run_xml(self, xml):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'results.xml'
            path.write_text(xml,encoding='utf-8')
            data = parse_junit(path)
            write_report(data,Path(d)/'out')
            self.assertTrue((Path(d)/'out'/'index.html').exists())
            self.assertTrue((Path(d)/'out'/'summary.json').exists())
            return data,(Path(d)/'out'/'index.html').read_text(encoding='utf-8')
    def test_pass_real_xml_format(self):
        d,_=self.run_xml('<testsuites><testsuite><testcase name="api" classname="demo" time="0.1"/></testsuite></testsuites>')
        self.assertEqual(d['overall'],'PASS')
    def test_failure_not_pass(self):
        d,_=self.run_xml('<testsuite><testcase name="api"><failure>bad</failure></testcase></testsuite>')
        self.assertEqual(d['overall'],'NOT_PASS')
    def test_skip_not_pass(self):
        d,_=self.run_xml('<testsuite><testcase name="ui"><skipped/></testcase></testsuite>')
        self.assertEqual(d['overall'],'NOT_PASS')
    def test_error_not_pass(self):
        d,_=self.run_xml('<testsuite><testcase name="ui"><error/></testcase></testsuite>')
        self.assertEqual(d['counts']['ERROR'],1)
        self.assertEqual(d['overall'],'NOT_PASS')
    def test_empty_xml_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            x=Path(d)/'empty.xml';x.write_text('<testsuite/>')
            with self.assertRaises(ValueError): parse_junit(x)
    def test_untrusted_name_escaped(self):
        d,html=self.run_xml('<testsuite><testcase name="&lt;script&gt;alert(1)&lt;/script&gt;"/></testsuite>')
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>',html)

if __name__=='__main__': unittest.main()
