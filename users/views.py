from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer

# Create your views here.
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