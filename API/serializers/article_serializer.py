from rest_framework import serializers

from crawler.models.article import Article


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "author",
            "title",
            "content",
        )
