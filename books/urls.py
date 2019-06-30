from django.urls import path
from . import views

urlpatterns = [
    path('', views.booklist_view, name='books'),
    path('books/detail/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/new/', views.book_new, name='book_new'),
    path('books/edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('books/delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('books/search/', views.book_search, name='book_search'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]