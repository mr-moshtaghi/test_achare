from rest_framework_simplejwt.views import TokenRefreshView

from .views import AccountViewSet, GetTokenInSignUpView
from django.urls import path, include

app_name = 'auth'
urlpatterns = [
    path('account/', include([
        path('', AccountViewSet.as_view(
            {'post': 'account'}
        )),
        path('<uuid:pk>/', include([
            path('verify-cellphone/', AccountViewSet.as_view(
                {'post': 'verify_cellphone'}
            )),
            path('register/', AccountViewSet.as_view({
                'post': 'register'
            }))
        ]))
    ])),
    path('token/', GetTokenInSignUpView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
