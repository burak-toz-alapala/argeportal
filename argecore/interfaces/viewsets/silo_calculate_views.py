# api/views.py
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from domain.models import Material
from domain.services import SiloCalculator, SiloCalculatorC1, SiloCalculatorC2, HopperCalculator
from ..serializers.silo_calculate_serializers import SiloCalculationSerializer, MaterialSerializer, MaterialComboboxSerializer, SiloFormSerializer
from ..serializers.silo_calculate_serializers import PressureDataSerializer, PressureFillHopperDataSerializer, PressureDiscHopperDataSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated
from services.permissions import IsAuthenticatedForReadJWTForWrite, IsAuthenticatedForReadJWTEngineerWrite
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
    permission_classes = [IsAuthenticatedForReadJWTForWrite]  # Login gerekmiyorsa
    # pagination_class = LargePagination
    

class PressureFillDataView(APIView):
    def get(self, request):
        data = [
            {"z": 0.00, "Phf": 0.00000, "Pwf": 0.00000, "Pvf": 0.00000},
            {"z": 2000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 4000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 6000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 8000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 10000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 12000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 14000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 16000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 18000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 20000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
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
            "x_name": "z (mm)",
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
            {"z": 2000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 4000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 6000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 8000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 10000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 12000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 14000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 16000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 18000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
            {"z": 20000.00, "Phf": 00000, "Pwf": 00000, "Pvf": 00000},
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
            "x_name": "z (mm)",
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
            {"x": 250.00, "Pnf": 00000, "Ptf": 00000},
            {"x": 500.00, "Pnf": 00000, "Ptf": 00000},
            {"x": 750.00, "Pnf": 00000, "Ptf": 00000},
            {"x": 1000.00, "Pnf": 00000, "Ptf": 00000},
            {"x": 1250.00, "Pnf": 00000, "Ptf": 00000},
            {"x": 1500.00, "Pnf": 00000, "Ptf": 00000},
            {"x": 1750.00, "Pnf": 00000, "Ptf": 00000},
            {"x": 2000.00, "Pnf": 00000, "Ptf": 00000},
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
                {"name": "Normal pressure Pnf", "values": pnf},
                {"name": "Wall friction traction Ptf", "values": ptf},
            ]
        }
        return Response(response)
    
class PressureDischargeHopperDataView(APIView):
    def get(self, request):
        data = [
            {"x": 0.00, "Pne": 0.00000, "Pte": 0.00000},
            {"x": 250.00, "Pne": 0.00000, "Pte": 0.00000},
            {"x": 500.00, "Pne": 0.00000, "Pte": 0.00000},
            {"x": 750.00, "Pne": 0.00000, "Pte": 0.00000},
            {"x": 1000.00, "Pne": 0.00000, "Pte": 0.00000},
            {"x": 1250.00, "Pne": 0.00000, "Pte": 0.00000},
            {"x": 1500.00, "Pne": 0.00000, "Pte": 0.00000},
            {"x": 1750.00, "Pne": 0.00000, "Pte": 0.00000},
            {"x": 2000.00, "Pne": 0.00000, "Pte": 0.00000},
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
                {"name": "Normal pressure Pne", "values": pne},
                {"name": "Wall friction traction Pte", "values": pte},
            ]
        }
        return Response(response)
    
    
class PressureFillAndDischargeHopperDataView(APIView):
    def get(self, request):
        data = [
            {"x": 0.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 250.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 500.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 750.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 1000.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 1250.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 1500.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 1750.00, "Pnf": 0.00000, "Ptf": 0.00000},
            {"x": 2000.00, "Pnf": 0.00000, "Ptf": 0.00000},
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
                {"name": "Normal pressure Pnf", "values": pnf},
                {"name": "Wall friction traction Ptf", "values": ptf},
            ]
        }
        return Response(response)
    
# @method_decorator(csrf_exempt, name='dispatch')
class SiloFormAPIView(APIView):
    permission_classes = [IsAuthenticatedForReadJWTEngineerWrite]  # Login gerekmiyorsa
    def post(self, request):
        serializer = SiloFormSerializer(data=request.data)
        if serializer.is_valid():
            # Veriyi kaydetme işlemi (örnek: DB veya hesaplama)
            fill = 1
            disc = 2
            veri = serializer.validated_data
            material = Material.objects.get(id=veri["particulate"])
            area = veri["alan"]
            step = veri ["height_range"]
            step_hopper = veri["height_range_konik"]
            perimeter = veri["cevre"]
            max_depth = veri["height"]
            hopper_height = veri["height_konik"]
            class_type = veri["class_type"]
            unit_weight = veri["unit_weight"]
            wall_type = veri["duvar_id"]
            sorth_div_long = veri["sorth_div_long"]
            degree = veri["degress"]
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

            pvf = result[-1]['vertical_pressure']

            fill_hopper = calculate_hopper_pressures_step(material, step_hopper, class_type, hopper_height, pvf, sorth_div_long, degree, wall_type, load_type=fill)
            disc_hopper = calculate_hopper_pressures_step(material, step_hopper, class_type, hopper_height, pvf, sorth_div_long, degree, wall_type, load_type=disc)
            chart_data_hopper_fill = format_hopper_pressures_for_chart(fill_hopper)
            chart_data_hopper_disc = format_hopper_pressures_for_chart(disc_hopper)

            formula_dict = get_formula(material, area, perimeter, class_type, unit_weight, wall_type, ef, e0, cop, dc, hopper_height, pvf, sorth_div_long, degree)
            # JSON olarak dön
            return Response({
                "status": "success",
                "chart_data": chart_data,
                "discharge_chart_data": discharge_chart_data,
                "fill_chart_data_hopper": chart_data_hopper_fill,
                "discharge_chart_data_hopper": chart_data_hopper_disc,
                "hesaplanan_degerler": result,
                "formul_dict":formula_dict
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
def get_formula(material, area, perimeter, class_type, unit_weight, wall_type, ef, e0, cop, dc, hopper_height, pvf, sorth_div_long, degree):
    if class_type == 1:
        calculator = SiloCalculatorC1(material, area=area, perimeter=perimeter, unit_weight=unit_weight, wall_type=wall_type)
    if class_type == 2:
        calculator = SiloCalculatorC2(material, area=area, perimeter=perimeter, unit_weight=unit_weight, wall_type=wall_type)

    hopper_calc = HopperCalculator(material=material, class_type=class_type, hopper_height=hopper_height,
                                    hopper_pressure=pvf, sorth_div_long=sorth_div_long, wall_type=wall_type,
                                    degree=degree)
    
    ch, cw = get_parametre_discharge(class_type, ef, e0, cop, dc)
    fill = 1
    disc = 2

    result = {

            'fill_phf': calculator.get_formula_phf(),
            'fill_pwf': calculator.get_formula_pwf(),
            'fill_pvf': calculator.get_formula_pvf(),
            
            'disc_phf': calculator.get_formula_phf(ch=ch),
            'disc_pwf': calculator.get_formula_pwf(cw=cw),
            'disc_pvf': calculator.get_formula_pvf(),
            
            'hopper_fill_pnf': hopper_calc.get_formula_normal(load_type=fill),
            'hopper_fill_ptf': hopper_calc.get_formula_wall(load_type=fill),

            'hopper_disc_pnf': hopper_calc.get_formula_normal(load_type=disc),
            'hopper_disc_ptf': hopper_calc.get_formula_wall(load_type=disc),



        }
    return result

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
    steps = int(max_depth // step)
    z = 0.0  # ilk değer 0
    for i in range(steps + 2):
        z = i * step
        if z > max_depth:
            z = max_depth
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
    z_list = [round(row['depth'], 2) for row in pressure_list]
    
    # Katsayılarla çarpılmış değerler
    phf = [round((row['horizontal_pressure'] * ch),5) for row in pressure_list]
    pwf = [round((row['wall_friction'] * cw),5) for row in pressure_list]
    pvf = [round((row['vertical_pressure']),5)for row in pressure_list]

    response = {
        "x_name": x_name,
        "y_name": y_name,
        "dates": z_list,
        "series": [
            {"name": "Yatay Basınç Phf", "values": phf},
            {"name": "Duvar sürtünmesi Pwf", "values": pwf},
            {"name": "Dikey Basınç Pvf", "values": pvf},
        ]
    }
    return response

def get_parametre_discharge(class_type, ef, e0, cop, dc):
    if class_type == 2:
        ch=1.15
        cw=1.10
    else:
        e = max(ef, e0)
        ch = 1.15 + 1.5*(1 + 0.4 * e / dc) * cop
        cw = 1.4 * (1 + 0.4 * e / dc)

    return ch, cw


def format_silo_discharge_pressures_c2_c3_for_chart(pressure_list, ch=1.15, cw=1.10):
    return format_silo_pressures_for_chart(pressure_list, ch=ch, cw=cw)

def format_silo_discharge_pressures_c1_for_chart(pressure_list, ef, e0, cop, dc):
    e = max(ef, e0)
    ch = 1.15 + 1.5*(1 + 0.4 * e / dc) * cop
    cw = 1.4 * (1 + 0.4 * e / dc)
    return format_silo_pressures_for_chart(pressure_list, ch=ch, cw=cw)

def calculate_hopper_pressures_step(material, step, class_type, hopper_height, pvf, sorth_div_long, degree, wall_type, load_type):
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
    hopper_calc = HopperCalculator(material=material, class_type=class_type, hopper_height=hopper_height,
                                    hopper_pressure=pvf, sorth_div_long=sorth_div_long, wall_type=wall_type,
                                    degree=degree)

    results = []

    x = 0.0  # ilk değer 0
    while x <= hopper_height:
        result = {
            'depth': x,
            'normal_pressure': hopper_calc.calculate_normal_pressure(load_type=load_type, x=x),
            'wall_friction': hopper_calc.calculate_wall_friction_traction(load_type=load_type, x=x),


        }
        results.append(result)
        x += step  # float step ile de çalışır

    return results

def format_hopper_pressures_for_chart(pressure_list, x_name="x (mm)", y_name="Pressure (MPa)"):
    """
    calculate_silo_pressures_step çıktısını z_list + series formatına çevirir.
    
    Args:
        pressure_list: [{'depth': z, 'horizontal_pressure': ..., 'wall_friction': ..., 'vertical_pressure': ...}, ...]
    
    Returns:
        dict: {"z_list": [...], "series": [{"name": ..., "values": [...]}, ...]}
    """
    # z değerlerini 1000 ile çarp ve 2 decimal
    z_list = [round(row['depth'], 2) for row in pressure_list]
    
    # Katsayılarla çarpılmış değerler
    phf = [round((row['normal_pressure']),5) for row in pressure_list]
    pwf = [round((row['wall_friction']),5) for row in pressure_list]
   

    response = {
        "x_name": x_name,
        "y_name": y_name,
        "dates": z_list,
        "series": [
            {"name": "Normal Basınç Pn", "values": phf},
            {"name": "Duvar sürtünmesi Pt", "values": pwf},
        ]
    }
    return response