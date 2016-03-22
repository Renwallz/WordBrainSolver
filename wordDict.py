#! /usr/bin/python3

import re


def clean_word_generator(filename):
    with open(filename) as f:
        for word in f:
            word = word.strip()
            word = word.lower()
            yield word


class WordDict:

    def __init__(self):
        self.words = set()
        for word in clean_word_generator('wordsEn.txt'):
            self.words.add(word)

    def search(self, pattern):
        results = []
        pattern = re.compile('^'+pattern+'$')
        for w in self.words:
            if pattern.match(w):
                results.append(w)
        return results


class _wordtree(object):
    def __init__(self, word=''):
        self.children = {}
        if word != '':
            self.is_word = False
            self.children[word[0]] = _wordtree(word[1:])
        else:
            self.is_word = True

    def add(self, word):
        if word == '':
            self.is_word = True
            return True
        if word[0] in self.children:
            self.children[word[0]].add(word[1:])
        else:
            self.children[word[0]] = _wordtree(word[1:])

    def _yield_words(self, prefix=None, starting_prefix=None):
        if starting_prefix is not None and len(starting_prefix) > 0:
            l = starting_prefix.pop(0)
            prefix.append(l)
            yield from self.children[l]._yield_words(prefix, starting_prefix)
        else:
            if self.is_word:
                yield ''.join(prefix)
            for l in self.children:
                prefix.append(l)
                yield from self.children[l]._yield_words(prefix)
                prefix.pop()


class wordtree(_wordtree):
    def __init__(self, dictionary='wordsEn.txt'):
        super().__init__()
        for word in clean_word_generator(dictionary):
            self.add(word)

    def yield_words(self, starting_prefix=None):
        if starting_prefix is None:
            for l in self.children:
                yield from self.children[l]._yield_words(prefix=[l])
        else:
            starting_prefix = list(starting_prefix)
            l = starting_prefix.pop(0)
            yield from self.children[l]._yield_words(
                    prefix=[l], starting_prefix=starting_prefix)

    def __contains__(self, word):
        node = self
        for letter in word:
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_word

    def prefix_valid(self, prefix):
        node = self
        for letter in prefix:
            if letter not in node.children:
                return False
            node = node.children[letter]
        return True

if __name__ == '__main__':
    d = WordDict()
    while (1):
        print(d.search(input("->")))

