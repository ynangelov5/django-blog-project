from django.shortcuts import render
from blog.models import Post


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    # user = request.user.profile.image
    return render(request, 'blog/home.html', {'posts': posts})


def about(request):
    return render(request, 'blog/about.html')