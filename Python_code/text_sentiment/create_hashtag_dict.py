"""
Combines all the sentiment dictionaries into one file to use in parsing
hashtags (because other words don't matter)
"""

from Python_code.text_sentiment import compare_sentiments as cs

# words are keys
afinn_dict = cs.load_afinn_dictionary('AFINN-111.txt')
hului_dict = cs.load_huliu_dict('hu_liu/opinion-lexicon-English/')
vader_dict = cs.vader.make_lex_dict('vader/vader_sentiment_lexicon.txt')

sentiment_words = []

for key in afinn_dict:
    sentiment_words.append(key)
for key in hului_dict:
    if key not in sentiment_words:
        sentiment_words.append(key)
for key in vader_dict:
    if key not in sentiment_words:
        sentiment_words.append(key)

sentiment_words.sort()

with open('hashtag_dict.txt', 'w') as file:
    for word in sentiment_words:
        file.write(word + '\n')

