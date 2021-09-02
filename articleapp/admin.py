from django.contrib import admin
from .models import Genres, ArticleDataModel, ArticleModel, Author, ModelLikesArticle
# Register your models here.

admin.site.register(Genres)
admin.site.register(Author)
admin.site.register(ArticleModel)
admin.site.register(ArticleDataModel)
admin.site.register(ModelLikesArticle)
