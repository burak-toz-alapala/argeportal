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

    def _prepare_formula_params_phf(self, pressure, wall_friction ):
        ph0 = self.calculator.ph0(pressure, wall_friction)
        z0 = self.calculator.z0(pressure, wall_friction)
        
        return {
            "ph0": ph0,
            "z0": z0
        }
    
    def get_formula_phf(self, ch=1):
        """Normal basınç için formülü döndürür."""
        params = self._prepare_formula_params_phf(pressure=self.pressure_mean, wall_friction=self.wall_friction_mean)
        ph0, z0 = params["ph0"], params["z0"]
        A = ph0 * ch
        formula = (
            rf"$$ p_hf(\mathbf{{z}}) = {self.calculator.round_to_decimal(A)} "
            rf"\left( 1 - e^{{- \mathbf{{z}} / {self.calculator.round_to_decimal(z0)}}} \right) $$"
        )
        return formula
    
    def get_formula_pwf(self, cw=1):
        """Normal basınç için formülü döndürür."""
        params = self._prepare_formula_params_phf(pressure=self.pressure_mean, wall_friction=self.wall_friction_mean)
        ph0, z0 = params["ph0"], params["z0"]
        A = self.wall_friction_mean * ph0 * cw
        formula = (
            rf"$$ p_wf(\mathbf{{z}}) = {self.calculator.round_to_decimal(A)} "
            rf"\left( 1 - e^{{- \mathbf{{z}} / {self.calculator.round_to_decimal(z0)}}} \right) $$"
        )
        return formula
    
    def get_formula_pvf(self):
        """Normal basınç için formülü döndürür."""
        params = self._prepare_formula_params_phf(pressure=self.pressure_mean, wall_friction=self.wall_friction_mean)
        ph0, z0 = params["ph0"], params["z0"]
        A = ph0 / self.pressure_mean
        formula = (
            rf"$$ p_vf(\mathbf{{z}}) = {self.calculator.round_to_decimal(A)} "
            rf"\left( 1 - e^{{- \mathbf{{z}} / {self.calculator.round_to_decimal(z0)}}} \right) $$"
        )
        return formula

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

    def _prepare_formula_params_phf(self, pressure, wall_friction ):
        ph0 = self.calculator.ph0(pressure, wall_friction)
        z0 = self.calculator.z0(pressure, wall_friction)
        
        return {
            "ph0": ph0,
            "z0": z0
        }
    
    def get_formula_phf(self, ch=1):
        """Normal basınç için formülü döndürür."""
        params = self._prepare_formula_params_phf(pressure=self.pressure_upper, wall_friction=self.wall_friction_lower)
        ph0, z0 = params["ph0"], params["z0"]

        A = ph0 * ch
        formula = (
            rf"$$ p_hf(\mathbf{{z}}) = {self.calculator.round_to_decimal(A)} "
            rf"\left( 1 - e^{{- \mathbf{{z}} / {self.calculator.round_to_decimal(z0)}}} \right) $$"
        )
        return formula

    def get_formula_pwf(self, cw=1):
        """Normal basınç için formülü döndürür."""
        params = self._prepare_formula_params_phf(pressure=self.pressure_upper, wall_friction=self.wall_friction_upper)
        ph0, z0 = params["ph0"], params["z0"]
        A = self.wall_friction_upper * ph0 * cw
        formula = (
            rf"$$ p_wf(\mathbf{{z}}) = {self.calculator.round_to_decimal(A)} "
            rf"\left( 1 - e^{{- \mathbf{{z}} / {self.calculator.round_to_decimal(z0)}}} \right) $$"
        )
        return formula

    def get_formula_pvf(self):
        """Normal basınç için formülü döndürür."""
        params = self._prepare_formula_params_phf(pressure=self.pressure_lower, wall_friction=self.wall_friction_lower)
        ph0, z0 = params["ph0"], params["z0"]
        A = ph0 / self.pressure_lower
        formula = (
            rf"$$ p_vf(\mathbf{{z}}) = {self.calculator.round_to_decimal(A)} "
            rf"\left( 1 - e^{{- \mathbf{{z}} / {self.calculator.round_to_decimal(z0)}}} \right) $$"
        )
        return formula
    
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
        self.Y = UnitConverter.kn_per_m3_to_N_per_mm3(kN_weight)
        

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
    
    def round_to_decimal(self, number):
        """
        Verilen sayıyı virgülden sonra 7 basamağa yuvarlar ve sonucu float olarak döndürür.
        
        Parametreler:
        number (float/int): Yuvarlanacak sayı.
        
        Döndürülen Değer:
        float: Yuvarlanmış kayan noktalı sayı.
        """
        return round(number, 7)

class HopperCalculator:
    cb = 1
    fill_load_type = 1
    disc_load_type = 2
    steep_type = 1
    shallow_type = 2
    def __init__(self, material, class_type, hopper_height, hopper_pressure, sorth_div_long, wall_type, degree):
        self.material = material
        self.h_h = hopper_height
        self.p_vf = hopper_pressure
        self.sorth_div_long = sorth_div_long
        self.degree = degree
        self.wall_friction_lower = UnitConverter.from_percent_integer(material.get_wall_friction_lower(wall_type))
        self.pressure_lower= UnitConverter.from_percent_integer(material.lateral_pressure_lower)
        self.hopper_type_number = None
        self.hopper_type_string = None
        self.mu_heff = None
        self.unit_weight_kN_m3 = UnitConverter.from_percent_integer(material.unit_weight_upper)
        self.unit_weight = UnitConverter.kn_per_m3_to_N_per_mm3(self.unit_weight_kN_m3)
        if class_type == 1:
            self.cb_instance = 1.3
        elif class_type in (2, 3, 4):
            self.cb_instance = 1 # Instance değişkeni
        else:
            # hopper_tipi belirtilmemişse veya geçersizse class değişkenini kullan
            self.cb_instance = HopperCalculator.cb
    
    def get_f_factor(self, load_type, degree, mu_heff, wall_friction_lower, hopper_type_number, lateral_pressure_upper):
        """Belirli yük tipine göre f katsayısını döndürür."""
        if load_type == self.fill_load_type:
            # Dolum yük tipi
            return self.calculate_Ff(0.2, degree, mu_heff)

        if load_type == self.disc_load_type:
            # Boşaltma yük tipi
            if hopper_type_number == self.shallow_type:
                return self.calculate_Ff(0.2, degree, mu_heff)
            return self.calculate_Fe(
                phi_l_degrees=lateral_pressure_upper,
                beta_degrees=degree,
                mu_h=wall_friction_lower
            )

        raise ValueError(f"Geçersiz yük tipi: {load_type}")

    def calculate_pressures(self, s, f, mu_heff, degree, unit_weight_upper, h_h, x, p_vft):
        """n, pv ve pn değerlerini hesaplar."""
        n = self.calculate_n(S=s, F=f, mu_heff=mu_heff, beta_degrees=degree)
        pv = self.calculate_pv(
            gamma=unit_weight_upper,
            h_h=h_h,
            n=n,
            x=x,
            p_vft=p_vft
        )
        return self.round_to_decimal(f * pv)
    
    def _prepare_formula_params(self, load_type):
        """Formül için ortak parametreleri hazırlar."""
        self.get_hopper_type()

        p_vft = self.calculate_pvft(self.cb_instance, p_vf=self.p_vf)
        s = self.calculate_s(sorth_div_long=self.sorth_div_long)
        f = self.get_f_factor(
            load_type=load_type,
            degree=self.degree,
            mu_heff=self.mu_heff,
            wall_friction_lower=self.wall_friction_lower,
            hopper_type_number=self.hopper_type_number,
            lateral_pressure_upper=UnitConverter.from_percent_integer(
                self.material.internal_friction_upper
            )
        )
        n = self.calculate_n(S=s, F=f, mu_heff=self.mu_heff, beta_degrees=self.degree)
        h_h = float(self.h_h)
        unit_weight = float(self.unit_weight)
        B = (unit_weight * h_h) / (n - 1)

        return {
            "f": f,
            "B": B,
            "n": n,
            "h_h": h_h,
            "p_vft": p_vft
        }

    def get_formula_normal(self, load_type):
        """Normal basınç için formülü döndürür."""
        params = self._prepare_formula_params(load_type)
        f, B, n, h_h, p_vft = params["f"], params["B"], params["n"], params["h_h"], params["p_vft"]

        formula = (
            rf"$$ p_n(\mathbf{{x}}) = {self.round_to_decimal(f)} \cdot \Bigg( "
            rf"{self.round_to_decimal(B)} \cdot \left( \frac{{\mathbf{{x}}}}{{{self.round_to_decimal(h_h)}}} - "
            rf"\left(\frac{{\mathbf{{x}}}}{{{self.round_to_decimal(h_h)}}}\right)^{{{self.round_to_decimal(n)}}} \right) "
            rf"+ {self.round_to_decimal(p_vft)} \cdot \left(\frac{{\mathbf{{x}}}}{{{self.round_to_decimal(h_h)}}}\right)^{{{self.round_to_decimal(n)}}} "
            rf"\Bigg) $$"
        )

        return formula

    def get_formula_wall(self, load_type):
        """Duvar basıncı için formülü LaTeX formatında döndürür."""
        params = self._prepare_formula_params(load_type)
        f, B, n, h_h, p_vft = params["f"], params["B"], params["n"], params["h_h"], params["p_vft"]

        C = self.mu_heff * f

        formula = (
            rf"$$ p_w(x) = {self.round_to_decimal(C)} \cdot \Bigg( "
            rf"{self.round_to_decimal(B)} \cdot \left( \frac{{x}}{{{self.round_to_decimal(h_h)}}} - "
            rf"\left(\frac{{x}}{{{self.round_to_decimal(h_h)}}}\right)^{{{self.round_to_decimal(n)}}} \right) "
            rf"+ {self.round_to_decimal(p_vft)} \cdot \left(\frac{{x}}{{{self.round_to_decimal(h_h)}}}\right)^{{{self.round_to_decimal(n)}}} "
            rf"\Bigg) $$"
        )

        return formula

    def calculate_normal_pressure(self, load_type, x):
        """Normal pressure (N/mm²)"""
        # Hopper tipini al
        self.get_hopper_type()

        # Ara hesaplamalar
        p_vft = self.calculate_pvft(self.cb_instance, p_vf=self.p_vf)
        s = self.calculate_s(sorth_div_long=self.sorth_div_long)

        # f faktörünü hesapla
        f = self.get_f_factor(
            load_type=load_type,
            degree=self.degree,
            mu_heff=self.mu_heff,
            wall_friction_lower=self.wall_friction_lower,
            hopper_type_number=self.hopper_type_number,
            lateral_pressure_upper=UnitConverter.from_percent_integer(self.material.internal_friction_upper)
        )

        # Basınç hesapla
        result_p_n = self.calculate_pressures(
            s=s,
            f=f,
            mu_heff=self.mu_heff,
            degree=self.degree,
            unit_weight_upper=self.unit_weight,
            h_h=self.h_h,
            x=x,
            p_vft=p_vft
        )

        return result_p_n
    
    def t_p_n(self, load_type, x):
        """Horizontal pressure (N/mm²)"""
        self.get_hopper_type()
        p_vft = self.calculate_pvft(self.cb_instance, p_vf=self.p_vf)
        s = self.calculate_s(sorth_div_long=self.sorth_div_long)
        if load_type == self.fill_load_type:
            f_f = self.calculate_Ff(0.2, self.degree, self.mu_heff)
            f = f_f
           
        if load_type == self.disc_load_type:
            if self.hopper_type_number == self.shallow_type:
                f_e = self.calculate_Ff(0.2, self.degree, self.mu_heff)
            else:
                f_e = self.calculate_Fe(phi_l_degrees=UnitConverter.from_percent_integer(self.material.internal_friction_upper),
                                        beta_degrees=self.degree,
                                        mu_h=self.wall_friction_lower)
            f = f_e
        _n = self.calculate_n(S=s, F=f, mu_heff=self.mu_heff, beta_degrees=self.degree)
        pv = self.calculate_pv(gamma=self.unit_weight,
                                   h_h=self.h_h,
                                   n=_n,
                                   x=x,
                                   p_vft=p_vft)
        
        result_p_n = f*pv
        return result_p_n
    
    def calculate_wall_friction_traction(self, load_type, x):
        """wall_friction_traction (N/mm²)"""
        horizontal_pressure = self.calculate_normal_pressure(load_type, x)
        return self.round_to_decimal(self.mu_heff * horizontal_pressure)
    
    def  calculate_f(self, ):
        pass

    def get_hopper_type(self):
        radyan = math.radians(self.degree)
        tanjant = math.tan(radyan)
        condition = (1-self.pressure_lower)/(2*self.wall_friction_lower)
        
        if tanjant < condition:
            self.hopper_type_number = 1
            self.hopper_type_string = "steep"
            self.mu_heff = self.wall_friction_lower
        else:
            self.hopper_type_number = 2
            self.hopper_type_string = "shallow"
            self.mu_heff = (1 - self.pressure_lower) / (2 * tanjant)
    
    def calculate_pvft(self, cb, p_vf):
        p_vft = p_vf* cb
        return p_vft


    def calculate_s(self, sorth_div_long):
        """
        Verilen short ve long değerlerini kullanarak 's' değerini hesaplar.
        Kural: long veya short 0 ise sonuç 1 olur.
        """
        
        # long veya short 0 ise sonucu 1 olarak döndür


        # long ve short sıfır değilse normal hesaplamayı yap
        # Orijinal formülünüz:
        return 1 + sorth_div_long
    
    def hooper_pressure_ratio_fill(self):
        pass

    def hooper_pressure_ratio_disc(self):
        pass
    
    def calculate_pv(self, gamma, h_h, n, x, p_vft):
        """
        Verilen matematiksel ifadeye göre pv değerini hesaplar.
        
        İfade: pv = (gamma * h_h / (n - 1)) * ((x / h_h) - (x / h_h)**n) + p_vft * (x / h_h)**n
        
        Parametreler:
        gamma (float): Özgül ağırlık veya benzeri bir katsayı.
        h_h (float): Yükseklik/derinlik parametresi.
        n (float): Üstel katsayı.
        x (float): Konum değişkeni.
        p_vft (float): Bir basınç veya benzeri bir değer.
        
        Döndürülen Değer:
        float: Hesaplanan pv değeri.
        
        Hata Kontrolü:
        n'nin 1'e eşit olmaması gerekir.
        h_h'nin 0'a eşit olmaması gerekir.
        """
        
        if n == 1:
            raise ValueError("n parametresi 1 olamaz çünkü bu durum tanımsız bir bölmeye yol açar (n-1 = 0).")
        
        if h_h == 0:
            raise ValueError("h_h parametresi 0 olamaz çünkü bu durum 0'a bölmeye yol açar (x/h_h).")
            
        # (x / h_h) terimini birden çok kez hesaplamamak için değişkene atayalım
        ratio_x_hh = self.round_to_decimal(x / h_h)
        
        # ratio_x_hh'nin n. kuvveti
        ratio_x_hh_power_n = self.round_to_decimal(ratio_x_hh ** n)
        
        # İlk parantez içindeki çarpım katsayısı
        coeff =  self.round_to_decimal((gamma * h_h) / (n - 1))
        
        # Kıvırcık parantez içindeki ifade
        curly_bracket_term =  self.round_to_decimal(ratio_x_hh - ratio_x_hh_power_n)
        
        # Birinci kısım
        term1 =  self.round_to_decimal(coeff * curly_bracket_term)
        
        # İkinci kısım
        term2 =  self.round_to_decimal(p_vft * ratio_x_hh_power_n)
        
        # Sonuç
        pv =  self.round_to_decimal(term1 + term2)
        
        return pv
    
    def calculate_n(self, S, F, mu_heff, beta_degrees):
        """
        Verilen matematiksel ifadeye göre n değerini hesaplar.
        
        İfade: n = S * (F * mu_heff * cot(beta) + F) - 2
        
        Parametreler:
        S (float): Katsayı/Değişken S.
        F (float): Kuvvet/Değişken F.
        mu_heff (float): Etkin sürtünme katsayısı (mu_heff).
        beta_degrees (float): Açı beta, derece cinsinden.
        
        Döndürülen Değer:
        float: Hesaplanan n değeri.
        
        Hata Kontrolü:
        Açı beta'nın tanjantının 0 olduğu durumları (beta = 0, 180, 360, ...)
        tanımsız kotanjanta yol açacağı için ele alır.
        """
        
        # Dereceyi radyana çeviriyoruz çünkü Python'daki trigonometrik fonksiyonlar radyan cinsinden çalışır
        beta_radians = math.radians(beta_degrees)
        # print(f"Hesaplanan beta_radians değeri: {beta_radians}")
        # Tanjant değeri
        tan_beta = math.tan(beta_radians)
        # print(f"Hesaplanan tan_beta değeri: {tan_beta}")
        # Kotanjant hesaplama (1 / tan(beta))
        # Kotanjant'ın tanımsız olduğu durumları kontrol etmeliyiz (tan(beta) = 0)
        if abs(tan_beta) < 1e-9: # Çok küçük bir değere eşitse 0 kabul et
            raise ValueError(
                "Açı beta'nın kotanjantı tanımsızdır (tan(beta) sıfırdır)."
                f"beta = {beta_degrees} derece için bu durum geçerlidir."
            )

        cot_beta = self.round_to_decimal(1.0 / tan_beta)
        # print(f"Hesaplanan cot_beta değeri: {cot_beta}")
        # İfadeyi hesaplayalım
        
        # Parantez içindeki ilk terim (F * mu_heff * cot(beta))
        term_in_parenthesis_1 = self.round_to_decimal(F * mu_heff * cot_beta)
        # print(f"Hesaplanan term_in_parenthesis_1 değeri: {term_in_parenthesis_1}")
        # Parantez içi toplamı
        parenthesis_sum = self.round_to_decimal(term_in_parenthesis_1 + F)
        # print(f"Hesaplanan parenthesis_sum değeri: {parenthesis_sum}")
        # S ile çarpım ve -2
        n = self.round_to_decimal(S * parenthesis_sum - 2)
        # print(f"Hesaplanan n değeri: {n}")
        return n
    
    def calculate_Ff(self, b, beta_degrees, mu_h):
        """
        Verilen matematiksel ifadeye göre Ff değerini hesaplar.
        
        İfade: Ff = 1 - b / (1 + tan(beta) / mu_h)
        
        Parametreler:
        b (float): Katsayı/Değişken b.
        beta_degrees (float): Açı beta, derece cinsinden.
        mu_h (float): Katsayı/Değişken mu_h.
        
        Döndürülen Değer:
        float: Hesaplanan Ff değeri.
        
        Hata Kontrolü:
        mu_h'nin sıfır olmaması gerekir.
        Paydanın sıfır olmaması gerekir.
        """
        
        if mu_h == 0:
            raise ValueError("mu_h (mü_h) parametresi sıfır olamaz çünkü bu, tanımsız bir bölmeye yol açar.")
        
        # Dereceyi radyana çeviriyoruz çünkü Python'daki trigonometrik fonksiyonlar radyan cinsinden çalışır
        beta_radians = math.radians(beta_degrees)
        
        # tan(beta) değerini hesaplayalım
        tan_beta = math.tan(beta_radians)
        
        # Parantez içindeki payda teriminin içindeki kesir: tan(beta) / mu_h
        fraction_term = self.round_to_decimal(tan_beta / mu_h)
        
        # Parantez içindeki ana payda: 1 + tan(beta) / mu_h
        denominator = self.round_to_decimal(1 + fraction_term)
        
        # Ana paydanın sıfır olup olmadığını kontrol edelim
        if denominator == 0:
            raise ValueError(
                "Parantez içindeki ana payda sıfır oldu (1 + tan(beta)/mu_h = 0)."
                "Bu, tanımsız bir bölmeye yol açar."
            )

        # İfadeyi hesaplayalım
        
        # Ana kesir: b / (1 + tan(beta) / mu_h)
        main_fraction = self.round_to_decimal(b / denominator)
        
        # Sonuç
        Ff = self.round_to_decimal(1 - main_fraction)
        
        return Ff
    
        # Adım 1: phi_wh'ı hesaplayan fonksiyon
    
    def calculate_phi_wh(self, mu_h):
        """
        phi_wh = tan⁻¹(mu_h) ifadesini hesaplar.
        Sonuç radyan cinsindendir.
        """
        # math.atan() tanjantın tersidir (arctan)
        return math.atan(mu_h)

    # Adım 2: epsilon'u hesaplayan fonksiyon
    def calculate_epsilon(self, phi_l, mu_h):
        """
        epsilon = phi_wh + sin⁻¹{ sin(phi_wh) / sin(phi_l) } ifadesini hesaplar.
        Tüm açılar (phi_l, phi_wh, epsilon) radyan cinsindendir.
        """
        
        # Öncelikle phi_wh'ı hesapla (Adım 1)
        phi_wh = self.calculate_phi_wh(mu_h)
        
        # Paydadaki sin(phi_l)'nin sıfır olup olmadığını kontrol et
        if math.sin(phi_l) == 0:
            raise ValueError("sin(phi_l) sıfır olamaz. Bu, tanımsız bir bölmeye yol açar.")
        
        # sin(phi_wh) / sin(phi_l) oranı
        ratio = math.sin(phi_wh) / math.sin(phi_l)
        
        # sin⁻¹'in argümanının [-1, 1] aralığında olup olmadığını kontrol et
        # Hassasiyet hatalarını gidermek için küçük bir tolerans kullanıyoruz.
        if ratio >= 1 or ratio <= -1.0:
            raise ValueError(
                f"sin⁻¹ argümanı [-1, 1] aralığı dışındadır ({ratio})."
                "Bu, matematiksel olarak geçersiz bir işlemdir."
            )
        
        # math.asin() sinüsün tersidir (arcsin)
        # Gerekirse hassasiyet için ratio'yu [-1, 1] aralığına sıkıştır
        ratio = max(-1.0, min(1.0, ratio))
        
        # arcsin terimi
        arcsin_term = math.asin(ratio)

        phi_wh_degree = math.degrees(phi_wh)
        arcsin_term_degree =  math.degrees(arcsin_term)
        epsilon = phi_wh_degree + arcsin_term_degree
        
        return epsilon

    # Adım 3: Fe'yi hesaplayan ana fonksiyon
    def calculate_Fe(self, phi_l_degrees, beta_degrees, mu_h):
        """
        Fe = (1 + sin(phi_l) * cos(epsilon)) / (1 - sin(phi_l) * cos(2*beta + epsilon))
        ifadesini hesaplar. Tüm iç hesaplamalar radyan cinsinden yapılır.
        """
        
        # 1. Giriş açılarını radyana çevir
        phi_l_radians = math.radians(phi_l_degrees)
        beta_radians = math.radians(beta_degrees)
        
        # 2. Epsilon'u hesapla (Adım 2)
        # Epsilon hesaplaması sırasında mu_h kontrolü yapılır.
        epsilon_degree = self.calculate_epsilon(phi_l_radians, mu_h)
        epsilon_radians = math.radians(epsilon_degree)
        
        # PAY (Numerator): 1 + sin(phi_l) * cos(epsilon)
        numerator = self.round_to_decimal(1 + math.sin(phi_l_radians) * math.cos(epsilon_radians))
        
        # PAYDA (Denominator) için açıyı hesapla: 2*beta + epsilon
        angle_for_denominator = self.round_to_decimal(2 * beta_radians + epsilon_radians)

        
        # PAYDA: 1 - sin(phi_l) * cos(2*beta + epsilon)
        denominator = 1 - math.sin(phi_l_radians) * math.cos(angle_for_denominator)
        
        # 3. Paydanın sıfır olup olmadığını kontrol et
        if denominator == 0:
            raise ValueError("Ana formülün paydası sıfır oldu. Bu, tanımsız bir Fe değerine yol açar.")
        
        # 4. Fe sonucunu hesapla
        Fe = self.round_to_decimal(numerator / denominator)
        
        return Fe
    
    def round_to_decimal(self, number):
        """
        Verilen sayıyı virgülden sonra 7 basamağa yuvarlar ve sonucu float olarak döndürür.
        
        Parametreler:
        number (float/int): Yuvarlanacak sayı.
        
        Döndürülen Değer:
        float: Yuvarlanmış kayan noktalı sayı.
        """
        return round(number, 7)
       
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
    def kn_per_m3_to_N_per_mm3(value_kn_m3):
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
    

