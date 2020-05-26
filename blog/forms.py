from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class ContactUsForm(forms.Form):
    name = forms.CharField(label="Nadawca", max_length=25, required=True)
    email = forms.EmailField(label="E-mail nadawcy", required=True)
    to = forms.CharField(label="Adres e-mail adresata", max_length=25, required=True)
    comment = forms.CharField(
        label="Wpisz komentarz",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )
