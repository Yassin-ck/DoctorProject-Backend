from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('',views.UserRegistration.as_view(),name='register'),
    path('login/',views.MyTokenObtainPairView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('profile/',views.UserProfile.as_view(),name='profile'),
    path('userprofile/',views.UserProfileView.as_view(),name='userprofile'),
    path('userprofile/<int:pk>/',views.UserProfileView.as_view(),name='userprofileedit'),
    path('home/',views.UserDoctorView.as_view(),name='home')
]