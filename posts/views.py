from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from django.urls import reverse


from .forms import PostForm
from .models import Post, Comment


# Create your views here.

class PostList(ListView):
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.all()


class PostDetail(DetailView):
    template_name = 'posts/details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post,
            id=self.kwargs.get("pk"))


class PostCreate(CreateView):
    template_name = 'posts/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        print(form.cleaned_data)
        return super(PostCreate, self).form_valid(form)
