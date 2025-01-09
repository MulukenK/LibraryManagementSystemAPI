from datetime import timezone
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


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

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
    def post(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
            if transaction.return_date is not None:
                return Response({"error": "This book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

            # Update return date and increase available copies
            transaction.return_date = timezone.now()
            transaction.book.copies_available += 1
            transaction.book.save()
            transaction.save()

            return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)
        

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

class BookFilterListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['copies_available']
    search_fields = ['title', 'author', 'isbn']