from rest_framework import serializers

from cart.models import Order, CartItem, Cart
from cart.send_mail import order_mail


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.email')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data['customer']
        cart = user.carts.first()
        validated_data['total_cost'] = cart.total_cost
        validated_data['info'] = ''
        for i in cart.cart_items.all():
            validated_data['info'] += f'Продукт:{i.product}, количество:{i.quantity}, сумма:{i.total_cost}'
        cart.cart_items.all().delete()
        order_mail(email=user.email, body=validated_data['info'])
        return super().create(validated_data)




    # def create(self, validated_data):
    #     quntity_order = validated_data['quantity']
    #     product = validated_data['product']
    #     product_quantity = product.amount
    #
    #     if quntity_order > product_quantity:
    #         raise serializers.ValidationError(f'Нет такого количества, есть только {product_quantity}')
    #     product.amount -= quntity_order
    #     product.save()
    #     return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        # fields = '__all__'
        exclude = ['cart']

    def create(self, validated_data):
        user = self.context.get('request').user
        cart, _ = Cart.objects.get_or_create(user=user)

        cart_item = CartItem.objects.create(cart=cart, product=validated_data['product'], quantity=validated_data['quantity'])

        quntity_order = validated_data['quantity']
        product = validated_data['product']
        product_quantity = product.amount

        if quntity_order > product_quantity:
            raise serializers.ValidationError(f'Нет такого количества, есть только {product_quantity}')
        product.amount -= quntity_order
        product.save()

        return cart_item
