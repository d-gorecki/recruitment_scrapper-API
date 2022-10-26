import string
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class Scrapper:
    @staticmethod
    def remove_stop_words(sentence):
        stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(sentence)
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        return " ".join(filtered_sentence)

    @staticmethod
    def return_words_dict(sentence):
        sentence = Scrapper.remove_stop_words(sentence)
        for sign in string.punctuation:
            sentence = sentence.replace(sign, "")
        words = dict()
        sentence = sentence.lower().strip().split(" ")
        for word in list(filter(None, sentence)):
            if word in words.keys():
                words[word] += 1
            else:
                words[word] = 1

        return words

    @staticmethod
    def calculate_10_most_common_words(sentence):
        dictionary = Scrapper.return_words_dict(sentence)
        sorted_dictionary = itertools.islice(
            {
                k: v
                for k, v in sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
            }.items(),
            0,
            10,
        )

        return dict(sorted_dictionary)


sentence = (
    "The deadline was very close. We had to fit all the work in only two weeks, so our team decided to run with "
    "a single bi-weekly design sprint. During that time, we had to prepare not only the wireframes and the "
    "design for both dashboard and the landing page, but also html/css templates and code a simple working "
)

print(Scrapper.calculate_10_most_common_words(sentence))
