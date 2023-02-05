from django.urls import include, path
from rest_framework import routers


from .views import (CreateUserViewSet, GetTokenViewSet, UserViewSet,
                    CategoryViewSet, GenreViewSet, TitleViewSet,)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/signup/',
        CreateUserViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        GetTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
]
