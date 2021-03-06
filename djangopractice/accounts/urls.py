from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .forms import LoginForm


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(
        form_class=LoginForm,
        template_name='accounts/login_form.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
]
