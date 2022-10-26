import string
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

from bs4 import BeautifulSoup, PageElement
from requests import get, Response
from crawler.models import Article, Author


class Scrapper:
    """Scrapper class responsible for performing web scrapping actions (based on BeautifulSoup package), calculating
    top used words and populating database with sourced data"""

    URL: str = "https://teonite.com/blog/"
    article_list: Response = get(URL)
    bs: BeautifulSoup = BeautifulSoup(article_list.content, features="html.parser")

    def get_content(self) -> list[dict[str, str]]:
        """Gets data from URL with the use of BeautifulSoup methods and returns processed data in form of list of
        dictionaries consisting of author, ttle and content"""
        article_data = []
        for article in Scrapper.bs.find("div", class_="post-cards").find_all("article"):
            title_anchor: PageElement = article.find("a", class_="title", href=True)
            title: str = title_anchor.get_text()
            article_detail: Response = get("https://teonite.com" + title_anchor["href"])
            bs_article: BeautifulSoup = BeautifulSoup(
                article_detail.content, features="html.parser"
            )
            article_content: str = ""
            for p in bs_article.find("article", class_="post-content").find_all("p"):
                article_content += p.get_text()
            author: PageElement = article.find("span", class_="author").get_text()
            article_data.append(
                {"author": author, "title": title, "content": article_content}
            )

        return article_data

    def populate_article_table(self, arr: list) -> None:
        """Save passed data ino Article table of database"""
        for elem in arr:
            db_article: Article = Article.objects.filter(
                author=elem.get("author"), title=elem.get("title")
            )
            if not db_article:  # Checks if DB has not been populated previously
                Article.objects.create(
                    author=elem.get("author"),
                    title=elem.get("title"),
                    content=elem.get("content"),
                )

    def populate_author_table(self, top_words_dict: dict[str, int]):
        """Save passed data ino Author table of database"""
        for full_name, top_used_words in top_words_dict.items():
            author: Author = Author.objects.filter(
                full_name=full_name
            )  # Checks if DB has not been populated previously
            if not author:
                Author.objects.create(
                    full_name=full_name,
                    author_uri="".join(full_name.strip().lower().split(" ")),
                    top_used_words=top_used_words,
                )

    def remove_stop_words(self, sentence: str) -> str:
        """Remove stop words from passed string using nltk"""
        stop_words: set = set(stopwords.words("english"))
        word_tokens: list[str] = word_tokenize(sentence)
        filtered_sentence: list = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        return " ".join(filtered_sentence)

    def return_words_dict(self, sentence: str) -> dict[str, int]:
        """Returns dictionary in form of word: occurrence_number"""
        sentence: str = self.remove_stop_words(sentence)
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

    def calculate_10_most_common_words(self, author: str) -> dict[str, int]:
        if author == "total":
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=author)
        sentence: str = ""
        for article in articles:
            sentence: str = sentence + article.content

        dictionary: dict[str, int] = self.return_words_dict(sentence)
        sorted_dictionary: itertools.islice = itertools.islice(
            {
                k: v
                for k, v in sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
            }.items(),
            10,
        )
        return dict(sorted_dictionary)
