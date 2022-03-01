from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView, CreateView

from .models import Profile
from .forms import ProfileForm

# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')


USER = get_user_model()

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


@login_required
def profile_edit(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_form.html', {
        'form': form
    })


class SignupView(CreateView):
    model = USER
    form_class = UserCreationForm
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        auth_login(self.request, user)
        return response


signup = SignupView.as_view()

