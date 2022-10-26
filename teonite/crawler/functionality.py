import string
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

from bs4 import BeautifulSoup
from requests import get, Response
from crawler.models import Article, Author
from collections import OrderedDict


class Scrapper:
    URL: str = "https://teonite.com/blog/"
    article_list: Response = get(URL)
    bs = BeautifulSoup(article_list.content, features="html.parser")

    def get_content(self):
        article_data = []
        for article in Scrapper.bs.find("div", class_="post-cards").find_all("article"):
            title_anchor = article.find("a", class_="title", href=True)
            title = title_anchor.get_text()
            article_detail = get("https://teonite.com" + title_anchor["href"])
            bs_article = BeautifulSoup(article_detail.content, features="html.parser")
            article_content = ""
            for p in bs_article.find("article", class_="post-content").find_all("p"):
                article_content += p.get_text()
            author = article.find("span", class_="author").get_text()
            article_data.append(
                {"author": author, "title": title, "content": article_content}
            )

        return article_data

    def populate_article_table(self, arr):
        for elem in arr:
            db_article = Article.objects.filter(
                author=elem.get("author"), title=elem.get("title")
            )
            if not db_article:  # Checks if DB has not been populated previously
                Article.objects.create(
                    author=elem.get("author"),
                    title=elem.get("title"),
                    content=elem.get("content"),
                )

    def populate_author_table(self, top_words_dict):
        for full_name, top_used_words in top_words_dict.items():
            author = Author.objects.filter(
                full_name=full_name
            )  # Checks if DB has not been populated previously
            if not author:
                Author.objects.create(
                    full_name=full_name,
                    author_uri="".join(full_name.strip().lower().split(" ")),
                    top_used_words=top_used_words,
                )

    def remove_stop_words(self, sentence):
        stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(sentence)
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        return " ".join(filtered_sentence)

    def return_words_dict(self, sentence):
        sentence = self.remove_stop_words(sentence)
        for sign in string.punctuation + "’“”—":
            sentence = sentence.replace(sign, "")
        words = dict()
        sentence = sentence.lower().strip().split(" ")
        for word in list(filter(None, sentence)):
            if word in words.keys():
                words[word] += 1
            else:
                words[word] = 1

        return words

    def calculate_10_most_common_words(self, author):
        if author == "total":
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=author)
        sentence = ""
        for article in articles:
            sentence = sentence + article.content

        dictionary = self.return_words_dict(sentence)
        sorted_dictionary = itertools.islice(
            {
                k: v
                for k, v in sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
            }.items(),
            10,
        )
        return dict(sorted_dictionary)
