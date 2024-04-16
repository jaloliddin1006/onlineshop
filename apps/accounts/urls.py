from django.urls import path, include
from .views import (
    UserRegisterView,
    LoginView,
    LogoutView,
    UpdateUserView,
    CustomPasswordResetView,
    CustomCheckVerifyCodeView,
    CustomPasswordResetConfirmView,

)


app_name = 'accounts'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', UpdateUserView.as_view(), name='update'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('check-verify-code/<uuid:uuid>/', CustomCheckVerifyCodeView.as_view(), name='check-verify'),
    path('password-reset-confirm/<uuid:uuid>/', CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    # path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('password-reset-complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]