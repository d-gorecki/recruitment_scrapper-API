import string
import itertools

from bs4 import BeautifulSoup
from requests import get, Response
from crawler.models import Article


class Scrapper:
    URL: str = "https://teonite.com/blog/"
    article_list: Response = get(URL)
    bs = BeautifulSoup(article_list.content, features="html.parser")

    @staticmethod
    def get_content():
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

    @staticmethod
    def populate_database(arr):
        for elem in arr:
            db_article = Article.objects.filter(
                author=elem.get("author"), title=elem.get("title")
            )
            if not db_article:
                Article.objects.create(
                    author=elem.get("author"),
                    title=elem.get("title"),
                    content=elem.get("content"),
                )

    @staticmethod
    def return_words_dict(sentence):
        sentence = sentence
        for sign in string.punctuation:
            sentence = sentence.replace(sign, " ")
        words = dict()
        for word in sentence.lower().strip().split(" "):
            if word in words.keys():
                words[word] += 1
            else:
                words[word] = 1

        return words

    @staticmethod
    def calculate_10_most_common_words():
        articles = Article.objects.all()
        sentence = ""
        for article in articles:
            sentence = sentence + article.content

        dictionary = Scrapper.return_words_dict(sentence)
        sorted_dictionary = itertools.islice(
            {
                k: v
                for k, v in sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
            }.items(),
            1,
            11,
        )

        return dict(sorted_dictionary)
