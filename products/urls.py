
from django.urls import path

from products.views import ProductsListView, basket_add, basket_remove, Search, post, ContactsView, ServicesView, \
   AgreementView
from users.views import UserProfileView

app_name = 'products'

urlpatterns = [
   path('', ProductsListView.as_view(), name='index'),
   path('ProductCategory/<int:category_id>/', ProductsListView.as_view(), name='category'),
   path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
   path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
   path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
   path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
   path('Search/', Search.as_view(), name='search'),
   path('baskets/change_qty/<str:prod>/<int:bas>/', post, name='change_qty'),
   path('Contacts/', ContactsView.as_view(), name='contacts'),
   path('Services/', ServicesView.as_view(), name='services'),
   path('subcategory/<int:category_id>/', ProductsListView.as_view(), name='subcategory'),
   path('Agreement/', AgreementView.as_view(), name='agreement'),
]


