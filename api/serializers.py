from rest_framework import serializers
from userauth.models import UsersAccount
from products.models import Product

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, label='Password',
                                     style={'input_type': 'password', 'placeholder': 'Type Password'})

    class Meta:
        model = UsersAccount
        fields = ['email', 'full_name', 'mobile', 'password']

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


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60, min_length=4, write_only=True)

    class Meta:
        model = UsersAccount
        fields = ['email', 'password']


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'product', 'product_image', 'description',
            'quantity', 'cost', 'other', 'collected_date',
            ]

