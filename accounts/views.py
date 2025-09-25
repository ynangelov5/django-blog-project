from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, 
                f'Account created successfully. Welcome to the Blog App, {username}'
            )
            return redirect('blog-home')
         
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})
    
    

