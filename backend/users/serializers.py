from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from api.models import Recipe
from .models import Follow, User


class CustomUserCreateSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {'is_subscribed': {'required': False}}

    def to_representation(self, obj):
        result = super(CustomUserCreateSerializer, self).to_representation(obj)
        result.pop('password', None)
        return result

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if Follow.objects.filter(
                user=request.user, following__id=obj.id).exists():
            return True
        else:
            return False


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'is_subscribed', 'password'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if Follow.objects.filter(
                user=request.user, following__id=obj.id).exists():
            return True
        else:
            return False

    def to_representation(self, obj):
        result = super(CustomUserSerializer, self).to_representation(obj)
        result.pop('password', None)
        return result


class FollowRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    recipes = FollowRecipesSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.only('id', 'name', 'image', 'cooking_time')
        if limit:
            recipes = recipes[:int(limit)]
        return FollowRecipesSerializer(recipes, many=True).data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if Follow.objects.filter(
                user=request.user, following__id=obj.id).exists():
            return True
        else:
            return False
