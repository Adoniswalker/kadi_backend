from rest_framework import serializers
from .models import Game, Player


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        extra_kwargs = {
            'started_by': {'required': False}  # Mark started_by as optional
        }

    def update(self, instance, validated_data):
        # Prevent started_by from being updated
        validated_data.pop('started_by', None)
        return super().update(instance, validated_data)

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
