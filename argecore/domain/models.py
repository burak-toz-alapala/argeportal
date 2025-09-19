from django.db import models

# Create your models here.
# core/models.py
from django.db import models

class Material(models.Model):
    """
    Malzeme modeli.
    Tüm oranlar ve açı değerleri % cinsinden integer olarak saklanır.
    Örn: 36° → 36, 0.5 → 50
    """
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5, blank=True, null=True)  # ✪ veya ⊥
    
    # Birim ağırlık (kN/m³) → integer olarak 100 ile çarpılmış şekilde
    unit_weight_lower = models.IntegerField()  # γₗ * 100
    unit_weight_upper = models.IntegerField()  # γᵤ * 100
    
    angle_of_repose = models.IntegerField()    # φᵣ * 100
    
    # İç sürtünme açısı (%)
    internal_friction_mean = models.IntegerField()  # φᵢm mean * 100
    internal_friction_factor = models.IntegerField()  # φᵢm factor * 100
    
    # Lateral pressure ratio (%)
    lateral_pressure_mean = models.IntegerField()  # K mean * 100
    lateral_pressure_factor = models.IntegerField()  # K factor * 100
    
    # Duvar sürtünme katsayıları (%) * 100
    wall_friction_d1 = models.IntegerField()
    wall_friction_d2 = models.IntegerField()
    wall_friction_d3 = models.IntegerField()
    wall_friction_factor = models.IntegerField()
    
    # Patch load factor (%) * 100
    patch_load_factor = models.IntegerField()

    used = models.IntegerField(default=0)

    def __str__(self):
        return self.name
