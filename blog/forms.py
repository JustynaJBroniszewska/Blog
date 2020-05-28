from django import forms


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
