from glob import glob

POSITIVE_TRAINING_FILES = glob(r".\data\pos\*.txt")
NEGATIVE_TRAINING_FILES = glob(r".\data\neg\*.txt")
CHARACTERS_TO_REMOVE = ("<br>", "<br/>", "<br />", ".", ",", "?", "!",
                        "-", '"', "", "(", ")", ":", ";", "-", "+",
                        "=", "/", "§", "*", "¡", "¦", "\\x91", "\\x97")
POSITIVE_WORDS_DICT = {}
NEGATIVE_WORDS_DICT = {}

for positive_file in POSITIVE_TRAINING_FILES:
    with open(positive_file, 'r') as pos_stream:
        pos_content = pos_stream.read()
        pos_content = pos_content.lower()

    for char in CHARACTERS_TO_REMOVE:
        pos_content = pos_content.replace(char, " ")

    POSITIVE_WORDS_SET = set(pos_content.split())

    for pos_word in POSITIVE_WORDS_SET:
        POSITIVE_WORDS_DICT[pos_word] = POSITIVE_WORDS_DICT.get(pos_word, 0) + 1

for negative_file in NEGATIVE_TRAINING_FILES:
    with open(negative_file, 'r') as neg_stream:
        neg_content = neg_stream.read()
        neg_content = neg_content.lower()

    for char in CHARACTERS_TO_REMOVE:
        neg_content = neg_content.replace(char, " ")

    NEGATIVE_WORDS_SET = set(neg_content.split())

    for neg_word in NEGATIVE_WORDS_SET:
        NEGATIVE_WORDS_DICT[neg_word] = NEGATIVE_WORDS_DICT.get(neg_word, 0) + 1

comment = input("Enter movie review, please: ")
print()

for char in CHARACTERS_TO_REMOVE:
    comment = comment.lower().replace(char, " ")

words = comment.split()
positive = 0
negative = 0
word_sentiment_sum = 0

for word in words:
    positive = POSITIVE_WORDS_DICT.get(word, 0)
    negative = NEGATIVE_WORDS_DICT.get(word, 0)
    all_ = positive + negative

    if all_ != 0:
        word_sentiment = (positive - negative) / all_
    else:
        word_sentiment = 0
    word_sentiment_sum += word_sentiment

    print(f"{word} --> sentiment = {word_sentiment}")

comment_sentiment = word_sentiment_sum / len(words)

if comment_sentiment > 0:
    sentiment = "positive"
elif comment_sentiment < 0:
    sentiment = "negative"
else:
    sentiment = "neutral"

print()
print(f"Entered review is {sentiment}. Sentiment = {comment_sentiment}")
