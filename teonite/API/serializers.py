from rest_framework import serializers
from crawler.models import Article, Author


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["top_used_words"]
