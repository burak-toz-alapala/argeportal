import math

class SiloCalculator:
    """
    Silo basınç hesaplamaları.
    Tüm oran ve açı değerleri % olarak integer alınır.
    """

    def __init__(self, material, area, perimeter):
        self.material = material
        self.A = area
        self.U = perimeter
        
        # Tasarım için üst yoğunluk (kN/m³)
        # % cinsinden integer olarak kaydedildiği için 100'e bölerek gerçek float değeri alıyoruz
        self.Y = material.unit_weight_upper / 100.0
        
        # Lateral pressure ratio (K)
        self.K = material.lateral_pressure_mean / 100.0
        self.mu = material.wall_friction_d1 / 100.0

        # Karakteristik derinlik
        self.zo = (1 / (self.K * self.mu)) * (self.A / self.U)

    def Yj(self, z):
        """Derinlik düzeltme faktörü (0-1 arası)"""
        return 1 - math.exp(-z / self.zo)

    def phf(self, z):
        """Horizontal pressure (kN/m²)"""
        pho = self.Y * self.K * self.zo
        return pho * self.Yj(z)

    def pwf(self, z):
        """Wall frictional traction (kN/m²)"""
        return self.mu * self.phf(z)

    def pvf(self, z):
        """Vertical pressure (kN/m²)"""
        return self.K * self.phf(z)

    # 💡 API için integer değer
    def to_percent_integer(self, value):
        """
        Float oranı % integer cinsine çevirir.
        Örn: 0.36 → 36
        """
        return int(round(value * 100))