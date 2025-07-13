from rest_framework import serializers
from .models import Category, Supplier, Product, StockMovement
from .models import StockAuditLog

class StockAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAuditLog
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = '__all__'
    def create(self, validated_data):
        movement = StockMovement.objects.create(**validated_data)

        # Auto-update product quantity
        product = movement.product
        if movement.movement_type == 'IN':
            product.quantity += movement.quantity
        elif movement.movement_type == 'OUT':
            product.quantity -= movement.quantity
        product.save()

        #  Create audit log
        from .models import StockAuditLog
        StockAuditLog.objects.create(
            product=product,
            quantity=movement.quantity,
            movement_type=movement.movement_type,
            user=self.context['request'].user  # Very important
        )

        return movement