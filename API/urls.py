from django.urls import path, include
from API.views.authors import AuthorsSlugListView, AuthorStatsView, TotalStatsListView
from API.views.articles import ArticlesListView


urlpatterns = [
    path("articles/", ArticlesListView.as_view(), name="articles"),
    path("stats/", TotalStatsListView.as_view(), name="stats"),
    path("authors/", AuthorsSlugListView.as_view(), name="authors"),
    path("stats/<str:author>/", AuthorStatsView.as_view(), name="stats-author"),
]
