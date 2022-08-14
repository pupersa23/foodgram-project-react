from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.models import CountOfIngredient, Ingredient, Recipe, Tag
from users.models import ShoppingCart
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountOfIngredient
        fields = ('id', 'amount',)
        extra_kwargs = {
            'id': {
                'read_only': False,
                'error_messages': {
                    'does_not_exist': 'Такого ингредиента не существует!',
                }
            },
            'amount': {
                'error_messages': {
                    'min_value': 'Количество ингредиента'
                                 ' не может быть меньше {min_value}!'.
                                 format(min_value=1),
                }
            }
        }


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = CountOfIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = RecipeIngredientReadSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time',
        )

    def get_user(self):
        return self.context['request'].user

    def get_is_favorited(self, obj):
        user = self.get_user()
        return (
            user.is_authenticated
            and user.favorites.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.get_user()
        try:
            return (user.is_authenticated
                    and user.shopping_cart.recipes.filter(
                        pk__in=(obj.pk,)).exists())
        except ShoppingCart.DoesNotExist:
            return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = serializers.ListField(
        child=serializers.SlugRelatedField(
            slug_field='id',
            queryset=Tag.objects.all(),
        ),
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )
        extra_kwargs = {
            'cooking_time': {
                'error_messages': {
                    'min_value': 1,
                }
            }
        }

    def validate(self, attrs):
        if attrs['cooking_time'] < 1:
            raise serializers.ValidationError(1)
        if len(attrs['tags']) == 0:
            raise serializers.ValidationError(
                'Рецепт не может быть без тегов!'
            )
        if len(attrs['tags']) > len(set(attrs['tags'])):
            raise serializers.ValidationError('Теги не могут повторяться!')
        if len(attrs['ingredients']) == 0:
            raise serializers.ValidationError(
                'Без ингредиентов рецепта не бывает!'
            )
        id_ingredients = []
        for ingredient in attrs['ingredients']:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента'
                    ' не может быть меньше {min_value}!'.
                    format(min_value=1,)
                )
            id_ingredients.append(ingredient['id'])
        if len(id_ingredients) > len(set(id_ingredients)):
            raise serializers.ValidationError(
                'Ингредиенты не могут повторяться!'
            )
        return attrs

    def add_ingredients_and_tags(self, instance, validated_data):
        ingredients, tags = (
            validated_data.pop('ingredients'), validated_data.pop('tags')
        )
        for ingredient in ingredients:
            count_of_ingredient, _ = CountOfIngredient.objects.get_or_create(
                ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
                amount=ingredient['amount'],
            )
            instance.ingredients.add(count_of_ingredient)
        for tag in tags:
            instance.tags.add(tag)
        return instance

    def create(self, validated_data):
        saved = {}
        saved['ingredients'] = validated_data.pop('ingredients')
        saved['tags'] = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        return self.add_ingredients_and_tags(recipe, saved)

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        instance = self.add_ingredients_and_tags(instance, validated_data)
        return super().update(instance, validated_data)
