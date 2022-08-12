from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import ProductView, CategoryView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('', ProductView)


urlpatterns = [
    path('', include(router.urls)),
]
