from django.apps import AppConfig
from django.db.models.signals import post_migrate


def call_scrapper_methods(sender, **kwargs):
    from crawler.functionality import Scrapper

    scrapper: Scrapper = Scrapper()
    scrapper_content: list[dict[str, str]] = scrapper.get_content()
    scrapper.populate_article_table(scrapper_content)
    author_list: list[str] = ["total"]

    for elem in scrapper_content:
        author_list.append(elem.get("author"))

    author_top_words: dict = dict()
    for author in set(author_list):
        author_top_words[author] = scrapper.calculate_10_most_common_words(author)

    scrapper.populate_author_table(author_top_words)


class CrawlerConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "crawler"

    def ready(self):
        """Method creates Scrapper out which carries out web scrapping, calculating top used words and populating
        database"""
        post_migrate.connect(call_scrapper_methods, sender=self)
