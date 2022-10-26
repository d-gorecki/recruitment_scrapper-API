from django.urls import path, include
from API import views

urlpatterns = [
    path("articles/", views.GetAllArticles.as_view()),
    path("stats/", views.StatsList.as_view()),
    path("authors/", views.AuthorList.as_view()),
    path("stats/<str:author>/", views.AuthorStatsDetail.as_view()),
]
