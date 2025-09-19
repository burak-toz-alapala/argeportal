# api/views.py
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from domain.models import Material
from domain.services import SiloCalculator
from ..serializers.silo_calculate_serializers import SiloCalculationSerializer, MaterialSerializer, MaterialComboboxSerializer
from ..serializers.silo_calculate_serializers import PressureDataSerializer

class SiloCalculationView(APIView):
    def post(self, request):
        serializer = SiloCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        material = Material.objects.get(id=serializer.validated_data['material_id'])
        calculator = SiloCalculator(
            material,
            area=serializer.validated_data['area'],
            perimeter=serializer.validated_data['perimeter']
        )
        z = serializer.validated_data['depth']

        result = {
            'horizontal_pressure': calculator.phf(z),
            'wall_friction': calculator.pwf(z),
            'vertical_pressure': calculator.pvf(z),

            # % integer değerler
            'internal_friction_percent': material.internal_friction_mean,
            'lateral_pressure_percent': material.lateral_pressure_mean,
            'wall_friction_percent': material.wall_friction_d1,
        }
        return Response(result)

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    # pagination_class = LargePagination
    
class MaterialComboboxViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.filter(used=1)
    serializer_class = MaterialComboboxSerializer
    # pagination_class = LargePagination
    

class PressureDataView(APIView):
    def get(self, request):
        data = [
            {"z": 0.00, "Phf": 0.00000, "Pwf": 0.00000, "Pvf": 0.00000},
            {"z": 2000.00, "Phf": 0.00576, "Pwf": 0.00190, "Pvf": 0.01067},
            {"z": 4000.00, "Phf": 0.00902, "Pwf": 0.00298, "Pvf": 0.01670},
            {"z": 6000.00, "Phf": 0.01086, "Pwf": 0.00358, "Pvf": 0.02011},
            {"z": 8000.00, "Phf": 0.01190, "Pwf": 0.00393, "Pvf": 0.02204},
            {"z": 10000.00, "Phf": 0.01249, "Pwf": 0.00412, "Pvf": 0.02313},
            {"z": 12000.00, "Phf": 0.01282, "Pwf": 0.00423, "Pvf": 0.02375},
            {"z": 14000.00, "Phf": 0.01301, "Pwf": 0.00429, "Pvf": 0.02410},
            {"z": 16000.00, "Phf": 0.01312, "Pwf": 0.00433, "Pvf": 0.02429},
            {"z": 18000.00, "Phf": 0.01318, "Pwf": 0.00435, "Pvf": 0.02441},
            {"z": 20000.00, "Phf": 0.01321, "Pwf": 0.00436, "Pvf": 0.02447},
        ]
        serializer = PressureDataSerializer(data, many=True)
        raw_data = serializer.data

        # x ekseni (z değerleri)
        z_list = [row["z"] for row in raw_data]

        # y eksenleri (Phf, Pwf, Pvf değerleri)
        phf = [row["Phf"] for row in raw_data]
        pwf = [row["Pwf"] for row in raw_data]
        pvf = [row["Pvf"] for row in raw_data]

        response = {
            "z_list": z_list,
            "series": [
                {"name": "Horizontal pressure Phf", "values": phf},
                {"name": "Wall friction traction Pwf", "values": pwf},
                {"name": "Vertical pressure Pvf", "values": pvf},
            ]
        }
        return Response(response)