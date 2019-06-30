from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:pk>/', views.user_detail),
    path('bookfieldsupdate/<int:pk>/', views.book_field_update),
    path('bookcoverupdate/<int:pk>/', views.book_cover_update),
    path('bookpdfupdate/<int:pk>/', views.book_pdf_update),
    path('booksearch/', views.search_books)
]
