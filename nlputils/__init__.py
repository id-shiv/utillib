from nltk.corpus import wordnet as wn

poses = {'n': 'noun',
         'v': 'verb',
         's': 'adj (s)',
         'a': 'adj',
         'r': 'adv'}


def get_synonyms(word):
    __synonyms = list()
    for synset in wn.synsets(word.lower()):
        __synonym = dict()
        __synonym[poses[synset.pos()]] = ", ".join([l.name() for l in synset.lemmas()])
        __synonyms.append(__synonym)

    return __synonyms


def get_hypernyms(word, pos='n', n='01'):
    try:
        __synset_of = word + '.' + pos + '.' + n
        __synset = wn.synset(__synset_of)
        return list(__synset.closure(lambda s: s.hypernyms()))
    except BaseException as be:
        print(be)


def main():
    synonyms = get_synonyms('test')
    print(synonyms)

    hypernyms = get_hypernyms('testing', pos='n', n='03')
    print(hypernyms)


# Word representations
#   One-hot vectors
#       Word represented by 1
#   Word vectors / Word embedding
#       Word represnted by vectors, distributed.

main()
