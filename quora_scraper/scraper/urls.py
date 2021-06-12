from django.urls import path

from . import views

app_name = 'scraper'

urlpatterns = [
    path('', views.SearchQueryView.as_view(), name='search_query'),
]