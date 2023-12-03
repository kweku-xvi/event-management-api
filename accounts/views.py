import jwt, os
from .models import User
from .serializers import RegisterUserSerializer, LoginUserSerializer
from .utils import send_verification_email
from dotenv import load_dotenv
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


load_dotenv()


@api_view(['POST'])
def register_user_view(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.get(email=serializer.validated_data['email'])
            token = RefreshToken.for_user(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('verify_user')
            absolute_url = f'http://{current_site}{relative_link}?token={token}'
            link = str(absolute_url)
            send_verification_email(email=user.email, username=user.username, link=link)

            return Response(
                {
                    'success':True,
                    'data':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


api_view(['GET'])
def verify_user_view(request):
    if request.method == 'GET':
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response(
                {
                    'success':True,
                    'message':'Account verified successfully'
                }, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignature as e:
            return Response(
                {
                    'success':False,
                    'message':'Activation link expired'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as e:
            return Response(
                {
                    'success':False,
                    'message':'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.InvalidTokenError as e:
            return Response(
                {
                    'success':False,
                    'message':'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist as e:
            return Response(
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )
        

@api_view(['POST'])
def login_user_view(request):
    if request.method == 'POST':
        serializer = LoginUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            tokens = serializer.generate_jwt_tokens(serializer.validated_data)

            return Response(
                {
                    'success':True,
                    'message':'Login successful!',
                    'tokens':tokens
                }, status=status.HTTP_200_OK
            )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users_view(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = RegisterUserSerializer(users, many=True)

        return Response(
            {
                'success':True,
                'users':serializer.data
            }, status=status.HTTP_200_OK
        )

