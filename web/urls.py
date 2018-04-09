from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name='blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    re_path('^article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='detail'),
    re_path('^category/(?P<name>.+)/$', views.ArticleByCategoryView.as_view(), name='category'),
    path('archives/', views.ArchivesView.as_view(), name='archives'),
    re_path('^archives/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.ArchivesByMonthView.as_view(), name='archives_month'),
    re_path('^tags/$', views.tags, name='tags'),
    re_path('^tags/(?P<name>.+)/$', views.TagDetail.as_view(), name='tag_detail'),
    re_path('^about/$', views.about, name='about'),
]