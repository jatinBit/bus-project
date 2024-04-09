from django.shortcuts import render
from django.http import Http404
from rest_framework.parsers import (FormParser ,MultiPartParser )
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

# for token
from rest_framework_simplejwt.tokens import RefreshToken
# generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Registration Successful','isAdmin':user.is_admin}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      print(user)
      return Response({'token':token, 'msg':'Login Success','isAdmin':user.is_admin}, status=status.HTTP_200_OK)
    else:
      return Response({'error':'Email or Password is not Valid'}, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
  def post(self, request, format=None):
    print(request.user)
    # request.user.auth_token.delete()
    return Response({'msg':'logout successfully',status:status.HTTP_200_OK})

class UserView(APIView):
    permission_classes=[IsAuthenticated]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, format=None):
        profile = self.get_object(request.user.id)
        serializer = UserSerializer(profile)
        return Response(serializer.data)

class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    parser_classes=[FormParser,MultiPartParser]
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        profile = self.get_object(request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        data=request.data
        data['user']=request.user.id
        serializer=UserProfileSerializer(data=data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
          return Response({'msg':'profile created'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        profile = self.get_object(request.user)
        data=request.data
        data['user']=request.user.id
        serializer = UserProfileSerializer(profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UserChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
          return Response({'msg':'password changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          return Response({'msg':'Password reset link Send. Please check your email'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    def post(self,request,uid,token,format=None):
      serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'Password Reset Succesfully'},status=status.HTTP_200_OK)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
"""    
class UserCreateView(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    lookup_field='id'

class LoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )
        if user is not None:
            # login(request, user)
            token = get_tokens_for_user(user)
            # return Response({'token': token.key})
            return Response({'msg': 'login Success','token':token})
        else:
            return Response({'error': 'Invalid credentials'})
"""
