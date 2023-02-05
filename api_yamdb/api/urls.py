from django.urls import include, path
from rest_framework import routers


from .views import CreateUserViewSet, GetTokenViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet)

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
