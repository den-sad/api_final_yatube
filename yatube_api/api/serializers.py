from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, value):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if request and hasattr(request, "data"):
            data = request.data
            following_name = data.get('following', None)

        if not following_name:
            raise serializers.ValidationError(
                'Отсутствует поле following')
        try:
            following_user = User.objects.get(username=following_name)
        except (Exception):
            raise serializers.ValidationError('Автор не найден')

        try:
            Follow.objects.get(
                user=user, following=following_user)
        except Follow.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError(
                'Такая подписка уже существует')

        if user == following_user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        return value
