from django.http import Http404
from rest_framework.decorators import api_view

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from API.serializers import ArticlesSerializer, StatsSerializer
from crawler.models import Article, Author
from crawler.functionality import Scrapper


class GetAllArticles(generics.ListAPIView):
    serializer_class = ArticlesSerializer
    queryset = Article.objects.all()
    fields = "__all__"


class AuthorList(APIView):
    def get(self, request):
        authors = Author.objects.all().exclude(full_name="total")
        authors_dict = dict()
        for author in authors:
            authors_dict[author.author_uri] = author.full_name
        return Response(authors_dict)


class StatsList(APIView):
    def get(self, request):
        stats = Author.objects.get(full_name="total")
        serializer = StatsSerializer(stats)
        return Response(serializer.data["top_used_words"])


class AuthorStatsDetail(APIView):
    def get_object(self, author):
        try:
            return Author.objects.get(author_uri=author)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, author):
        author = self.get_object(author)
        serializer = StatsSerializer(author)
        return Response(serializer.data["top_used_words"])
