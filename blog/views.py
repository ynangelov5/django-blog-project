from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView
    )
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
    )
from django.contrib.auth.models import User
from django.db.models import Q
from blog.models import Post


def about(request):
    return render(request, 'blog/about.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user-posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_at')


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


class PostSearchView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'results'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.all()
        search_fields = ['query', 'title', 'author'] 
        q_object = Q()

        for field in search_fields:
            value = self.request.GET.get(field, '').strip()
            if value:
                if field == 'query':
                    q_object |= Q(title__icontains=value) | Q(author__username__icontains=value)
                elif field == 'title':
                    q_object &= Q(title__icontains=value)
                elif field == 'author':
                    q_object &= Q(author__username__icontains=value)

        return queryset.filter(q_object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title_query = self.request.GET.get('title', '').strip()
        author_query = self.request.GET.get('author', '').strip()
        """
        If the search bar is used, it overrides the title and author filters.  
        If the search bar is empty but the title and author fields are filled, 
        their values are combined and shown as the search query.
        """
        context['query'] = self.request.GET.get('query', '').strip() or f"{title_query} {author_query}".strip()
        context['title_query'] = title_query
        context['author_query'] = author_query
        return context