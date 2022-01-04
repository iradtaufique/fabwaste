from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mass_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateAPIView
from userauth.models import UsersAccount

from products.models import Product, Category, SubCategory
from userauth.tokens import account_activation_token
from .serializers import RegisterSerializer, UserLoginSerializer, CreateProductSerializer, ListProductSerializer, \
    ListHouseHoldPayedProductSerializer, AddCategorySerializer, ListAvailableToSoldProductSerializer, \
    AddSubCategorySerializer, ListUsersSerializer, UserProfileSerializer
import jwt


class RegisterUserAPi(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_house_hold=True, is_active=True)
            current_site = get_current_site(request)
            subject = 'Activate Account'
            message = render_to_string(
                'registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(subject=subject, message=message)

            return Response(
                {
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED,
                    "message": "Account Created Successfully",
                }

            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""ApiView for registering agent"""
class RegisterAgentAPiView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_agent=True, is_active=True)

            return Response(
                {
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED,
                    "message": "Account Created Successfully",
                }

            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""ApiView for registering Manufacture"""
class RegisterManufactureAPiView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_manufacture=True, is_active=True)

            return Response(
                {
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED,
                    "message": "Account Created Successfully",
                }

            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""ApiView for registering house_hold"""
class RegisterHouseHoldAPiView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_house_hold=True, is_active=True)

            current_site = get_current_site(request)
            subject = 'Activate Account'
            message = render_to_string(
                'registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(subject=subject, message=message)

            return Response(
                {
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED,
                    "message": "Account Created Successfully",
                }

            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""api view for login a user"""
class UserLoginApiView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        email = data.get('email', )
        password = data.get('password', )
        user = authenticate(email=email, password=password)

        # print(request.data)
        print(user.is_house_hold)

        if user:
            auth_token = jwt.encode({'email': user.email, 'full_name': user.full_name, 'id': user.id},
                                    settings.JWT_SECRET_KEY)
            serializer = UserLoginSerializer(user)

            if user.is_house_hold:
                data = {'user': serializer.data, 'household': user.is_house_hold, 'id': user.id,  'token': auth_token}
            elif user.is_agent:
                data = {'user': serializer.data, 'agent': user.is_agent, 'id': user.id, 'token': auth_token}

            elif user.is_manufacture:
                data = {'user': serializer.data, 'manufacture': user.is_manufacture, 'id': user.id, 'token': auth_token}

            elif user.is_admin:
                data = {'user': serializer.data, 'admin': user.is_admin, 'id': user.id, 'token': auth_token}

            else:
                data = {'message': 'User Has No Role!!'}

            print(data)

            # ----------- description for redirecting users -------------
            # if user.is_house_hold:
            #     return redirect('list_devices_api')
            # ------------end of redirect--------------------------------
            return Response(data, status=status.HTTP_200_OK)

        return Response({'details': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# ====== view for adding device ========
class CreateProductApiView(CreateAPIView):
    serializer_class = CreateProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        print(serializer.data['collected_date'])

        dat = serializer.data['collected_date']
        device = serializer.data['product_name']

        template = render_to_string('send_email.html', {'date': dat})
        template2 = render_to_string('send_email2.html', {'device': device, 'date': dat})

        email1 = (
            ' Thanks for adding your product',
            template,
            settings.EMAIL_HOST_USER,
            [self.request.user.email, 'iradukunda.ta@gmail.com'],
            # ['iradukunda.ta@gmail.com'],
        )
        email2 = (
            ' New Product Added',
            template2,
            settings.EMAIL_HOST_USER,
            ['iradukunda.ta@gmail.com'],
        )
        send_mass_mail((email1, email2), fail_silently=False)

        return redirect('view_product')

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user).order_by('-created_date')


# view for listing devices
class ListDevicesApiView(ListAPIView):
    serializer_class = ListProductSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
        # return Product.objects.all()


# view for listing devices
class ListHouseHoldPayedProductApiView(ListAPIView):
    serializer_class = ListHouseHoldPayedProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user, payed=True)


class ListUsersApiView(ListAPIView):
    serializer_class = ListUsersSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UsersAccount.objects.all()


class DeleteUsersApiView(RetrieveDestroyAPIView):
    serializer_class = ListUsersSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get_queryset(self):
        return UsersAccount.objects.all()


# ApiView for adding category
class AddCategoryApiView(CreateAPIView):
    serializer_class = AddCategorySerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        return


"""API View for listing agents"""
class ListAllAgentAPIView(ListAPIView):
    serializer_class = ListUsersSerializer

    def get_queryset(self):
        return UsersAccount.objects.filter(is_agent=True)


"""API View for agents Details"""
class AgentDetailsAPIView(RetrieveAPIView):
    serializer_class = ListUsersSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return UsersAccount.objects.filter(is_agent=True)


"""APi view for listing electronics products"""
class ListElectronicsProductsApiView(ListAPIView):
    serializer_class = ListAvailableToSoldProductSerializer

    def get_queryset(self):
        return Product.objects.filter(category__name='Electronics')


"""APi view for listing Plastics products"""
class ListPlasticsProductsApiView(ListAPIView):
    serializer_class = ListAvailableToSoldProductSerializer

    def get_queryset(self):
        return Product.objects.filter(category__name='Plastics')


"""APi view for listing Plastics products"""
class ListMetalsProductsApiView(ListAPIView):
    serializer_class = ListAvailableToSoldProductSerializer

    def get_queryset(self):
        return Product.objects.filter(category__name='Metals')


"""APi view for listing Plastics products"""
class ListTextileProductsApiView(ListAPIView):
    serializer_class = ListAvailableToSoldProductSerializer

    def get_queryset(self):
        return Product.objects.filter(category__name='Textile')


"""view for product details"""
class ProductDetailsAPIView(RetrieveAPIView):
    serializer_class = ListProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'


"""view for adding category"""
class AddCategoryAPIView(CreateAPIView):
    serializer_class = AddCategorySerializer

    def get_queryset(self):
        return Category.objects.all()


"""view for Listing category"""
class ListCategoryAPIView(ListAPIView):
    serializer_class = AddCategorySerializer

    def get_queryset(self):
        return Category.objects.all()


"""view for adding sub-category"""
class AddSubCategoryAPIView(CreateAPIView):
    serializer_class = AddSubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.all()


"""view for Listing sub-category"""
class ListSubCategoryAPIView(ListAPIView):
    serializer_class = AddSubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.all()


"""view for Listing sub-category"""
class DeleteCategory(RetrieveDestroyAPIView):
    serializer_class = AddCategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'pk'


"""view for Listing sub-category"""
class DeleteSubCategory(RetrieveDestroyAPIView):
    serializer_class = AddSubCategorySerializer
    queryset = SubCategory.objects.all()
    lookup_field = 'pk'


""" api view for updating subcategory """
class UpdateSubCategory(RetrieveUpdateAPIView):
    serializer_class = AddSubCategorySerializer
    queryset = SubCategory.objects.all()
    lookup_field = 'pk'


class UserProfileAPIView(ListAPIView):
    serializer_class = UserProfileSerializer
    def get_queryset(self):
        return UsersAccount.objects.filter(id=self.request.user.id)