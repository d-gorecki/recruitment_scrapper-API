from django.db.models import QuerySet
from django.http import Http404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from API.serializers import ArticlesSerializer, StatsSerializer
from crawler.models import Article, Author


class GetAllArticles(generics.ListAPIView):
    """Additional view providing API for all data scrapped from given URL"""

    serializer_class: ArticlesSerializer = ArticlesSerializer
    queryset: QuerySet[Article] = Article.objects.all()
    fields: str = "__all__"


class AuthorList(APIView):
    """API providing authors credentials in format Full Name: fullname"""

    def get(self, request) -> Response:
        authors: QuerySet[Author] = Author.objects.all().exclude(full_name="total")
        authors_dict: dict = dict()
        for author in authors:
            authors_dict[author.author_uri] = author.full_name
        return Response(authors_dict)


class StatsList(APIView):
    """API providing stats (top used words) for all authors/all articles"""

    def get(self, request) -> Response:
        stats: Author = Author.objects.get(full_name="total")
        serializer: StatsSerializer = StatsSerializer(stats)
        return Response(serializer.data["top_used_words"])


class AuthorStatsDetail(APIView):
    """API view providing stats (top used words) for passed author"""

    def get_object(self, author: str) -> Author | Http404:
        """Return Author obj based on passed str or raise Http404 error"""
        try:
            return Author.objects.get(author_uri=author)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, author) -> Response:
        author: Author = self.get_object(author)
        serializer: StatsSerializer = StatsSerializer(author)
        return Response(serializer.data["top_used_words"])
