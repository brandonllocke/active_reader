from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=300,
        validators=[
            UniqueValidator(
                queryset=Book.objects.all(),
                message='A book by this title already exists.'
            )
        ]
    )
    active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = Book
        fields = ('__all__')
