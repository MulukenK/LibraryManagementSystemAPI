from rest_framework import serializers
from .models import Book, CustomUser, Transaction
from rest_framework.exceptions import ValidationError



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'date_of_membership', 'is_active']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


        

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, data):
        # Check if the book has available copies for check-out
        if self.context['request'].method == 'POST':  # Only for creating a transaction
            book = data['book']
            if book.copies_available <= 0:
                raise ValidationError(f"The book '{book.title}' is currently unavailable.")
        return data