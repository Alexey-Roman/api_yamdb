from django.urls import include, path
from rest_framework import routers


from .views import (CreateUserViewSet, GetTokenViewSet, UserViewSet,
                    CategoryViewSet, GenreViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename='comments'
)

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
