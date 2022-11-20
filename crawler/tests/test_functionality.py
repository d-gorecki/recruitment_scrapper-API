from unittest import TestCase

from crawler.functionality import Scrapper
from crawler.models.article import Article


class TestFunctionality(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scrapper = Scrapper()
        cls.articles_count = Article.objects.count()

    def test_remove_stop_words(self):
        input = "some a an or text him himself yours if into"
        expected = "text"
        actual = self.scrapper.remove_stop_words(input)
        self.assertEqual(actual, expected)

    def test_return_words_dict(self):
        input = "Some some SomE sentence 123 an example"
        expected = {"sentence": 1, "123": 1, "example": 1}
        actual = self.scrapper.return_words_dict(input)
        self.assertEqual(actual, expected)
