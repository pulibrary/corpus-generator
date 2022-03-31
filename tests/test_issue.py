# -*- coding: utf-8 -*-

from corpus_generator.issue import Issue

issue_path = "/Users/cwulfman/repos/github/pulibrary/corpus-generator/tests/data/06_01"

issue = Issue(issue_path)
assert len(issue.articles) == 30
