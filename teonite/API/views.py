from rest_framework import generics
from API.serializers import ArticlesSerializer
from crawler.models import Article


class GetAllArticles(generics.ListAPIView):
    serializer_class = ArticlesSerializer
    queryset = Article.objects.all()
    fields = "__all__"
