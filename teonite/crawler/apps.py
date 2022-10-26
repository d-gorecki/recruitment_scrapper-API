from django.apps import AppConfig


class CrawlerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "crawler"

    def ready(self):

        from crawler.functionality import Scrapper

        scrapper = Scrapper()
        scrapper_content = scrapper.get_content()
        scrapper.populate_article_table(scrapper_content)
        author_list = ["total"]

        for elem in scrapper_content:
            author_list.append(elem.get("author"))

        author_top_words = dict()
        for author in set(author_list):
            author_top_words[author] = scrapper.calculate_10_most_common_words(author)

        scrapper.populate_author_table(author_top_words)
