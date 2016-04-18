import unittest

import raw_log_processor as processor

class TestProcessor(unittest.TestCase):

    def test_returns_all_commits(self):
        with open('data/fakerepo_raw_logs.txt') as f:
            raw_logs = processor.read_file(f)
            commits = processor.make_commit_list(raw_logs)

            self.assertEqual(len(commits), 7)

