from django.urls import path
from .views import BookListCreateView, BookDetailView, UserListCreateView, UserDetailView, BorrowingHistoryView
from .views import CheckOutBookView, ReturnBookView, BookFilterListView

urlpatterns = [
    # Book endpoints
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/available/', BookFilterListView.as_view(), name='book-filter-list'),

    # User endpoints
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Checkout and Return endpoints
    path('checkout/', CheckOutBookView.as_view(), name='checkout-book'),
    path('return/<int:book_id>/', ReturnBookView.as_view(), name='return-book'),

    # Borrow History endpoints
    path('borrowing-history/', BorrowingHistoryView.as_view(), name='borrowing-history'),

    
]




