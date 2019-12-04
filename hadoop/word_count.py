"""The classic MapReduce job: count the frequency of words.
"""
from mrjob.job import MRJob
import re
import string
WORD_RE = re.compile(r"[\w']+")


class MRWordFreqCount(MRJob):

    def mapper(self, _, line):
        line = line.strip().lower().translate(str.maketrans('', '', string.punctuation))
        words = line.split()
        for word in words:
            if word.isalpha():
                yield (word, 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))


if __name__ == '__main__':
     MRWordFreqCount.run()
