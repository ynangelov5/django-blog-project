from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView
    )
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
    )
from blog.models import Post


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    # user = request.user.profile.image
    return render(request, 'blog/home.html', {'posts': posts})


def about(request):
    return render(request, 'blog/about.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post-create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
     

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post-update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author 
        # raises 403 if a user tries to edit someone else's post



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post-delete.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author 
        # raises 403 if a user tries to delete someone else's post

