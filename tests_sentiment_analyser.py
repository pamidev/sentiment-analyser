import os
from unittest.mock import patch

import pytest

from sentiment_analyser import preprocess_review, compute_words, get_review, compute_sentiment, print_sentiment


def test_preprocess_review_with_punctuations():
    review = "<br />This <br>movie is*to: long+and=boring;<br />"
    result = preprocess_review(review)
    expected = ["this", "movie", "is", "to", "long", "and", "boring"]
    assert result == expected


def test_preprocess_review_without_punctuations():
    review = "A review without any punctuation"
    result = preprocess_review(review)
    expected = ["a", "review", "without", "any", "punctuation"]
    assert result == expected


@pytest.fixture
def tmp_files(tmpdir):
    tmp_file1 = tmpdir.join("file1.txt")
    tmp_file1.write("This is a test file.")
    tmp_file2 = tmpdir.join("file2.txt")
    tmp_file2.write("Another test file.")
    return str(tmpdir)


def test_compute_words(tmp_files):
    result = compute_words(os.path.join(tmp_files, "*.txt"))
    assert result.get("test") == 2
    assert result.get("file") == 2
    assert result.get("this") == 1
    assert result.get("is") == 1
    assert result.get("a") == 1
    assert result.get("another") == 1


@patch('builtins.input', return_value="This \"is a §test review! <br/>It contains punctuation./")
def test_get_review(mock_input):
    result = get_review()
    expected = ["this", "is", "a", "test", "review", "it", "contains", "punctuation"]
    assert result == expected


def test_compute_sentiment_positive_review():
    words = ["this", "is", "a", "positive", "review"]
    words_count_pos = {"this": 5, "is": 10, "a": 2, "positive": 50, "review": 20}
    words_count_neg = {"this": 1, "is": 0, "a": 0, "positive": 2, "review": 5}
    result = compute_sentiment(words, words_count_pos, words_count_neg)
    expected = 0.8379487179487178
    assert result == expected


def test_compute_sentiment_negative_review():
    words = ["this", "is", "a", "negative", "review"]
    words_count_pos = {"this": 5, "is": 10, "a": 2, "positive": 10, "review": 20}
    words_count_neg = {"this": 10, "is": 50, "a": 10, "negative": 70, "review": 5}
    result = compute_sentiment(words, words_count_pos, words_count_neg)
    expected = -0.4670967741935484
    assert result == expected


def test_compute_sentiment_neutral_review():
    words = ["this", "is", "a", "neutral", "review"]
    words_count_pos = {"this": 1, "is": 2, "a": 3, "positive": 11, "review": 22}
    words_count_neg = {"this": 1, "is": 2, "a": 3, "negative": 11, "review": 22}
    result = compute_sentiment(words, words_count_pos, words_count_neg)
    expected = 0.0
    assert result == expected


def test_print_sentiment(capsys):
    sentiment = 0.889
    expected = "------------------------------------------------------------\n" \
               "Entered review is positive. Sentiment = 0.889\n"
    print_sentiment(sentiment)
    captured_output = capsys.readouterr()
    assert captured_output.out == expected
