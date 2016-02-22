"""
Takes a tweet and does 2 things:
1) removes hyperlinks
2) attempts to parse hashtags into actual words
3) writes new value to database
Code derived from
stackoverflow.com/questions/20516100/term-split-by-hashtag-of-multiple-words
"""


def english_word_list():
    """
    Generates a list of all english words
    option 1: file site is hard-coded for unix-based systems (linux or OSX)
    option 2: words in sentiment dictionaries
    :return english_words: list of english words
    """
    # option 1: all english words
    wordlist = '/usr/share/dict/words'
    # option 2: sentiment words only
    # wordlist = 'hashtag_dict.txt'
    with open(wordlist) as f:
        content = f.readlines()
    english_words = [word.rstrip('\n').lower() for word in content]
    return english_words


def parse_sentence(sentence, wordlist):
    new_sentence = ""  # output
    terms = sentence.split(' ')
    for term in terms:
        if term[:1] == '#':  # this is hashtag, parse it
            new_sentence += parse_tag(term, wordlist) + ' '
        elif term[:4].lower() != 'http':  # Just append the word
            new_sentence += term + ' '
        # new_sentence += " "

    return new_sentence


def parse_tag(term, wordlist):
    words = []
    # Remove hashtag, split by dash
    tags = term[1:].split('-')
    for tag in tags:
        word = find_word(tag, wordlist)
        while word != None and len(tag) > 0:
            words += [word]
            if len(tag) == len(word):  # Special case for when eating rest of word
                break
            tag = tag[len(word):]
            word = find_word(tag, wordlist)
    return " ".join(words)


def find_word(token, wordlist):
    i = len(token) + 1
    while i > 1:
        i -= 1
        if token[:i].lower() in wordlist:
            return token[:i]
    return None


if __name__ == '__main__':
    wordlist = english_word_list()
    sentence = "big #awesome-dayofmylife because #iamgreat"
    print(parse_sentence(sentence, wordlist))
    sentence2 = '#THIsIsMyHashTag'
    print(parse_sentence(sentence2, wordlist))
