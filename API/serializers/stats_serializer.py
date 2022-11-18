from rest_framework import serializers

from crawler.models.author import Author


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("top_used_words",)
        read_only_fields = fields
