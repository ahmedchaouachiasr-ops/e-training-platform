from rest_framework import serializers

from training.models import Cours, Formateur


class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cours
        fields = '__all__'

class FormateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formateur
        fields = '__all__'