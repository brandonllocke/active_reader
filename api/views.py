from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from .models import Book


class BookViews(APIView):
    def post(self, request, id=None):
        return self._edit_book(request, id) if id else self._add_book(request)

    def get(self, request, id=None):
        return self._get_book(id) if id else self._get_books()

    @staticmethod
    def _success_response(serializer):
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @staticmethod
    def _failure_response(serializer):
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def _edit_book(self, request, id):
        item = Book.objects.get(id=id)
        serializer = BookSerializer(item, request.data, partial=True)
        return self._validate_and_respond(serializer)

    def _add_book(self, request):
        serializer = BookSerializer(data=request.data)
        return self._validate_and_respond(serializer)

    def _validate_and_respond(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return self._success_response(serializer)
        else:
            return self._failure_response(serializer)

    def _get_book(self, id):
        item = Book.objects.get(id=id)
        serializer = BookSerializer(item)
        return self._success_response(serializer)

    def _get_books(self):
        items = Book.objects.all()
        serializer = BookSerializer(items, many=True)
        return self._success_response(serializer)

