from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, FormView

from .models import Post
from .forms import EmailPostForm


class PostList(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})


class SharePost(FormView):
    form_class = EmailPostForm
    template_name = "blog/post/share_post.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                messages.success(
                    request,
                    "Na wskazany adres e-mail została wysłana wiadomość z linkiem do posta.",
                )

            except Exception:
                messages.error(request, "Nie udało się udostępnić posta.")
            return render(request, "blog/post/list.html")
        else:
            return self.form_invalid(form)
