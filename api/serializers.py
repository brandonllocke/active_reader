from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .validators.immutable import Immutable
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=300,
        validators=[
            UniqueValidator(
                queryset=Book.objects.all(),
                message='A book by this title already exists.'
            ),
            Immutable(
                message='Cannot update book title after creation.'
            )
        ]
    )
    active = serializers.BooleanField(required=False, default=True)

    #def validate_title(self, value):
    #    if self.instance and value != self.instance.title:
    #        raise serializers.ValidationError("Cannot change book title once set.")
    #    return value

    class Meta:
        model = Book
        fields = ('__all__')
