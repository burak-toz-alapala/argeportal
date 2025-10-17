# api/views.py
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from domain.models import Material
from domain.services import SiloCalculator, SiloCalculatorC1, SiloCalculatorC2
from ..serializers.silo_calculate_serializers import SiloCalculationSerializer, MaterialSerializer, MaterialComboboxSerializer, SiloFormSerializer
from ..serializers.silo_calculate_serializers import PressureDataSerializer, PressureFillHopperDataSerializer, PressureDiscHopperDataSerializer

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
    

class PressureFillDataView(APIView):
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
            "x_name": "x (mm)",
            "y_name": "Pressure (MPa)",
            "dates": z_list,
            "series": [
                {"name": "Horizontal pressure Phf", "values": phf},
                {"name": "Wall friction traction Pwf", "values": pwf},
                {"name": "Vertical pressure Pvf", "values": pvf},
            ]
        }
        return Response(response)

class PressureDischargeDataView(APIView):
    def get(self, request):
        data = [
            {"z": 0.00, "Phf": 0.00000, "Pwf": 0.00000, "Pvf": 0.00000},
            {"z": 2000.00, "Phf": 0.01181, "Pwf": 0.00266, "Pvf": 0.01067},
            {"z": 4000.00, "Phf": 0.01849, "Pwf": 0.00417, "Pvf": 0.01670},
            {"z": 6000.00, "Phf": 0.02227, "Pwf": 0.00502, "Pvf": 0.02011},
            {"z": 8000.00, "Phf": 0.02440, "Pwf": 0.00550, "Pvf": 0.02204},
            {"z": 10000.00, "Phf": 0.02561, "Pwf": 0.00577, "Pvf": 0.02313},
            {"z": 12000.00, "Phf": 0.02629, "Pwf": 0.00592, "Pvf": 0.02375},
            {"z": 14000.00, "Phf": 0.02668, "Pwf": 0.00601, "Pvf": 0.02410},
            {"z": 16000.00, "Phf": 0.02689, "Pwf": 0.00606, "Pvf": 0.02429},
            {"z": 18000.00, "Phf": 0.02702, "Pwf": 0.00609, "Pvf": 0.02441},
            {"z": 20000.00, "Phf": 0.02709, "Pwf": 0.00610, "Pvf": 0.02447},
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
            "x_name": "x (mm)",
            "y_name": "Pressure (MPa)",
            "dates": z_list,
            "series": [
                {"name": "Horizontal pressure Phf", "values": phf},
                {"name": "Wall friction traction Pwf", "values": pwf},
                {"name": "Vertical pressure Pvf", "values": pvf},
            ]
        }
        return Response(response)

class PressureFillHopperDataView(APIView):
    def get(self, request):
        data = [
            {"x": 0.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 250.00, "Pnf": 0.01004, "Ptf": 0.00286},
            {"x": 500.00, "Pnf": 0.01523, "Ptf": 0.00433},
            {"x": 750.00, "Pnf": 0.01906, "Ptf": 0.00542},
            {"x": 1000.00, "Pnf": 0.02208, "Ptf": 0.00628},
            {"x": 1250.00, "Pnf": 0.02455, "Ptf": 0.00698},
            {"x": 1500.00, "Pnf": 0.02659, "Ptf": 0.00756},
            {"x": 1750.00, "Pnf": 0.02829, "Ptf": 0.00805},
            {"x": 2000.00, "Pnf": 0.02971, "Ptf": 0.00845},
        ]

        serializer = PressureFillHopperDataSerializer(data, many=True)
        raw_data = serializer.data

        # x ekseni (z değerleri)
        x_list = [row["x"] for row in raw_data]

        # y eksenleri (Pnf, Pwf, Pvf değerleri)
        pnf = [row["Pnf"] for row in raw_data]
        ptf = [row["Ptf"] for row in raw_data]


        response = {
            "x_name": "x (mm)",
            "y_name": "Pressure (MPa)",
            "dates": x_list,
            "series": [
                {"name": "Horizontal pressure Pnf", "values": pnf},
                {"name": "Wall friction traction Ptf", "values": ptf},
            ]
        }
        return Response(response)
    
class PressureDischargeHopperDataView(APIView):
    def get(self, request):
        data = [
            {"x": 0.00, "Pne": 0.00000, "Pte": 0.00000},
            {"x": 250.00, "Pne": 0.00262, "Pte": 0.00075},
            {"x": 500.00, "Pne": 0.00600, "Pte": 0.00171},
            {"x": 750.00, "Pne": 0.01017, "Pte": 0.00289},
            {"x": 1000.00, "Pne": 0.01512, "Pte": 0.00430},
            {"x": 1250.00, "Pne": 0.02089, "Pte": 0.00594},
            {"x": 1500.00, "Pne": 0.02747, "Pte": 0.00781},
            {"x": 1750.00, "Pne": 0.03487, "Pte": 0.00992},
            {"x": 2000.00, "Pne": 0.04309, "Pte": 0.01226},
        ]


        serializer = PressureDiscHopperDataSerializer(data, many=True)
        raw_data = serializer.data

        # x ekseni (z değerleri)
        x_list = [row["x"] for row in raw_data]

        # y eksenleri (Pnf, Pwf, Pvf değerleri)
        pne = [row["Pne"] for row in raw_data]
        pte = [row["Pte"] for row in raw_data]


        response = {
            "x_name": "x (mm)",
            "y_name": "Pressure (MPa)",
            "dates": x_list,
            "series": [
                {"name": "Horizontal pressure Pne", "values": pne},
                {"name": "Wall friction traction Pt3", "values": pte},
            ]
        }
        return Response(response)
    
    
class PressureFillAndDischargeHopperDataView(APIView):
    def get(self, request):
        data = [
            {"x": 0.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 250.00, "Pnf": 0.00487, "Ptf": 0.00217},
            {"x": 500.00, "Pnf": 0.00905, "Ptf": 0.00402},
            {"x": 750.00, "Pnf": 0.01287, "Ptf": 0.00573},
            {"x": 1000.00, "Pnf": 0.01645, "Ptf": 0.00732},
            {"x": 1250.00, "Pnf": 0.01983, "Ptf": 0.00882},
            {"x": 1500.00, "Pnf": 0.02304, "Ptf": 0.01025},
            {"x": 1750.00, "Pnf": 0.02611, "Ptf": 0.01161},
            {"x": 2000.00, "Pnf": 0.02904, "Ptf": 0.01292},
        ]



        serializer = PressureFillHopperDataSerializer(data, many=True)
        raw_data = serializer.data

        # x ekseni (z değerleri)
        x_list = [row["x"] for row in raw_data]

        # y eksenleri (Pnf, Pwf, Pvf değerleri)
        pnf = [row["Pnf"] for row in raw_data]
        ptf = [row["Ptf"] for row in raw_data]


        response = {
            "x_name": "x (mm)",
            "y_name": "Pressure (MPa)",
            "dates": x_list,
            "series": [
                {"name": "Horizontal pressure Pnf", "values": pnf},
                {"name": "Wall friction traction Ptf", "values": ptf},
            ]
        }
        return Response(response)
    
class SiloFormAPIView(APIView):
    def post(self, request):
        serializer = SiloFormSerializer(data=request.data)
        if serializer.is_valid():
            # Veriyi kaydetme işlemi (örnek: DB veya hesaplama)
            veri = serializer.validated_data
            material = Material.objects.get(id=veri["particulate"])
            area = veri["alan"]
            step = veri ["height_range"]
            perimeter = veri["cevre"]
            max_depth = veri["height"]
            class_type = veri["class_type"]
            unit_weight = veri["unit_weight"]
            wall_type = veri["duvar_id"]
            ef = veri["ef"]
            e0 = veri["e0"]
            cop = veri["cop"]
            dc = veri["dc"]
            result = calculate_silo_pressures_step(material, area, perimeter, step, max_depth, class_type, unit_weight, wall_type)
            chart_data = format_silo_pressures_for_chart(result)
            discharge_chart_data = chart_data
            if class_type == 1:
                discharge_chart_data = format_silo_discharge_pressures_c1_for_chart(result, ef, e0, cop, dc)
            if class_type == 2:
                discharge_chart_data = format_silo_discharge_pressures_c2_c3_for_chart(result)

            # JSON olarak dön
            return Response({
                "status": "success",
                "chart_data": chart_data,
                "discharge_chart_data": discharge_chart_data,
                "hesaplanan_degerler": result
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

def calculate_silo_pressures_step(material, area, perimeter, step, max_depth, class_type, unit_weight, wall_type):
    """
    Step artışına göre siloya ait basınç ve sürtünme değerlerini hesaplar.
    İlk değer 0'dan başlar.

    Args:
        material: Material nesnesi
        area: Silo taban alanı
        perimeter: Silo çevresi
        step: Derinlik artış miktarı
        max_depth: Hesaplamanın yapılacağı maksimum derinlik

    Returns:
        list: Her derinlik için hesaplanan değerlerin dict listesi
    """
    if class_type == 1:
        calculator = SiloCalculatorC1(material, area=area, perimeter=perimeter, unit_weight=unit_weight, wall_type=wall_type)
    if class_type == 2:
        calculator = SiloCalculatorC2(material, area=area, perimeter=perimeter, unit_weight=unit_weight, wall_type=wall_type)

    results = []

    z = 0.0  # ilk değer 0
    while z <= max_depth:
        result = {
            'depth': z,
            'horizontal_pressure': calculator.phf(z),
            'wall_friction': calculator.pwf(z),
            'vertical_pressure': calculator.pvf(z),

            # % integer değerler
            'internal_friction_percent': material.internal_friction_mean,
            'lateral_pressure_percent': material.lateral_pressure_mean,
            'wall_friction_percent': material.wall_friction_d1,
        }
        results.append(result)
        z += step  # float step ile de çalışır

    return results

def format_silo_pressures_for_chart(pressure_list, ch=1, cw=1, x_name="z (mm)", y_name="Pressure (MPa)"):
    """
    calculate_silo_pressures_step çıktısını z_list + series formatına çevirir.
    
    Args:
        pressure_list: [{'depth': z, 'horizontal_pressure': ..., 'wall_friction': ..., 'vertical_pressure': ...}, ...]
    
    Returns:
        dict: {"z_list": [...], "series": [{"name": ..., "values": [...]}, ...]}
    """
    # z değerlerini 1000 ile çarp ve 2 decimal
    z_list = [round(row['depth'] * 1000, 2) for row in pressure_list]
    
    # Katsayılarla çarpılmış değerler
    phf = [row['horizontal_pressure'] * ch for row in pressure_list]
    pwf = [row['wall_friction'] * cw for row in pressure_list]
    pvf = [row['vertical_pressure'] for row in pressure_list]

    response = {
        "x_name": x_name,
        "y_name": y_name,
        "dates": z_list,
        "series": [
            {"name": "Horizontal pressure Phf", "values": phf},
            {"name": "Wall friction traction Pwf", "values": pwf},
            {"name": "Vertical pressure Pvf", "values": pvf},
        ]
    }
    return response

def format_silo_discharge_pressures_c2_c3_for_chart(pressure_list, ch=1.15, cw=1.10):
    return format_silo_pressures_for_chart(pressure_list, ch=ch, cw=cw)

def format_silo_discharge_pressures_c1_for_chart(pressure_list, ef, e0, cop, dc):
    e = max(ef, e0)
    ch = 1.15 + 1.5*(1 + 0.4 * e / dc) * cop
    cw = 1.4 * (1 + 0.4 * e / dc)
    return format_silo_pressures_for_chart(pressure_list, ch=ch, cw=cw)