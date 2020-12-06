from django.urls import path

from home import views

urlpatterns = [
    path("banners/", views.BannerAPIView.as_view()),
    path('navHead/', views.NavAPIView.as_view()),
    path('navFoot/', views.NavAPIViews.as_view()),
]