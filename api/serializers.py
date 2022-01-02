from rest_framework import serializers
from userauth.models import UsersAccount
from products.models import Product, Category, SubCategory


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, label='Password',
                                     style={'input_type': 'password', 'placeholder': 'Type Password'}, write_only=True)

    class Meta:
        model = UsersAccount
        fields = ['email', 'full_name', 'mobile', 'location', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('mobile')
        if not phone.isnumeric() or len(phone) < 10 or len(phone) > 12:
            raise serializers.ValidationError({'Phone': 'Enter valid phone numbers'})
        if UsersAccount.objects.filter(email=email).exists():
            raise serializers.ValidationError({'Email': 'Email already Exist'})
        return super().validate(attrs)

    def create(self, validated_data):
        return UsersAccount.objects.create_user(**validated_data)


class CreateProductSerializer(serializers.ModelSerializer):
    # desired_price = MoneyField(max_digits=10, decimal_places=2, default_currency='FRw')
    class Meta:
        model = Product
        fields = [
            'category', 'product_name', 'product_image', 'description',
            'quantity', 'desired_price', 'collected_date',
            'district', 'sector', 'cell', 'village',
            'road_number', 'house_number', 'location_description'
        ]


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60, min_length=4, write_only=True)

    class Meta:
        model = UsersAccount
        fields = ['email', 'password']


# --------- serializer for listing household products -----------------
class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'product_name', 'product_image', 'description',
            'quantity', 'desired_price', 'collected_date', 'user', 'district',
            'sector', 'cell', 'village', 'road_number', 'house_number', 'location_description'
        ]


# --------- view for listing household paid products -----------------
class ListHouseHoldPayedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'product_name', 'product_image', 'description',
            'quantity', 'desired_price', 'buying_price', 'collected_date', 'user', 'district',
            'sector', 'cell', 'village', 'road_number', 'house_number'
        ]


class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class AddSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'minimum_price', 'maximum_price']


"""serializer for listing eelctronic products"""
class ListAvailableToSoldProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'product_name', 'product_image'
        ]