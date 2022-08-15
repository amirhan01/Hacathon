from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from product.models import Category, Product, Comment, Rating, Like, Favorite, Contact
from product.serializers import CategorySerializer, ProductSerializer, CommentSerializer, RatingSerializer, \
    ContactSerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category']
    ordering_fields = ['name']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk):
        serializers = RatingSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(product_id=pk, owner=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status=201)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk):
        try:
            like_object, _ = Like.objects.get_or_create(owner=request.user, product_id=pk)
            like_object.like = not like_object.like
            like_object.save()

            if like_object.like:
                return Response('Вы поставили лайк :)')
            return Response('Вы убрали лайк :(')
        except:
            return Response('К сожалению, такого продукта нет')

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk):
        try:
            fav_object, _ = Favorite.objects.get_or_create(owner=request.user, product_id=pk)
            fav_object.favorite = not fav_object.favorite
            fav_object.save()

            if fav_object.favorite:
                return Response('Вы добавили в избранное :)')
            return Response('Вы удалили из избранного :(')
        except:
            return Response('К сожалению, такого продукта нет')


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContactView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]