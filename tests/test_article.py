# -*- coding: utf-8 -*-

from corpus_generator.issue import Issue, Article

issue_path = "/Users/cwulfman/repos/github/pulibrary/corpus-generator/tests/data/06_01"

article = Issue(issue_path).articles[0]

article_date = "1968-05-06"
article_title = "Faculty to consider IDA, student power potentials"

def test_metadata():
    assert article.metadata['date']==article_date
    assert article.metadata['title']==article_title

def test_text():
    assert 'faculty' in article.text

def test_jsonl():
    assert article.jsonl['meta']['title']==article_title
    assert article.jsonl['meta']['date']==article_date
    assert 'faculty' in article.jsonl['text']
