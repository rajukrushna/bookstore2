from django.shortcuts import render
from .forms import LoginForm, SignUpForm, BookForm, EditBookForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
import requests
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic.edit import UpdateView


API_URL = 'http://127.0.0.1:8000'


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password1": form.cleaned_data["password1"],
                "password2": form.cleaned_data["password2"],
            }
            resp = requests.post(f'{API_URL}/auth/signup/', data=data)
            if resp.status_code == 400:
                resp_data = resp.json()
                for error in resp_data:
                    if error == 'non_field_errors':
                        form.add_error(None, resp_data[error])
                    else:
                        form.add_error(error, resp_data[error])
                return render(request, 'signup.html', {"form": form})
            return render(request, 'signup_success.html')
        else:
            return render(request, 'signup.html')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password"]
            }
            url = f'{API_URL}/auth/login/'
            resp = requests.post(url, data)
            response_data = resp.json()
            if resp.status_code == 400:
                if 'non_field_errors' in response_data:
                    form.add_error(None, response_data['non_field_errors'])
                return render(request, 'login.html', {"form": form})
            request.session['key'] = response_data['key']
            request.session["username"] = data["username"]
            headers = {"Authorization": f'Token {request.session["key"]}'}
            user = requests.get(f'{API_URL}/auth/user/', headers=headers, data={"username": data['username']})
            user_data = user.json()
            user = requests.get(f'{API_URL}/api/user/{user_data["pk"]}', headers=headers)
            user_data = user.json()
            request.user = User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_staff=user_data['is_staff']
            )
            request.auth = Token(request.session['key'])

            return HttpResponseRedirect(reverse('books'))
        else:
            return render(request, 'login.html', {"form": form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {"form": form})


def booklist_view(request):
    authenticate_request(request)
    if request.method == 'GET':
        url = f'http://{request.get_host()}/api/books'
        r = requests.get(url)
        data = r.json()
        count = int(data['count'])
        next = data['next']
        prev = data['previous']
        books = data['results']
        return render(request, 'books.html', {
            'count': count,
            'next': next,
            'prev': prev,
            'books': books
        })
    return HttpResponse("Bad Request")


def book_new(request):
    authenticate_request(request)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            headers = {"Authorization": f'Token {request.session["key"]}'}
            resp = requests.post(f'{API_URL}/api/books/', headers=headers, data=request.POST, files=request.FILES)
            return HttpResponseRedirect(reverse('books'))
    else:
        form = BookForm()
        return render(request, 'book_new.html', {"form": form})


def book_detail(request, pk):
    authenticate_request(request)
    if request.method == 'GET':
        resp = requests.get(f'{API_URL}/api/books/{pk}')
        book = resp.json()
        return render(request, 'book_detail.html', {"book": book})


def book_edit(request, pk):
    """
    if request is GET, get the data and pre populate the Book form with the obtained data
    if request is POST, update the data in database
    """
    authenticate_request(request)
    if request.method == 'POST':
        form = EditBookForm(request.POST, request.FILES)
        headers = {"Authorization": f'Token {request.session["key"]}'}
        if form.is_valid():
            text_data = {
                "id": form.cleaned_data['id'],
                "title": form.cleaned_data['title'],
                "author": form.cleaned_data['author'],
                "no_of_pages": form.cleaned_data['no_of_pages'],
                "published_year": form.cleaned_data['published_year'],
                "isbn": form.cleaned_data['isbn']
            }
            url = f'{API_URL}/api/bookfieldsupdate/{form.cleaned_data["id"]}/'
            resp = requests.put(url, headers=headers, data=text_data)
            if 'cover' in request.FILES:
                cover_data = {
                    "id": form.cleaned_data['id'],
                }
                cover_file = {
                    "cover": request.FILES['cover']
                }
                url = f'{API_URL}/api/bookcoverupdate/{form.cleaned_data["id"]}/'
                resp = requests.put(url, headers=headers, data=cover_data, files=cover_file)
            if 'pdf' in request.FILES:
                pdf_data = {
                    "id": form.cleaned_data['id'],
                }
                pdf_file = {
                    "pdf": request.FILES['pdf']
                }
                url = f'{API_URL}/api/bookpdfupdate/{form.cleaned_data["id"]}/'
                resp = requests.put(url, headers=headers, data=pdf_data, files=pdf_file)
            return HttpResponseRedirect(reverse('books'))
    else:
        url = f'{API_URL}/api/books/{pk}'
        resp = requests.get(url)
        book = resp.json()
        data = {
            "id": book['id'],
            'title': book['title'],
            "author": book['author'],
            "published_year": book['published_year'],
            "no_of_pages": book['no_of_pages'],
            "isbn": book['isbn']
        }

        form = EditBookForm(data=data)
        return render(request, 'book_edit.html', {
            "form": form
        })


def book_delete(request, pk):
    authenticate_request(request)
    if request.method == 'GET':
        url = f'{API_URL}/api/books/{pk}'
        headers = {"Authorization": f'Token {request.session["key"]}'}
        resp = requests.delete(url, headers=headers)
        return HttpResponseRedirect(reverse('books'))


def logout_view(request):
    try:
        del request.session['key']
        del request.session['username']
        request.user = None
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('books'))


def authenticate_request(request):
    if 'key' not in request.session:
        return
    try:
        headers = {"Authorization": f'Token {request.session["key"]}'}
        user = requests.get(f'{API_URL}/auth/user/', headers=headers, data={"username": request.session['username']})
        user_data = user.json()
        user = requests.get(f'{API_URL}/api/user/{user_data["pk"]}', headers=headers)
        user_data = user.json()
        request.user = User(
            id=user_data['id'],
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_staff=user_data['is_staff']
        )
        request.auth = Token(request.session['key'])
    except:
        pass



