from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated  
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from notifications.models import Notification
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserFollowSerializer
)
from .models import CustomUser

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'token': user.token,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        login(request, user)
        return Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])  
def user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Class-based views for follow/unfollow functionality
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'user_id'  # Add this line
    
    def post(self, request, *args, **kwargs):
        user_to_follow = self.get_object()
        
        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.following.filter(id=user_to_follow.id).exists():
            return Response({"error": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.follow(user_to_follow):
            return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Unable to follow user."}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request, *args, **kwargs):
        user_to_follow = self.get_object()
        
        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.following.filter(id=user_to_follow.id).exists():
            return Response({"error": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.follow(user_to_follow):
            # Create notification for the user being followed
            Notification.objects.create(
                recipient=user_to_follow,
                actor=request.user,
                verb="started following you"
            )
            
            return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Unable to follow user."}, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'user_id'  
    
    def post(self, request, *args, **kwargs):
        user_to_unfollow = self.get_object()
        
        if not request.user.following.filter(id=user_to_unfollow.id).exists():
            return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.unfollow(user_to_unfollow):
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Unable to unfollow user."}, status=status.HTTP_400_BAD_REQUEST)
    

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  
    queryset = CustomUser.objects.all()  
    
    def post(self, request, *args, **kwargs):
        user_to_unfollow = self.get_object()
        
        if not request.user.following.filter(id=user_to_unfollow.id).exists():
            return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.unfollow(user_to_unfollow):
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Unable to unfollow user."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_followers(request):
    """Get list of followers"""
    followers = request.user.followers.all()
    serializer = UserFollowSerializer(followers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_following(request):
    """Get list of users being followed"""
    following = request.user.following.all()
    serializer = UserFollowSerializer(following, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def user_profile_with_follow_info(request):
    """Get user profile with follow information"""
    serializer = UserProfileSerializer(request.user, context={'request': request})
    return Response(serializer.data)