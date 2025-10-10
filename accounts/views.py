from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DetailView
from accounts.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from accounts.models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, 
                f'Account created successfully. Welcome to the Blog App, {username}'
            )

            login(request, user)

            return redirect('blog-home')
         
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def my_profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile
            )
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('my-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)


    context = {
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/my-profile.html', context)
    

class UserProfileView(DetailView):
    model = User
    template_name = 'accounts/user-profile.html'
    context_object_name = 'user_obj'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        context['posts'] = self.object.posts.all().order_by('-created_at')[:5]
        return context

