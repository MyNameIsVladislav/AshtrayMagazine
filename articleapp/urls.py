from django.urls import path

from articleapp.views import ArticleListView, ArticleGenresListView, ArticlePageView, add_like

app_name = 'articleapp'

urlpatterns = [
    path('', ArticleListView.as_view(), name='all'),
    path('<slug:slug_genres>', ArticleGenresListView.as_view(), name='genres'),
    path('page/<slug:slug>', ArticlePageView.as_view(), name='article'),
    path('likes/', add_like, name='likes')
]
