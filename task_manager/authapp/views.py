from django.contrib import auth
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer


class UserRegistrationView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_active:
                user.is_active = True
                user.save()
            auth.login(request, user)
            return Response({'Authorization': user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials", "user": user}, status=status.HTTP_400_BAD_REQUEST)

