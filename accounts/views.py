from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
~from django.contrib.auth.decorators import login_required
from accounts.forms import UserRegisterForm


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
def profile(request):
    return render(request, 'accounts/profile.html')
    

