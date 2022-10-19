from django.urls import path, include
from API import views

urlpatterns = [
    path("articles/", views.GetAllArticles.as_view(), name="article_list_view"),
    path("stats/", views.get_stats, name="get_stats"),
]
