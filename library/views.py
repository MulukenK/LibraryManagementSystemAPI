
from django.shortcuts import render
from .models import Book, CustomUser
from .serializers import BookSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Transaction
from .serializers import TransactionSerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone





class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer




class CheckOutBookView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            book = serializer.validated_data['book']
            if book.copies_available > 0:
                # Decrease the number of available copies
                book.copies_available -= 1
                book.save()

                # Save the transaction
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "No copies available."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        try:
            # Get the book
            book = Book.objects.get(id=book_id)

            # Find an active transaction for this book and user
            transaction = Transaction.objects.filter(
                user=request.user, book=book, return_date__isnull=True
            ).first()

            if not transaction:
                return Response(
                    {"detail": "You have not checked out this book."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Mark the transaction as returned
            transaction.return_date = timezone.now().date()
            transaction.save()

            # Increment the book's available copies
            book.copies_available += 1
            book.save()

            return Response({"detail": "Book returned successfully."}, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

class BookFilterListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['copies_available']
    search_fields = ['title', 'author', 'isbn']



class BorrowingHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).select_related('book')
        history = [
            {
                "book_title": transaction.book.title,
                "book_author": transaction.book.author,
                "checkout_date": transaction.checkout_date,
                "return_date": transaction.return_date,
            }
            for transaction in transactions
        ]
        return Response(history)