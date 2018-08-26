from django.urls import path
from . import views
from django.contrib.auth import views as auth_view #LogoutView
urlpatterns = [
    path('',views.signup, name='signup'),
    path('logout/', auth_view.LogoutView.as_view(), name="logout"),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
]