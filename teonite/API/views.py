from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes

from rest_framework import generics

from rest_framework.response import Response

from API.serializers import ArticlesSerializer
from crawler.models import Article
from crawler.functionality import Scrapper


class GetAllArticles(generics.ListAPIView):
    serializer_class = ArticlesSerializer
    queryset = Article.objects.all()
    fields = "__all__"


@api_view(["GET"])
def get_stats(request):
    dict_ = Scrapper.calculate_10_most_common_words()
    return Response(dict_)
