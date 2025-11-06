from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .serializers import UserSignupSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpView(APIView):
    def post(self, request):
        #create instance of SignupSerializer & populate it with data from client
        serializer = UserSignupSerializer(data=request.data)

        #if data valid, save new user, return response with success message & validated data
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User created successfully!",
                    "user": {
                        "id": user.id,
                        "full_name": user.full_name,
                        "email": user.email,
                    }
                },
                #send back CREATED status code
                status=status.HTTP_201_CREATED
            )
        else:
            #return errors & error response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request):
        #get email & password from req
        email = request.data.get("email")
        password = request.data.get("password")

        #make sure both fields present
        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        #authenticate user
        user = authenticate(request, email=email, password=password)
        #if authentication fails return error message
        if user is None:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        #if authentication - create JWT tokens & return tokens
        refresh = RefreshToken.for_user(user)   #long-lived token to get new access token
        access = refresh.access_token   #access token used for requests

        #return tokens 
        return Response(
            {
                "refresh": str(refresh),
                "access": str(access),
                "user": {
                    "id": user.id,
                    "email": user.email
            }
        },
        status=status.HTTP_200_OK
    )


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
def dashboard(request):
    return render(request, 'dashboard.html')
