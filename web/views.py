import markdown
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Article, Tag, MyAuthor


class IndexView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['author'] = MyAuthor.objects.first()

        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        article = super(ArticleDetailView, self).get_object(queryset=None)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

        article.content = md.convert(article.content)
        article.toc = md.toc

        return article


class ArticleByCategoryView(ListView):
    model = Article
    template_name = 'category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        name = self.kwargs.get('name')
        return super(ArticleByCategoryView, self).get_queryset().filter(category__name=name)

    def get_context_data(self, **kwargs):
        context = super(ArticleByCategoryView, self).get_context_data(**kwargs)
        name = self.kwargs.get('name')
        context['name'] = name

        return context


class ArchivesView(ListView):
    model = Article
    template_name = 'archives.html'
    context_object_name = 'articles'
    paginate_by = 10


class ArchivesByMonthView(ListView):
    model = Article
    template_name = 'archives_month.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')

        return super(ArchivesByMonthView, self).get_queryset().filter(add_date__year=year, add_date__month=month)

    def get_context_data(self, **kwargs):
        context = super(ArchivesByMonthView, self).get_context_data(**kwargs)
        context['year'] = self.kwargs.get('year')
        context['month'] = self.kwargs.get('month')

        return context


class TagDetail(ListView):
    model = Article
    template_name = 'tag_detail.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        name = self.kwargs.get('name')
        return super(TagDetail, self).get_queryset().filter(tags__name=name)

    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data()
        context['name'] = self.kwargs.get('name')

        return context


def tags(request):
    tag = Tag.objects.annotate(num_count=Count('article'))
    return render(request, 'tags.html', {'tags': tag})


def about(request):
    return render(request, 'about.html')