from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, PostComment
from .forms import PostForm, EmailPostForm, CommentForm, ContactForm, Category


def home(request):
    """
    Home page view.
    """
    return render(request, 'home.html', {})

    
def about(request):
    """
    About page.
    """
    return render(request, 'about.html', {})
    

def post_share(request, post_slug):
    """
    Share blog post.
    """
    post = get_object_or_404(Post, slug=post_slug, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} would recommend reading f{post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'contact@mysite.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share.html',
                  {'post': post, 'form': form, 'sent': sent})


class PostView(ListView):
    """
    Blog posts view.
    """
    model = Post
    template_name = 'blog.html'
    ordering = ['-published']
    paginate_by = 5


class ArticleView(DetailView):
    """
    Single post view.
    """
    model = Post
    template_name = 'article.html'


class AddPostView(CreateView):
    """
    Create blog post view.
    """
    model = Post
    form_class = PostForm
    template_name = 'post-new.html'

class AddCategory(CreateView):
    """
    Create blog post view.
    """
    model = Category
    template_name = 'article-category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    """
    Update blog post view.
    """
    model = Post
    template_name = 'edit-post.html'
    fields = ['title', 'body', 'status']
    

class DeletePostView(DeleteView):
    """
    Delete blog post.
    """
    model = Post
    template_name = 'delete-post.html'
    success_url = reverse_lazy('website:blog')


def contact_view(request):
    """
    Contact form view.
    """
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('website:success')
    return render(request, "contact.html", {'form': form})


def success_view(request):
    """
    Success message.
    """
    return render(request, "success.html")

