from django.urls import re_path
from myapp.views import (add_product, 
                         list_products,
                         filter_products,
                         list_categories)

urlpatterns = [
    re_path(r'^add_product/', add_product, name='add_product'),
    re_path(r'^list_products/', list_products, name='list_products'),
    re_path(r'^search_products/', filter_products, name='filter_products'),
    re_path(r'^list_categories/', list_categories, name='list_categories'),
]