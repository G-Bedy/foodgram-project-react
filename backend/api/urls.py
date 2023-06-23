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
# router.register('recipesingredient', RecipeIngredientViewSet, basename='recipesingredient') # тестовый адрес потом удали



# router.register('categories', CategoryViewSet, basename='category')
# router.register('genres', GenreViewSet, basename='genre')
# router.register('titles', TitleViewSet, basename='titles')
# router.register(r'titles/(?P<title_id>\d+)/reviews',
#                 ReviewsViewSet, basename='reviews')
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentsViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('', include('djoser.urls.jwt')),
]