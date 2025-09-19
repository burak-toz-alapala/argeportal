# api/serializers.py
from rest_framework import serializers
from domain.models import Material

class SiloCalculationSerializer(serializers.Serializer):
    material_id = serializers.IntegerField()
    area = serializers.FloatField()
    perimeter = serializers.FloatField()
    depth = serializers.FloatField()
    
    horizontal_pressure = serializers.FloatField(read_only=True, help_text="Yatay basınç (kN/m²)")
    wall_friction = serializers.FloatField(read_only=True, help_text="Duvar sürtünmesi (kN/m²)")
    vertical_pressure = serializers.FloatField(read_only=True, help_text="Dikey basınç (kN/m²)")
    
    # Yüzdelik integer değerler
    internal_friction_percent = serializers.IntegerField(read_only=True, help_text="Malzeme iç sürtünme açısı (%)")
    lateral_pressure_percent = serializers.IntegerField(read_only=True, help_text="Lateral pressure ratio (%)")
    wall_friction_percent = serializers.IntegerField(read_only=True, help_text="Duvar sürtünme katsayısı (%)")

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class MaterialComboboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name']


from rest_framework import serializers

class PressureDataSerializer(serializers.Serializer):
    z = serializers.FloatField()
    Phf = serializers.FloatField()
    Pwf = serializers.FloatField()
    Pvf = serializers.FloatField()
