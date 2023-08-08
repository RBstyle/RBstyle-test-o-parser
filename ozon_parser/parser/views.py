from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    UserSerializer,
    GroupSerializer,
    ProductSerializer,
    NumberOfProductsSerializer,
)
from .tasks import create_product
from .models import Product
from telegram_bot.views import run_bot

num_of_products = openapi.Parameter(
    "num_of_products",
    openapi.IN_QUERY,
    description="Number of products",
    type=openapi.TYPE_INTEGER,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@swagger_auto_schema(
    methods=["post"],
    request_body=NumberOfProductsSerializer,
    operation_description="Введите количество продуктов(от 0 до 50)",
)
@swagger_auto_schema(
    methods=["get"],
    operation_description="Возвращает список всех товаров",
)
@api_view(["GET", "POST"])
def parser(request):
    if request.method == "POST":
        num_of_products = request.data["num_of_products"]
        create_product(num_of_products=num_of_products)
        return Response(num_of_products)
    elif request.method == "GET":
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    methods=["get"],
    operation_description="Возвращает товар по ID",
)
@api_view(["GET"])
def get_product_by_id(request, id: int):
    if request.method == "GET":
        query = Product.objects.filter(id=id).first()
        serializer = ProductSerializer(query)
        return Response(serializer.data)
