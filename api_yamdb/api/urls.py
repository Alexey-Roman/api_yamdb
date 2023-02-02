from django.urls import path


from .views import CreateUserViewSet, GetTokenViewSet


urlpatterns = [
    path(
        'v1/auth/signup/',
        CreateUserViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        GetTokenViewSet.as_view({'post': 'create'}),
        name='token'
    )
]
