from django.urls import path
from .views import SignUpView, LoginView, UserProfileView
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', views.dashboard, name='dashboard'),
]