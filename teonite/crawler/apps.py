from django.apps import AppConfig


class CrawlerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "crawler"

    def ready(self):
        from crawler.functionality import Scrapper

        Scrapper.populate_database(Scrapper.get_content())
