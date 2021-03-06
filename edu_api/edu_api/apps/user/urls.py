from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    path("login/", obtain_jwt_token),
    path("captcha/", views.CaptchaAPIView.as_view()),
    path("users/", views.UserAPIView.as_view()),
    path("phone/", views.PhoneAPIView.as_view({'post': 'phone'})),
    path("message/", views.SendMessageAPIView.as_view()),
    # path("get_username/",views.GetUserAPIView.as_view()),
]
