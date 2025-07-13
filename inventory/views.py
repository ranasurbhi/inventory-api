from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Category, Supplier, Product, StockMovement
from .serializers import (
    CategorySerializer,
    StockAuditLogSerializer,
    SupplierSerializer,
    ProductSerializer,
    StockMovementSerializer
)
from django.db.models import Count, Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import StockAuditLog

# -------------------------------
# Registration view
# -------------------------------

@api_view(['POST'])
@permission_classes([AllowAny])  # Public route
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "User registered successfully!"}, status=201)


# -------------------------------
# CATEGORY VIEWS
# -------------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------------------
# SUPPLIER VIEWS
# -------------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def supplier_list(request):
    if request.method == 'GET':
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def supplier_detail(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk)
    except Supplier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------------------
# PRODUCT VIEWS
# -------------------------------


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list(request):
    if request.method == 'GET':
        category = request.GET.get('category')
        supplier = request.GET.get('supplier')
        search = request.GET.get('search')
        ordering = request.GET.get('ordering')

        products = Product.objects.all()

        # Filtering
        if category:
            products = products.filter(category_id=category)
        if supplier:
            products = products.filter(supplier_id=supplier)

        # Search by name
        if search:
            products = products.filter(name__icontains=search)

        # Sorting
        if ordering:
            products = products.order_by(ordering)

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set default page size
        result_page = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------------------
# STOCK MOVEMENT VIEWS
# -------------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def stock_movement_list(request):
    if request.method == 'GET':
        movements = StockMovement.objects.all()
        serializer = StockMovementSerializer(movements, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StockMovementSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()  # save() will update product quantity
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def stock_movement_detail(request, pk):
    try:
        movement = StockMovement.objects.get(pk=pk)
    except StockMovement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StockMovementSerializer(movement)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        movement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def low_stock_products(request):
    threshold = 5
    products = Product.objects.filter(quantity__lt=threshold)
    data = [
        {
            "id": p.id,
            "name": p.name,
            "quantity": p.quantity,
            "status": "LOW STOCK"
        }
        for p in products
    ]
    return Response(data)

@api_view(['GET'])
def inventory_stats(request):
    stats = Product.objects.values('category__name').annotate(
        total_products=Count('id'),
        total_quantity=Sum('quantity')
    )

    result = {
        entry['category__name']: {
            "total_products": entry['total_products'],
            "total_quantity": entry['total_quantity']
        }
        for entry in stats
    }

    return Response(result)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def stock_movement_list(request):
    if request.method == 'GET':
        movements = StockMovement.objects.all()
        serializer = StockMovementSerializer(movements, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StockMovementSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                movement = serializer.save()

                # Create audit log
                StockAuditLog.objects.create(
                    product=movement.product,
                    quantity=movement.quantity,
                    movement_type=movement.movement_type,
                    user=request.user
                )

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_audit_logs(request):
    logs = StockAuditLog.objects.all().order_by('-timestamp')
    serializer = StockAuditLogSerializer(logs, many=True)
    return Response(serializer.data)
