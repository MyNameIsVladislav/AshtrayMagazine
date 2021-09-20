from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import ugettext as _

from core.settings import AUTH_USER_MODEL


def choose_path(instance, filename: str):
    return f'root_file/articles/{instance.slug}/{filename}'


class Author(models.Model):
    user_id = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('authors'))

    def __str__(self):
        return f'{self.user_id.last_name}'

    @property
    def full_name(self):
        return f'{self.user_id.first_name} {self.user_id.last_name} '


class Genres(models.Model):
    class Meta:
        ordering = ('name',)
    name = models.CharField(verbose_name=_('genre'), max_length=16)
    slug = models.SlugField(verbose_name=_('slug'))

    def __str__(self):
        return f'{self.name} - {self.pk}'

    def get_absolute_url(self):
        return reverse('art:genres', kwargs={'slug_genre': self.slug})


class ContentQuerySet(models.QuerySet):
    def new_content(self):
        return self.order_by('publish')[0]


class TopContent(models.QuerySet):
    def get_top(self):
        return self.raw("""
                select * from articleapp_articlemodel aa  where aa.id in (select a.id from articleapp_articlemodel a
                left join articleapp_modellikesarticle am
                on am.article_id_id = a.id
                left join authapp_user ac
                on ac.id = am.user_id_id
                group by a.id order by count(am.id) desc  limit 3)""")


class ArticleModel(models.Model):
    class Meta:
        ordering = ('-publish',)

    title = models.CharField(max_length=70, verbose_name=_('title'), default=_('Not found'))
    short_describe = models.TextField(verbose_name=_('short describe'), max_length=150, default=_('Not Found'))
    owner_id = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,
                                 verbose_name=_('owner'), related_name='owner')
    genres_id = models.ManyToManyField(Genres, related_name='genres', related_query_name='genre')
    slug = models.SlugField(max_length=70, unique_for_date='publish')
    text = models.TextField(verbose_name=_('text'), null=True)
    img_mini = models.ImageField(upload_to=choose_path, verbose_name=_('image mini'))
    img_main = models.ImageField(upload_to=choose_path, verbose_name=_('image main'))

    is_active = models.BooleanField(verbose_name='active', default=True)
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    new_articles = ContentQuerySet.as_manager()
    top = TopContent().as_manager()

    def __str__(self):
        return f'{self.title} - {self.pk}'

    def get_absolute_url(self):
        return reverse('art:article', kwargs={'slug': self.slug})


class ArticleUserModel(models.Model):
    class Meta:
        abstract = True

    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name=_('user'), related_query_name='users')
    article_id = models.ForeignKey('ArticleModel', on_delete=models.CASCADE,
                                   verbose_name=_('article'), related_query_name='arts')
    status = models.BooleanField(verbose_name='status', max_length=5, default=True)

    def __str__(self):
        return f'{self.user_id.first_name} {self.user_id.last_name} - comment {self.id}'


class ModelLikesArticle(ArticleUserModel):
    class Meta:
        unique_together = (("user_id", "article_id"),)


class CommentsModel(ArticleUserModel):
    class Meta:
        ordering = ('created_at',)

    text = models.TextField(verbose_name=_('comment'), max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user_id.first_name} - date: {self.created_at}'


class ModelLikesComment(ArticleUserModel):
    class Meta:
        unique_together = (("user_id", "comment_id"),)

    comment_id = models.ForeignKey(CommentsModel, on_delete=models.CASCADE)
