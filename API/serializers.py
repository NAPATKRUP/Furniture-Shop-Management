from django.contrib.auth.models import User
from django.core.validators import validate_email
from rest_framework import serializers

from Account.models import Account, Employee, Owner
from Manage.models import Customer, Item, Stock, Supplier, Order, Order_Item


class supplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'address',
                  'phone', 'email', 'account_id']
        read_only_fields = ['id']
        extra_kwargs = {
            # 'email': {'validators': []},
            'name': {"error_messages": {"blank": "* กรุณากรอกชื่อบริษัท"}},
            'address': {"error_messages": {"blank": "* กรุณากรอกที่อยู่"}},
            'phone': {"error_messages": {"blank": "* กรุณากรอกเบอร์มือถือ"}},
            'email': {"error_messages": {"blank": "* กรุณากรอกอีเมล", 'invalid': "* กรุณากรอกอีเมลให้ถูกต้อง"}},
        }

    def validate_phone(self, value):
        if len(value) != 10:
            raise serializers.ValidationError(
                "* กรุณากรอกเบอร์มือถือให้ถูกต้อง")
        return value


class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description',
                  'item_type', 'purchase_price', 'sale_price', 'supplier_id']
        read_only_fields = ['id']
        depth = 1
        extra_kwargs = {
            'name': {"error_messages": {"blank": "* กรุณากรอกชื่อสินค้า"}},
            'description': {"error_messages": {"blank": "* กรุณากรอกรายละเอียดสินค้า"}},
            'item_type': {"error_messages": {"blank": "* กรุณากรอกประเภทสินค้า"}},
            'purchase_price': {"error_messages": {"blank": "* กรุณากรอกราคาซื้อ", 'invalid': "* กรุณากรอกราคาซื้อให้ถูกต้อง"}},
            'sale_price': {"error_messages": {"blank": "* กรุณากรอกราคาขาย", 'invalid': "* กรุณากรอกราคาขายให้ถูกต้อง"}},
        }

    def validate_purchase_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "* กรุณากรอกราคาซื้อให้ถูกต้อง")
        return value

    def validate_sale_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "* กรุณากรอกราคาขายให้ถูกต้อง")
        return value


class stockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'item_id', 'color', 'amount']
        read_only_fields = ['id']
        depth = 1
        extra_kwargs = {
            'color': {"error_messages": {"blank": "* กรุณากรอกสี"}},
            'amount': {"error_messages": {"blank": "* กรุณากรอกจำนวนสินค้า", 'invalid': "* กรุณากรอกจำนวนให้ถูกต้อง"}},
        }

    def validate_amount(self, value):
        if int(value) < 0:
            raise serializers.ValidationError(
                "* กรุณากรอกจำนวนสินค้าให้ถูกต้อง")
        return value


class customerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'fname', 'lname',
                  'email', 'phone', 'address', 'account_id']
        read_only_fields = ['id']
        extra_kwargs = {
            'fname': {"error_messages": {"blank": "* กรุณากรอกชื่อจริง"}},
            'lname': {"error_messages": {"blank": "* กรุณากรอกนามสกุล"}},
            'email': {"error_messages": {"blank": "* กรุณากรอกอีเมล", 'invalid': "* กรุณากรอกอีเมลให้ถูกต้อง"}},
            'phone': {"error_messages": {"blank": "* กรุณากรอกเบอร์มือถือ"}},
            'address': {"error_messages": {"blank": "* กรุณากรอกที่อยู่"}},
        }

    def validate_phone(self, value):
        if len(value) != 10:
            raise serializers.ValidationError(
                "* กรุณากรอกเบอร์มือถือให้ถูกต้อง")
        return value


class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'department', 'owner_id', 'account']
        read_only_fields = ['id', 'owner_id', 'account']
        depth = 2


class accountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'phone', 'user']
        read_only_fields = ['id', 'user']
        extra_kwargs = {
            'phone': {"error_messages": {"blank": "* กรุณากรอกเบอร์มือถือ"}},
        }

    def validate_phone(self, value):
        if len(value) != 10:
            raise serializers.ValidationError(
                "* กรุณากรอกเบอร์มือถือให้ถูกต้อง")
        return value


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'username']

    def validate_first_name(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError(
                "* กรุณากรอกชื่อจริง")
        return value

    def validate_last_name(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError(
                "* กรุณากรอกนามสกุล")
        return value


class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'create_date', 'account_id', 'cus_id']
        read_only_fields = ['id']
        depth = 3


class orderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Item
        fields = ['id', 'name', 'description', 'item_type',
                  'amount', 'color', 'price', 'order_id']
        read_only_fields = ['id']
        depth = 1


class ownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'shop_name', 'account']
        read_only_fields = ['id']
