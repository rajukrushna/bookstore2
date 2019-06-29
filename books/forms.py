from django import forms
from api.models import Book


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))


class BookForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    author = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    published_year = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    no_of_pages = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    isbn = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    cover = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control'
        }
    ))
    pdf = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control'
        }
    ))


class EditBookForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    author = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    published_year = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    no_of_pages = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    isbn = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    cover = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control'
        }
    ))
    pdf = forms.FileField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control'
        }
    ))
