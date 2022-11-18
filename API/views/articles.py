from django.db.models import QuerySet
from rest_framework import generics

from API.serializers.article_serializer import ArticlesSerializer
from crawler.models.article import Article


class ArticlesListView(generics.ListAPIView):
    """Additional view providing API for all data scrapped from given URL"""

    serializer_class: ArticlesSerializer = ArticlesSerializer
    queryset: QuerySet[Article] = Article.objects.all()
