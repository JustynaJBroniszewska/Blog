from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    sender_name = forms.CharField(label="Nadawca", max_length=25, required=True)
    sender_email = forms.EmailField(label="E-mail nadawcy", required=True)
    addressee_email = forms.EmailField(
        label="E-mail adresata", max_length=25, required=True
    )
    comment = forms.CharField(
        label="Wpisz komentarz",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )


class ContactUsForm(forms.Form):
    sender_name = forms.CharField(label="Nadawca", max_length=25, required=True)
    sender_email = forms.EmailField(label="E-mail nadawcy", required=True)
    comment = forms.CharField(
        label="Wpisz komentarz",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("commentator_name", "commentator_email", "comment_body")
        labels = {
            "commentator_name": "Autor:",
            "commentator_email": "E-mail:",
            "comment_body": "Komentarz:",
        }


class SearchForm(forms.Form):
    query = forms.CharField()
