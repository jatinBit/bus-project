from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . views import *

urlpatterns = [
    path('register/',UserRegistrationView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('logout/',UserLogoutView.as_view()),
    path('changepassword/',UserChangePasswordView.as_view()),
    path('send-reset-password-email/',SendPasswordResetEmailView.as_view()),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('', UserView.as_view()),
    # path('register/<id>',UserGeneric.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
