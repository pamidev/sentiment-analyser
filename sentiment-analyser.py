from glob import glob

POSITIVE_TRAINING_FILES = glob(r".\data\pos\*.txt")
NEGATIVE_TRAINING_FILES = glob(r".\data\neg\*.txt")
CHARACTERS_TO_REMOVE = ("<br>", "<br/>", "<br />", ".", ",", "?", "!",
                        "-", '"', "", "(", ")", ":", ";", "-", "+",
                        "=", "/", "§", "*", "¡", "¦", "\\x91", "\\x97")
POSITIVE_WORDS_LISTS = []
NEGATIVE_WORDS_LISTS = []

for positive_file in POSITIVE_TRAINING_FILES:
    with open(positive_file, 'r') as pos_stream:
        pos_content = pos_stream.read()
        pos_content = pos_content.lower()

    for char in CHARACTERS_TO_REMOVE:
        pos_content = pos_content.replace(char, " ")

    POSITIVE_WORDS_LISTS.append(pos_content.split())

for negative_file in NEGATIVE_TRAINING_FILES:
    with open(negative_file, 'r') as neg_stream:
        neg_content = neg_stream.read()
        neg_content = neg_content.lower()

    for char in CHARACTERS_TO_REMOVE:
        neg_content = neg_content.replace(char, " ")

    NEGATIVE_WORDS_LISTS.append(neg_content.split())

comment = input("Enter comment, please: ").lower()

for char in CHARACTERS_TO_REMOVE:
    comment = comment.replace(char, " ")

words = comment.split()
positive = 0
negative = 0
word_sentiment_sum = 0

for word in words:
    for positive_comment in POSITIVE_WORDS_LISTS:
        if word in positive_comment:
            positive += 1
    for negative_comment in NEGATIVE_WORDS_LISTS:
        if word in negative_comment:
            negative += 1

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
print(f"Entered sentence is {sentiment}. Sentiment = {comment_sentiment}\n")
