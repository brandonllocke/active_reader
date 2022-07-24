from rest_framework import serializers


class Immutable:
    message = "This field cannot be changed once set."
    requires_context = True

    def __init__(self, message=None):
        self._message = message or self.message

    def __call__(self, value, serializer_field):
        instance = getattr(serializer_field.parent, 'instance', None)
        if instance and value != instance.title:
            raise serializers.ValidationError(self._message)
