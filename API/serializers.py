from rest_framework import serializers

from crawler.models.article import Article
from crawler.models.author import Author


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["author", "title", "content"]


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["top_used_words"]
        read_only_fields = fields
