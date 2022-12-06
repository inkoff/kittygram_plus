from rest_framework import serializers

from cats.models import Achievement, AchievementCat, Cat, Owner

CHOICES = (
    ("Gray", "Серый"),
    ("Black", "Чёрный"),
    ("White", "Белый"),
    ("Ginger", "Рыжий"),
    ("Mixed", "Смешанный"),
)


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ("id", "name")


class CatSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(many=True, required=False)

    class Meta:
        model = Cat
        fields = ("id", "name", "color", "birth_year", "owner", "achievements")

    def create(self, validated_data: dict):
        if "achievements" not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        achievements = validated_data.pop("achievements")
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement
            )
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat
            )
        return cat


class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ("id", "name", "color")


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ("first_name", "last_name", "cats")
