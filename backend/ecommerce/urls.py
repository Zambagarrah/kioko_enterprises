from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
]


from django.urls import path, include

urlpatterns = [
    path('api/', include('ecommerce.urls')),
    ...
]
