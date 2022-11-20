from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=100, help_text="Full name")
    author_uri = models.CharField(max_length=100, help_text="Full name")
    top_used_words = models.JSONField(help_text="Top used words by author")
