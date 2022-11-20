from django.db import models


class Article(models.Model):
    author = models.CharField(max_length=50, help_text="Author of the article")
    title = models.CharField(max_length=100, help_text="Title of the article")
    content = models.TextField(help_text="Content of the article")
