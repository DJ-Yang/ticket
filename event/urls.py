from django.urls import path

from event import views


urlpatterns = [
    path("", views.EventPageView.as_view()),
    path("download/", views.UserGetCouponAPI.as_view()),
    path("list/", views.EventBookListAPI.as_view()),
]
