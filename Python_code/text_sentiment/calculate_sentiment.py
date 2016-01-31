"""
Routines to calculate sentiment for a specific tweet
"""

try:
    from Python_code.text_sentiment.vader import vader as vs
except:
    import vader.vader as vs
try:
    from Python_code.text_sentiment import split_hashtag as sh
except:
    import split_hashtag as sh


def vader_sentiment(tweet_text):
    return vs.sentiment(tweet_text)


def generic_sentiment(tweet_text, sent_dict):
    """
    Uses any given sentiment dictionary to calculate a sentiment value
    :param tweet_text:
    :param sent_dict:
    :return:
    """
    sentiment = 0
    for word in tweet_text.split():
        if word.lower() in sent_dict:
            sentiment += sent_dict[word.lower()]
    return sentiment


def create_sentiment_dictionary(sentiment_file_location, splitter='\t'):
    """
    Creates a sentiment dictionary based on a text file
    dictionary needs to be lines of term and sentiment score
    :param sentiment_file_location: string with location of sentiment data
    :param splitter: text of character to split on = default is tab
    :return sentiment_dictionary: dictionary
    """
    sentiment_file = open(sentiment_file_location)
    sentiment_dictionary = {}
    for line in sentiment_file:
        term, score = line.split(splitter)
        sentiment_dictionary[term] = float(score)
    sentiment_file.close()
    return sentiment_dictionary


def test():
    sample_test = ["when meghan doesnt know how to use her computer https://t.co/Qi34ysqGLa",
                   "#KendrickJohnson values, she's related to Eric Sheppard since she's threatening mutilation? Eric wants to decapitate https://t.co/JtYURg7fXP",
                   "When he's handsome and a scholar lol https://t.co/hUmMInfzt6",
                   "I love streets with no rush, specially in night. https://t.co/GzDFAybttK",
                   "#makeAmericaGreatLikeGermany On to victory! #DonaldTrump2016: https://t.co/c3uLw9rrUZ https://t.co/0b1HCh8jC0",
                   "Way to go D!  Keep it up! https://t.co/chDv9Emq4v",
                   'BING AND GRONDAHL B &amp; G "WHO IS CALLING" PORCELAIN FIGURE FIGURINE #2251  https://t.co/QUCt8erIT3 https://t.co/Qm5coKVUk8',
                   'Look at this idiot https://t.co/yCrRlpE12X']
    word_list = sh.english_word_list()
    afinn_dict = create_sentiment_dictionary('text_sentiment/AFINN-111.txt')
    for text in sample_test:
        cleaned_text = sh.parse_sentence(text, word_list)
        print(text)
        print(vader_sentiment(text))
        print(generic_sentiment(text, afinn_dict))
        print(cleaned_text)
        print(vader_sentiment(cleaned_text))
        print(generic_sentiment(cleaned_text, afinn_dict))


if __name__ == '__main__':
    test()