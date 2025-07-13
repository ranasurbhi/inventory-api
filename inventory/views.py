from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Category, Supplier, Product, StockMovement
from .serializers import (
    CategorySerializer,
    SupplierSerializer,
    ProductSerializer,
    StockMovementSerializer
)
from django.db.models import Count, Sum

# -------------------------------
# CATEGORY VIEWS
# -------------------------------
@api_view(['GET', 'POST'])
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
def product_list(request):
    if request.method == 'GET':
        category = request.GET.get('category')
        supplier = request.GET.get('supplier')
        products = Product.objects.all()
        if category:
            products = products.filter(category_id=category)
        if supplier:
            products = products.filter(supplier_id=supplier)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
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
