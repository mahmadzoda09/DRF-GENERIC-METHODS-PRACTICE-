
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import PageNumberPagination

from .models import Book
from .serializers import BookSerializer


class BookPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50


class BookListView(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        return Book.objects.all()

    def get_serializer_class(self):
        return BookSerializer

    def get(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    


class BookDetailView(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        book = self.get_object()
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        book = self.get_object()
        serializer = self.get_serializer(book,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        book = self.get_object()
        book.delete()
        return Response(status=204)
