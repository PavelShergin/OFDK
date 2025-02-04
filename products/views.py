from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class ContactsView(TitleMixin, TemplateView):
    template_name = 'products/contacts.html'
    title = 'Контакты'


class AgreementView(TitleMixin, TemplateView):
    template_name = 'products/agreement.html'
    title = 'Соглашение'


class ServicesView(TitleMixin, TemplateView):
    template_name = 'products/services.html'
    title = 'Услуги'


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'От Фундамента до Кровли'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 24
    title = 'Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(ProductCategory, id=category_id)
            return queryset.filter(category__in=category.get_descendants(include_self=True)).order_by('price')
        return queryset.order_by('price')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['category'] = self.get_category()
        return context

    def get_category(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return get_object_or_404(ProductCategory, id=category_id)
        return None


class Search(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 15
    context_object_name = 'search'
    title = 'Каталог'

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['q'] = self.request.GET.get('q')
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def post(request, *args, **kwargs):
    product_name = kwargs.get('prod')
    product = Product.objects.get(name=product_name)
    baskets = Basket.objects.filter(user=request.user, product=product)
    basket = baskets.first()
    qty = int(request.POST.get('qty'))
    if basket.quantity != qty:
        basket.quantity = qty
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
