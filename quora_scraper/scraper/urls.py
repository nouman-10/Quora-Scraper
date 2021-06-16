from django.urls import path

from . import views

app_name = 'scraper'

urlpatterns = [
    path('', views.SearchQueryView.as_view(), name='search_query'),
    path('questions_stats/', views.QuestionStatsView.as_view(),
         name='questions_stats'),
    path('data_scrape/<int:data_scrape_id>/',
         views.DataScrapeDetailView.as_view(), name='data_scrape'),
    path('data_scrapes/', views.DataScrapesListView.as_view(), name='data_scrapes'),
    path('data_scrape/delete/',
         views.DataScrapeDeleteView.as_view(), name='data_scrape_delete'),
]