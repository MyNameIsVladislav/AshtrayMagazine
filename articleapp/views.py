from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from articleapp.models import ArticleModel, Genres, CommentsModel, ModelLikesArticle
from articleapp.forms import CommentForm


class ArticleListView(ListView):
    queryset = ArticleModel.objects.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'article/article_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['genres'] = Genres.objects.all()
        return context


class ArticleGenresListView(ListView):
    model = ArticleModel
    template_name = 'article/article_list.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        return ArticleModel.objects.filter(genres_id__slug=self.kwargs['slug_genres'], is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleGenresListView, self).get_context_data(**kwargs)
        context['genres'] = Genres.objects.all()
        return context
    
    def get(self, request, *args, **kwargs):
        if get_object_or_404(Genres, slug=kwargs['slug_genres']):
            return super(ArticleGenresListView, self).get(request, *args, **kwargs)


class ArticlePageView(DetailView, RedirectView):
    model = ArticleModel
    template_name = 'article/detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticlePageView, self).get_context_data(**kwargs)
        context['comments'] = CommentsModel.objects.filter(article_id=context['post'], status=True)
        article_info = {'user_id': self.request.user, 'article_id': context['post']}
        context['total_cost'] = context['post'].modellikesarticle_set.filter(status=True).count()
        if not self.request.user.is_anonymous:
            context['active_like'] = ModelLikesArticle.objects.filter(
                user_id=self.request.user,
                article_id=context['post'],
            ).first()
            context['comment_form'] = CommentForm(initial=article_info)
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@require_POST
def add_like(request):
    post = ArticleModel.objects.get(pk=request.POST.get('article_id'))
    like, status = ModelLikesArticle.objects.get_or_create(user_id=request.user, article_id=post)
    like.status = False if not status and like.status else True
    like.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
