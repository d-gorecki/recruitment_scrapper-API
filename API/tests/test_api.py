from django.urls import reverse
from rest_framework.test import APITestCase
from API.factories.article_factory import ArticleFactory
from API.factories.author_factory import AuthorFactory
from rest_framework import status


class TestAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        ArticleFactory()
        author = AuthorFactory()

        cls.urls = [
            "/articles/",
            "/authors/",
            "/stats/",
            f"/stats/{author.author_uri}/",
        ]

        cls.named_urls = [
            reverse("articles"),
            reverse("authors"),
            reverse("stats"),
        ]

    def test_API_urls_exists_at_desired_location(self):
        for url in self.urls:
            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)

    def test_API_accessible_by_url_name(self):
        for url in self.named_urls:
            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)

    def test_API_delete_method_returns_method_not_allowed_405(self):
        response = self.client.delete(self.urls[3])
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
