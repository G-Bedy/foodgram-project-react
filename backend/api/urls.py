from django.urls import include, path
from rest_framework import routers
from djoser import views as djoser_views

from .views import (UserViewSet, TagViewSet, IngredientViewSet, RecipeViewSet,
                    SubscriberViewSet,)

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes'),
router.register('subscribers', SubscriberViewSet, basename='subscribers')



urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]