from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view
from .forms import LoginForm

urlpatterns = [
     path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
   ]