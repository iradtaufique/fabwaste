from rest_framework import serializers
from userauth.models import UsersAccount, Profile
from products.models import Product, Category, SubCategory


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, label='Password',
                                     style={'input_type': 'password', 'placeholder': 'Type Password'}, write_only=True)

    class Meta:
        model = UsersAccount
        fields = ['email', 'full_name', 'mobile', 'location', 'password']

    def to_representation(self, instance):
        rep = super(RegisterSerializer, self).to_representation(instance)
        rep['location'] = instance.location.name
        return rep

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


class ListUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersAccount
        fields = ['id', 'email', 'full_name', 'mobile', 'location']

    def to_representation(self, instance):
        rep = super(ListUsersSerializer, self).to_representation(instance)
        rep['location'] = instance.location.name
        return rep


class CreateProductSerializer(serializers.ModelSerializer):
    # district = serializers.CharField(source='district.name')
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

    def to_representation(self, instance):
        rep = super(ListProductSerializer, self).to_representation(instance)
        rep['category'] = instance.category.name
        rep['district'] = instance.district.name
        rep['user'] = instance.user.full_name
        return rep

# --------- view for listing household paid products -----------------
class ListHouseHoldPayedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'product_name', 'product_image', 'description',
            'quantity', 'desired_price', 'buying_price', 'collected_date', 'user', 'district',
            'sector', 'cell', 'village', 'road_number', 'house_number'
        ]

    def to_representation(self, instance):
        rep = super(ListHouseHoldPayedProductSerializer, self).to_representation(instance)
        rep['category'] = instance.category.name
        rep['district'] = instance.district.name
        rep['user'] = instance.user.full_name
        return rep


class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AddSubCategorySerializer(serializers.ModelSerializer):
    # category = serializers.CharField(source='category.name')

    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'name', 'minimum_price', 'maximum_price']

    def to_representation(self, instance):
        rep = super(AddSubCategorySerializer, self).to_representation(instance)
        rep['category'] = instance.category.name
        return rep


"""serializer for listing electronic products"""
class ListAvailableToSoldProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'product_name', 'product_image'
        ]

    def to_representation(self, instance):
        rep = super(ListAvailableToSoldProductSerializer, self).to_representation(instance)
        rep['category'] = instance.category.name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UsersAccount
        fields = "__all__"

"""serializer for user profile"""
class UserProfileSerializer(serializers.ModelSerializer):
    # profile = serializers.StringRelatedField(many=True)
    # user = serializers.SerializerMethodField()
    # user = serializers.CurrentUserDefault()
    # first_name = serializers.PrimaryKeyRelatedField(queryset=user.profile.first_name,many=False)

    def get_user(self, obj):
        request = self.context.get('request', None)
        if request:
            return UserSerializer(request.user, many=False).data

    class Meta:
        model = Profile
        fields = ['user']