from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer,UserLoginSerilizer,UserProfileSerializer,UserProfileAdminSerializer
from rest_framework.views import APIView
from .models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .custompermission import AdminPermission,UserPermision
from rest_framework.decorators import permission_classes


class UserRegistration(APIView):
    def post(self,request):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                username = serializer.validated_data['username'],
                email = serializer.validated_data['email'],
                password = serializer.validated_data['password'],
                is_doctor = serializer.validated_data['is_doctor']                
            )
            return Response({"msg":"User Registered Succesfully..."},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

def get_access_token(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }
    


class UserLogin(APIView):
    def post(self,request):
        serializer = UserLoginSerilizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_access_token(user)                
                return Response({'msg':'User Loggined Succesfully','token':token},status=status.HTTP_200_OK)
            return Response({"msg":"Login Failed !!! ",'errors':{'non_filed_errors':['Email or Password  is not Valid']}},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserProfile(APIView):
    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request):
        serializer = UserProfileSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Profile Updated ...','Profile':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response({"msg":"Deleted"},status=status.HTTP_200_OK)


@permission_classes([AdminPermission])
class UserProfileView(APIView):
    def get(self,request):
        user = User.objects.all()
        serilaizer = UserProfileAdminSerializer(user,many=True)
        return Response(serilaizer.data)
    
    def patch(self,request,pk=None):
        if pk is not None:
            user = User.objects.get(pk=pk)
            serializer = UserProfileAdminSerializer(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                if serializer.validated_data['is_active']:
                    return Response({"msg":"User Unblocked !!!"},status=status.HTTP_200_OK)
                return Response({"msg":"User Blocked !!!"},status=status.HTTP_200_OK)
            return Response(serializer.errors)


@permission_classes([UserPermision])
class UserDoctorView(APIView):
    def get(self,request):
        user = User.objects.filter(is_doctor=True)
        serializer = UserProfileAdminSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)