import time
import nltk
import logging
from nltk.corpus import wordnet as wn

class WordNetFunctionality:

    def __init__(self):
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def get_baseform(self, word, pos):
        baseform = self.lemmatizer.lemmatize(word, pos=pos)
        return baseform
        
    def check_hypernym_tree(self, word, pos, words_to_check):
        synsets = wn.synsets(word, pos=pos)
        for syn in synsets:
            hypernyms = self.get_all_hypernyms(syn)
            if any(hyper.lemmas()[0].name() in words_to_check for hyper in hypernyms):
                return True
        return False

    def get_all_hypernyms(self, synset):
        hypernyms = set()
        self.gather_hypernyms(synset, hypernyms)
        return hypernyms

    def gather_hypernyms(self, synset, hypernyms):
        for hypernym in synset.hypernyms():
            hypernyms.add(hypernym)
            self.gather_hypernyms(hypernym, hypernyms)
            
    def deriveVerb(self, noun):
        if not noun: 
            return ""
        lemma = self.lemmatizer.lemmatize(noun, pos=wn.NOUN)
        logging.info(f"{lemma=}")
        if not lemma: 
            return ""
        syn = wn.synsets(lemma, pos=wn.VERB)
        logging.info(f"{syn=}")
        if syn:
            return syn[0].name().split(".")[0]
        return ""

if __name__ == "__main__":
    wnf = WordNetFunctionality()
    start = time.monotonic()
    print(wnf.check_hypernym_tree("secretary", "n", ["person", "social_group"]))
    print(f"Time: {time.monotonic() - start} ms")