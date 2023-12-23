import unittest
from src.bechdel_scorer import bechdel_scorer

class TestBechdelScorer(unittest.TestCase):
    def test_fail_notalk_disagree(self):
        self.assertEqual(bechdel_scorer(('FAIL', 'notalk', 'notalk-disagree')), -0.75)

    def test_fail_dubious_disagree(self):
        self.assertEqual(bechdel_scorer(('FAIL', 'dubious', 'dubious-disagree')), -0.75)

    def test_pass_ok_disagree(self):
        self.assertEqual(bechdel_scorer(('PASS', 'ok', 'ok-disagree')), 1)

    def test_pass_ok_ok(self):
        self.assertEqual(bechdel_scorer(('PASS', 'ok', 'ok')), 1)

if __name__ == '__main__':
    unittest.main()
