from django.urls import path
from . import views



urlpatterns = [
    path('',views.UserRegistration.as_view(),name='register'),
    path('login/',views.UserLogin.as_view(),name='login'),
    path('profile/',views.UserProfile.as_view(),name='profile')
]