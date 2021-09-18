from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from shopapp.models import Product, Category


class ShowProduct(ListView):
    model = Product
    template_name = 'shop/catalog.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowProduct, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryProduct(ListView):
    model = Product
    template_name = 'shop/catalog.html'
    context_object_name = 'product'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug_cat'], available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryProduct, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/product.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if get_object_or_404(Category, slug=kwargs['slug_cat']):
            return super(ProductDetail, self).get(request, *args, **kwargs)
        else:
            raise Http404
