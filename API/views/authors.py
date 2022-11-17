from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from API.serializers.stats_serializer import StatsSerializer
from crawler.models.author import Author


class TotalStatsListView(APIView):
    """API providing stats (top used words) for all authors/all articles"""

    def get(self, request) -> Response:
        stats: Author = Author.objects.get(full_name="total")
        serializer: StatsSerializer = StatsSerializer(stats)
        return Response(serializer.data["top_used_words"])


class AuthorStatsView(APIView):
    """API view providing stats (top used words) for passed author"""

    def get(self, request, author) -> Response:
        author: Author = get_object_or_404(Author, author_uri=author)
        serializer: StatsSerializer = StatsSerializer(author)
        return Response(serializer.data["top_used_words"])


class AuthorsSlugListView(APIView):  # -> AuthorViewSet
    """API view providing authors credentials in format Full Name: fullname"""

    def get(self, request) -> Response:
        authors: QuerySet[Author] = Author.objects.all().exclude(full_name="total")
        authors_dict: dict = dict()
        for author in authors:
            authors_dict[author.author_uri] = author.full_name
        return Response(authors_dict)
