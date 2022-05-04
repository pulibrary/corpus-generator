# -*- coding: utf-8 -*-

from corpus_generator.issue import Issue

issue_path = "/Users/cwulfman/repos/github/pulibrary/corpus-generator/tests/data/06_01"

def test_issue():
    issue = Issue(issue_path)
    assert len(issue.articles) == 30
    assert issue.date == "1968-05-06"

def test_jsonl():
    issue = Issue(issue_path)
    assert issue.jsonl is not None
