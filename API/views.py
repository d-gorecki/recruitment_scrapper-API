from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from API.serializers.article_serializer import ArticlesSerializer
from API.serializers.stats_serializer import StatsSerializer
from crawler.models.author import Author
from crawler.models.article import Article


class GetAllArticles(generics.ListAPIView):
    """Additional view providing API for all data scrapped from given URL"""

    serializer_class: ArticlesSerializer = ArticlesSerializer
    queryset: QuerySet[Article] = Article.objects.all()


class StatsList(APIView):
    """API providing stats (top used words) for all authors/all articles"""

    def get(self, request) -> Response:
        stats: Author = Author.objects.get(full_name="total")
        serializer: StatsSerializer = StatsSerializer(stats)
        return Response(serializer.data["top_used_words"])


class AuthorStatsDetail(APIView):
    """API view providing stats (top used words) for passed author"""

    def get(self, request, author) -> Response:
        author: Author = get_object_or_404(Author, author_uri=author)
        serializer: StatsSerializer = StatsSerializer(author)
        return Response(serializer.data["top_used_words"])


class AuthorList(APIView):  # -> AuthorViewSet
    """API providing authors credentials in format Full Name: fullname"""

    def get(self, request) -> Response:
        authors: QuerySet[Author] = Author.objects.all().exclude(full_name="total")
        authors_dict: dict = dict()
        for author in authors:
            authors_dict[author.author_uri] = author.full_name
        return Response(authors_dict)
