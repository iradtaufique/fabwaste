from django.conf import settings
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
from rest_framework.generics import CreateAPIView, GenericAPIView

from products.models import Product
from userauth.tokens import account_activation_token
from .serializers import RegisterSerializer, UserLoginSerializer, CreateProductSerializer
import jwt


class RegisterUserAPi(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            current_site = get_current_site(request)
            subject = 'Activate Account'
            message = render_to_string(
                'registration/account_activation _email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(subject=subject, message=message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""api view for login a user"""
class UserLoginApiView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        email = data.get('email',)
        password = data.get('password', )
        user = authenticate(email=email, password=password)

        if user:
            auth_token = jwt.encode({'email': user.email}, settings.JWT_SECRET_KEY)
            serializer = UserLoginSerializer(user)
            data = {'user': serializer.data, 'token': auth_token}
            return Response(data, status=status.HTTP_200_OK)

        return Response({'details': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CreateProductApiView(CreateAPIView):
    serializer_class = CreateProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        # dat = form.cleaned_data['collected_date']
        # device = form.cleaned_data['product']
        #
        # template = render_to_string('send_email.html', {'name': request.user, 'date': dat})
        # template2 = render_to_string('send_email2.html', {'name': request.user, 'device': device, 'date': dat})
        #
        # email1 = (
        #     ' Thanks for adding your product',
        #     template,
        #     settings.EMAIL_HOST_USER,
        #     [request.user.email, 'iradukunda.ta@gmail.com'],
        # )
        # email2 = (
        #     ' Thanks for adding your product',
        #     template2,
        #     settings.EMAIL_HOST_USER,
        #     ['iradukunda.ta@gmail.com'],
        # )
        # send_mass_mail((email1, email2), fail_silently=False)
        # # email.fail_silently = False
        # # email.send()
        # return redirect('view_product')

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
