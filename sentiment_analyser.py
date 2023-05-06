from glob import glob

POSITIVE_PATTERN = r".\data\pos\*.txt"
NEGATIVE_PATTERN = r".\data\neg\*.txt"
PUNCTUATIONS = ("<br>", "<br/>", "<br />", ".", ",", "?", "!",
                "-", '"', "", "(", ")", ":", ";", "-", "+",
                "=", "/", "§", "*", "¡", "¦", "\\x91", "\\x97")
POSITIVE_WORDS_DICT = {}
NEGATIVE_WORDS_DICT = {}


def preprocess_review(review):
    review = review.lower()
    for punc in PUNCTUATIONS:
        review = review.replace(punc, " ")
    words = review.split()
    return words


def compute_words(path_pattern):
    words_count = {}
    files = glob(path_pattern)
    for file in files:
        with open(file) as stream:
            content = stream.read()
            content = content.lower()
        words = set(preprocess_review(content))
        for word in set(words):
            words_count[word] = words_count.get(word, 0) + 1
    return words_count


def get_review():
    comment = input("Enter review: ")
    words = preprocess_review(comment)
    return words


def compute_sentiment(words, words_count_pos, words_count_neg, debug=False):
    sentence_sentiment = 0
    for word in words:
        positive = words_count_pos.get(word, 0)
        negative = words_count_neg.get(word, 0)
        all_ = positive + negative
        if all_ == 0:
            word_sentiment = 0
        else:
            word_sentiment = (positive - negative) / all_
        if debug:
            print(f"{word} --> sentiment = {word_sentiment}")
        sentence_sentiment += word_sentiment
    if len(words) > 0:
        sentence_sentiment /= len(words)
    else:
        sentence_sentiment = 0
    return sentence_sentiment


def print_sentiment(sentiment):
    if sentiment > 0:
        label = "positive"
    elif sentiment < 0:
        label = "negative"
    else:
        label = "neutral"
    print("------------------------------------------------------------")
    print(f"Entered review is {label}. Sentiment = {sentiment}")


def main():
    words = get_review()
    words_count_pos = compute_words(POSITIVE_PATTERN)
    words_count_neg = compute_words(NEGATIVE_PATTERN)
    review_sentiment = compute_sentiment(words, words_count_pos, words_count_neg, debug=True)
    print_sentiment(review_sentiment)


if __name__ == '__main__':
    main()
