
from rest_framework.routers import DefaultRouter

from cart.views import OrderView, CartItemView

router = DefaultRouter()
router.register('cart', CartItemView)
router.register('', OrderView)

urlpatterns = []

urlpatterns.extend(router.urls)
