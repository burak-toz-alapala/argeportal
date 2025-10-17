import math


class SiloCalculatorC1:
    def __init__(self, material, area, perimeter, unit_weight, wall_type):
        self.material = material
        self.A = area
        self.U = perimeter
        self.kg_weight = unit_weight
        self.wall_friction_mean = UnitConverter.from_percent_integer(material.get_wall_friction(wall_type))
        self.pressure_mean =  UnitConverter.from_percent_integer(material.lateral_pressure_mean)
        self.calculator = SiloCalculator( self.A, self.U, self.kg_weight)

    def phf(self, z):
        return self.calculator.phf(z, pressure=self.pressure_mean, wall_friction=self.wall_friction_mean)
    
    def pwf(self, z):
        return self.calculator.pwf(z, pressure=self.pressure_mean, wall_friction=self.wall_friction_mean)
    
    def pvf(self, z):
        return self.calculator.pvf(z, pressure=self.pressure_mean, wall_friction=self.wall_friction_mean)
    
    
class SiloCalculatorC2:
    def __init__(self, material, area, perimeter, unit_weight, wall_type):
        self.material = material
        self.A = area
        self.U = perimeter
        self.kg_weight = unit_weight
        self.wall_friction_mean = UnitConverter.from_percent_integer(material.get_wall_friction(wall_type))
        self.pressure_mean = UnitConverter.from_percent_integer(material.lateral_pressure_mean)
        self.pressure_upper= UnitConverter.from_percent_integer(material.lateral_pressure_upper)
        self.pressure_lower= UnitConverter.from_percent_integer(material.lateral_pressure_lower)
        self.wall_friction_upper = UnitConverter.from_percent_integer(material.get_wall_friction_upper(wall_type))
        self.wall_friction_lower = UnitConverter.from_percent_integer(material.get_wall_friction_lower(wall_type))
        self.calculator = SiloCalculator( self.A, self.U, self.kg_weight)
    
    def phf(self, z):
        return self.calculator.phf(z, pressure=self.pressure_upper, wall_friction=self.wall_friction_lower)
    
    def pwf(self, z):
        return self.calculator.pwf(z, pressure=self.pressure_upper, wall_friction=self.wall_friction_upper)
    
    def pvf(self, z):
        return self.calculator.pvf(z, pressure=self.pressure_lower, wall_friction=self.wall_friction_lower)

class SiloCalculator:
    """
    Silo basınç hesaplamaları.
    Tüm oran ve açı değerleri % olarak integer alınır.
    """

    def __init__(self, area, perimeter, unit_weight):
        self.A = area
        self.U = perimeter
        self.kg_weight = unit_weight

        
        # Tasarım için üst yoğunluk (kN/m³)
        # % cinsinden integer olarak kaydedildiği için 100'e bölerek gerçek float değeri alıyoruz
        kN_weight = UnitConverter.kg_per_m3_to_kn_per_m3(self.kg_weight)
        self.Y = UnitConverter.kn_per_m3_to_n_per_mm3(kN_weight)
        

        # Karakteristik derinlik

    def z0(self, pressure, wall_friction):
        return (1 / (pressure * wall_friction)) * (self.A / self.U)

    def ph0(self, pressure, wall_friction):
        return self.Y * pressure * self.z0(pressure, wall_friction)

    def Yj(self, z, pressure, wall_friction):
        """Derinlik düzeltme faktörü (0-1 arası)"""
        return 1 - math.exp(-z / self.z0(pressure, wall_friction))
    
    def phf(self, z, pressure, wall_friction):
        """Horizontal pressure (N/mm²)"""
        return  self.ph0(pressure, wall_friction) * self.Yj(z, pressure, wall_friction)

    def pwf(self, z, pressure, wall_friction):
        """Wall frictional traction (N/mm²)"""
        return wall_friction * self.ph0(pressure, wall_friction) * self.Yj(z, pressure, wall_friction)

    def pvf(self, z, pressure, wall_friction):
        """Vertical pressure (N/mm²)"""
        return (self.ph0(pressure, wall_friction) * self.Yj(z, pressure, wall_friction)) / pressure



class UnitConverter:

        # 💡 API için integer değer
    @staticmethod
    def to_percent_integer(value):
        """
        Float oranı % integer cinsine çevirir.
        Örn: 0.36 → 36
        """
        return int(round(value * 100))
    
    @staticmethod
    def from_percent_integer(value):
        """
        100 birim üzerinden verilen integer değeri float oranına çevirir.
        Örn: 36 → 0.36
        """
        return value / 100
    
        # Integer → float oran (1000'e bölerek)
    @staticmethod
    def from_per_mille_integer(value):
        """
        1000 birim üzerinden verilen integer değeri float oranına çevirir.
        Örn: 36 → 0.036
        """
        return value / 1000
    @staticmethod
    def kn_per_m3_to_n_per_mm3(value_kn_m3):
        """
        kN/m³ cinsinden verilen değeri N/mm³ cinsine çevirir.
        
        Args:
            value_kn_m3 (float): kN/m³ cinsinden değer
            
        Returns:
            float: N/mm³ cinsinden değer
        """
        return value_kn_m3 * 1e-6
    

    # ---------------------------
    # kN/m³ ↔ kg/m³ dönüşümleri
    # ---------------------------
    @staticmethod
    def kn_per_m3_to_kg_per_m3(kn_per_m3, g=10):
        """kN/m³ → kg/m³"""
        return (kn_per_m3 * 1000) / g
    @staticmethod
    def kg_per_m3_to_kn_per_m3(kg_per_m3, g=10):
        """kg/m³ → kN/m³"""
        return (kg_per_m3 * g) / 1000

    # g = 10 için hızlı kullanım
    @staticmethod
    def kn_per_m3_to_kg_per_m3_g10(kn_per_m3):
        return kn_per_m3 * 100
    @staticmethod
    def kg_per_m3_to_kn_per_m3_g10(kg_per_m3):
        return kg_per_m3 / 100

    # ---------------------------
    # Radyan ↔ Derece dönüşümleri
    # ---------------------------
    @staticmethod
    def rad_to_deg(radian):
        """Radyan → Derece"""
        return radian * (180 / math.pi)
    @staticmethod
    def deg_to_rad(degree):
        """Derece → Radyan"""
        return degree * (math.pi / 180)
    

