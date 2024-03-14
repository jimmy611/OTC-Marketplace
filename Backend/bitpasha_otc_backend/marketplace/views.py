from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework import viewsets
from .serializers import CustomUserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import render


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    
def transaction_dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    context = {'transactions': transactions}
    return render(request, 'transaction_dashboard.html', context)
    
    
@api_view(['POST'])
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate tokens
    refresh = RefreshToken.for_user(user)

    # Return tokens and user info in response
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Add more user information as needed
        },
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    })



@api_view(['POST'])
def logout(request):
    # Perform logout logic here if needed
    return Response({'message': 'Successfully logged out'})


@api_view(['POST'])
def transactions(request):
    # Extract transaction data from the request
    data = request.data
    
    # Create a new transaction object with the extracted data
    serializer = TransactionSerializer(data=data)
    
    if serializer.is_valid():
        # Save the transaction to the database
        serializer.save()
        
        # Return a success response
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # Return an error response if the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
