from django.contrib import admin
from .models import Genres, ArticleModel, Author, ModelLikesArticle, CommentsModel, ModelLikesComment
from django.utils.safestring import mark_safe
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CategoriesFilter(admin.SimpleListFilter):
    title = 'genres'
    parameter_name = 'genres_id'

    def lookups(self, request, model_admin):
        return set([(genre.slug, genre.name) for genre in Genres.objects.all()])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(genres_id__slug=self.value())


class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(label='Описание',
                           widget=CKEditorUploadingWidget())

    class Meta:
        model = ArticleModel
        fields = '__all__'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name')
    list_display_links = ('user_id', 'full_name')
    readonly_fields = ('full_name',)


class CommentInline(admin.TabularInline):
    model = CommentsModel
    extra = 1


@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'id', 'title', 'owner_id',
                    'created_at',
                    'updated_at', 'publish', 'is_active')
    list_display_links = ('id', 'title')
    list_filter = ('owner_id', CategoriesFilter)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'owner_id',)
    inlines = [CommentInline]
    form = ArticleAdminForm
    save_on_top = True
    readonly_fields = ('get_image',)
    actions = ['activate', 'no_activate']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.img_mini.url} width="50" height="60">')

    get_image.short_description = 'Image'

    def activate(self, request, queryset):
        """Опубликовано"""
        row_update = queryset.update(is_active=True)
        self.message_user(request, f'записей опубликовано: {row_update}')

    def no_activate(self, request, queryset):
        """Снять публикацию"""
        row_update = queryset.update(is_active=False)
        self.message_user(request, f'записей снято: {row_update}')

    activate.short_description = 'Опубликовать'
    activate.allowed_permissions = ('change',)

    no_activate.short_description = 'Снять публикации'
    no_activate.allowed_permissions = ('change',)


@admin.register(ModelLikesArticle)
class LikesArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('user_id', 'article_id')


@admin.register(CommentsModel)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'article_id', 'text', 'status')
    readonly_fields = ('user_id', 'article_id')


@admin.register(ModelLikesComment)
class LikesCommentsAdmin(admin.ModelAdmin):
    readonly_fields = ('user_id', 'article_id', 'comment_id')
