from django.shortcuts import render


def index(request):
    return render(request, 'base/index.html', {'title': 'Ashtray Magazine'})


def contact(request):
    return render(request, 'base/contacts.html', {'title': 'Контакты'})