from rest_framework import serializers
from .models import Post, Comment
from django.conf import settings

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        # Get the post from context
        post_pk = self.context.get('post_pk')
        if post_pk:
            validated_data['post_id'] = post_pk
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'author_username', 'title', 'content', 
                 'created_at', 'updated_at', 'comments', 'comments_count')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at', 'comments')
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        # Set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostListSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments_count = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'author_username', 'title', 'excerpt', 
                 'created_at', 'updated_at', 'comments_count')
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_excerpt(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content