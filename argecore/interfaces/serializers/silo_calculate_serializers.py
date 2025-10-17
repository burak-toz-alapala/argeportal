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

class PressureFillHopperDataSerializer(serializers.Serializer):
    x = serializers.FloatField()
    Pnf = serializers.FloatField()
    Ptf = serializers.FloatField()

class PressureDiscHopperDataSerializer(serializers.Serializer):
    x = serializers.FloatField()
    Pne = serializers.FloatField()
    Pte = serializers.FloatField()

class SiloFormSerializer(serializers.Serializer):
    # Formdaki tüm alanları buraya ekle
    particulate = serializers.CharField()
    unit_weight = serializers.FloatField()
    cop = serializers.FloatField()
    height = serializers.FloatField()
    height_konik = serializers.FloatField()
    degress = serializers.FloatField()
    et = serializers.FloatField()
    ef = serializers.FloatField()
    e0 = serializers.FloatField()
    sekil_id = serializers.IntegerField()
    duvar_id = serializers.IntegerField()
    class_type = serializers.IntegerField()
    height_range = serializers.FloatField()
    height_range_konik = serializers.FloatField()
    alan = serializers.FloatField()
    hacim = serializers.FloatField()
    cevre = serializers.FloatField()
    dc = serializers.FloatField()
    sorth_div_long = serializers.FloatField()
    silo_tipi = serializers.CharField()
    duvarTipi = serializers.CharField()
    flexCheckDefault = serializers.BooleanField(required=False)