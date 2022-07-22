from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=300)
    active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = Book
        fields = ('__all__')
