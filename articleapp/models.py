from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from core.settings import AUTH_USER_MODEL


def choose_path(instance, filename: str):
    return f'root_file/articles/{instance.tag}/{filename}'


class Author(models.Model):
    user_id = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('authors'))

    def __str__(self):
        return f'{self.user_id.last_name}'

    @property
    def full_name(self):
        return f'{self.user_id.first_name} {self.user_id.lat_name} '


class Genres(models.Model):
    name = models.CharField(verbose_name=_('genre'), max_length=16)

    def __str__(self):
        return f'{self.name} - {self.pk}'


class ArticleDataModel(models.Model):
    tag = models.CharField(max_length=20, verbose_name=_('tag'))
    text = models.TextField(verbose_name=_('text'), null=True)
    img_mini = models.ImageField(upload_to=choose_path, verbose_name=_('image mini'))
    img_main = models.ImageField(upload_to=choose_path, verbose_name=_('image main'))

    def __str__(self):
        return f'article file {self.tag} - {self.pk}'


#
class ContentQuerySet(models.QuerySet):
    def new_content(self):
        return self.order_by('publish')[0]


class ContentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().raw("""
                select * from articleapp_articlemodel aa  where aa.id in (select a.id from articleapp_articlemodel a
                left join articleapp_modellikesarticle am
                on am.article_id_id = a.id
                left join authapp_customuser ac
                on ac.id = am.user_id_id
                group by a.id order by count(am.id) desc  limit 3)""")


class ArticleModel(models.Model):
    class Meta:
        ordering = ('-publish',)

    title = models.CharField(max_length=70, verbose_name=_('title'), default=_('Not found'))
    short_describe = models.TextField(verbose_name=_('short describe'), max_length=150, default=_('Not Found'))
    articles_data_id = models.ForeignKey(ArticleDataModel, on_delete=models.SET_NULL,
                                         verbose_name=_('article'), null=True, related_name='article_file')
    owner_id = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,
                                 verbose_name=_('owner'), related_name='owner')
    genres_id = models.ManyToManyField(Genres, related_name='genres', related_query_name='genre')
    slug = models.SlugField(max_length=70, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    new_articles = ContentQuerySet.as_manager()
    top = ContentManager()

    def __str__(self):
        return f'{self.title} - {self.pk}'


class ModelLikesArticle(models.Model):
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name=_('user'), related_query_name='users')
    article_id = models.ForeignKey('ArticleModel', on_delete=models.CASCADE,
                                   verbose_name=_('article'), related_query_name='arts')


class CommentsModel(ModelLikesArticle):
    class Meta:
        ordering = ('created_at',)

    text = models.TextField(verbose_name=_('comment'), max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user_id.name} - date: {self.created_at}'


class ModelLikesComment(ModelLikesArticle):
    comment_id = models.ForeignKey(CommentsModel, on_delete=models.CASCADE)
