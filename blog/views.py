from django.contrib import messages
from django.core.mail import send_mail

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, FormView

from .forms import EmailPostForm, ContactUsForm
from .models import Post


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
        post = get_object_or_404(Post, id=kwargs["post_id"], status="published")
        form = self.get_form()
        if form.is_valid():

            sender_name = form.cleaned_data["sender_name"]
            sender_email = form.cleaned_data["sender_email"]
            addressee_email = form.cleaned_data["addressee_email"]
            message = "Nadawca:{0}, udostępnił Ci post:\n{1}".format(
                sender_name, post.title
            )
            send_mail("Nowa wiadomość", message, sender_email, ["example@mail.com"])

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
