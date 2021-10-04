from django.shortcuts import render

from articleapp.models import ArticleModel


def index(request):
    new_post = ArticleModel.new_articles.first()
    top = ArticleModel.top.all()
    context = {'title': 'Ashtray Magazine',
               'top': top,
               'new_post': new_post
               }
    return render(request, 'base/index.html', context)


def contact(request):
    return render(request, 'base/contacts.html', {'title': 'Контакты'})