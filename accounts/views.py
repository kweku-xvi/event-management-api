from .serializers import RegisterUserSerializer, LoginUserSerializer
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def register_user_view(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

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
