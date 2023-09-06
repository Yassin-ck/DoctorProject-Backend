from django.urls import path
from . import views



urlpatterns = [
    path('',views.UserRegistration.as_view(),name='register'),
    path('login/',views.UserLogin.as_view(),name='login'),
    path('profile/',views.UserProfile.as_view(),name='profile'),
    path('userprofile/',views.UserProfileView.as_view(),name='userprofile'),
    path('userprofile/<int:pk>/',views.UserProfileView.as_view(),name='userprofileedit'),
    path('home/',views.UserDoctorView.as_view(),name='home')
]