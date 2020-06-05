from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, FormView

from .forms import EmailPostForm, ContactUsForm, CommentForm
from .models import Post
from taggit.models import Tag


class PostList(ListView):
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"
    model = Post

    def get_queryset(self):
        if "tag_slug" in self.kwargs and self.kwargs["tag_slug"]:
            tag = get_object_or_404(Tag, slug=self.kwargs["tag_slug"])
            return self.model.published.all().filter(tags__in=[tag])
        return self.model.published.all()


class PostDetail(FormView):
    form_class = CommentForm
    template_name = "blog/post/detail.html"

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            slug=kwargs["post"],
            status="published",
            publish__year=kwargs["year"],
            publish__month=kwargs["month"],
            publish__day=kwargs["day"],
        )

        comments = post.comments.filter(active=True)
        comment_form = self.form_class()

        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=post.id
        )
        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-publish"
        )[:4]

        return render(
            request,
            self.template_name,
            {
                "post": post,
                "comments": comments,
                "comment_form": comment_form,
                "similar_posts": similar_posts,
            },
        )

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            slug=kwargs["post"],
            status="published",
            publish__year=kwargs["year"],
            publish__month=kwargs["month"],
            publish__day=kwargs["day"],
        )
        comments = post.comments.filter(active=True)
        form = self.get_form()
        if form.is_valid():
            comment_form = self.form_class(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
        else:
            form = self.form_invalid(form)
        return render(
            request,
            self.template_name,
            {"post": post, "comments": comments, "comment_form": comment_form},
        )


class SharePost(FormView):
    form_class = EmailPostForm
    template_name = "blog/post/share_post.html"

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs["post_id"], status="published")
        form = self.get_form()

        if form.is_valid():
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "{} ({}) zachęca do przeczytania '{}'".format(
                form.cleaned_data["sender_name"],
                form.cleaned_data["sender_email"],
                post.title,
            )
            message = "Przeczytaj post '{}' na stronie {} \n\nKomentarz dodany przez {}:\n\n{}".format(
                post.title,
                post_url,
                form.cleaned_data["sender_name"],
                form.cleaned_data["comment"],
            )
            addressee_email = form.cleaned_data["addressee_email"]
            send_mail(
                subject,
                message,
                "example@mail.com",
                [form.cleaned_data["addressee_email"]],
            )
            try:
                messages.success(
                    request,
                    "Na wskazany adres e-mail została wysłana wiadomość z linkiem do posta o tytule: "
                    + post.title,
                )
            except Exception:
                messages.error(request, "Nie udało się udostępnić posta.")
            return render(request, "blog/post/list.html")
        else:
            return self.form_invalid(form)
        return render(request, self.template_name, {"post": post, "form": form})


class ContactUs(FormView):
    template_name = "blog/components/contact.html"
    form_class = ContactUsForm
    success_url = reverse_lazy("blog:contact")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            sender_name = form.cleaned_data["sender_name"]
            sender_email = form.cleaned_data["sender_email"]
            message = "{0} przesyła wiadomość:\n\n{1}".format(
                sender_name, form.cleaned_data["comment"]
            )
            send_mail("Nowa wiadomość", message, sender_email, ["example@mail.com"])
            try:
                messages.success(request, "Dziękujemy za kontakt.")
            except Exception:
                messages.error(request, "Niestety, nie udało się wysłać wiadomości.")
            return redirect(reverse("blog:post_list"))
        else:
            form = self.get_form(form)
        return render(request, "blog/components/contact.html", {"form": form})
