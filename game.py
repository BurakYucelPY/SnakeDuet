import random
import math

class Yem:
    def __init__(self, ekran_w, ekran_h):
        self.ekran_w = ekran_w
        self.ekran_h = ekran_h
        self.spawn()

    def spawn(self):
        self.x = random.randint(50, self.ekran_w - 50)
        self.y = random.randint(50, self.ekran_h - 50)

    def ciz(self, img, cv2):
        cv2.circle(img, (self.x, self.y), 10, (0, 255, 255), -1)

class Yilan:
    def __init__(self, baslangic_x, baslangic_y, renk):
        self.govde = [(baslangic_x, baslangic_y)]
        self.yon = "DURUYOR"
        self.renk = renk
        self.hayatta = True
        self.skor = 0
        self.buyu = False

    def hareket_et(self, yeni_yon, ekran_genislik, ekran_yukseklik):
        if not self.hayatta or yeni_yon == "DURUYOR":
            return

        zıt_yonler = {"SAG": "SOL", "SOL": "SAG", "YUKARI": "ASAGI", "ASAGI": "YUKARI"}
        if zıt_yonler.get(self.yon) != yeni_yon:
            self.yon = yeni_yon

        bas_x, bas_y = self.govde[0]
        hiz = 10 
        
        if self.yon == "SAG": bas_x += hiz
        elif self.yon == "SOL": bas_x -= hiz
        elif self.yon == "YUKARI": bas_y -= hiz
        elif self.yon == "ASAGI": bas_y += hiz

        # Ekran sınırlarını geçince karşı taraftan devam et
        if bas_x < 0:
            bas_x = ekran_genislik
        elif bas_x > ekran_genislik:
            bas_x = 0
        if bas_y < 0:
            bas_y = ekran_yukseklik
        elif bas_y > ekran_yukseklik:
            bas_y = 0

        self.govde.insert(0, (bas_x, bas_y))

        if not self.buyu:
            self.govde.pop()
        else:
            self.buyu = False

    def yedi_mi(self, yem):
        kafa_x, kafa_y = self.govde[0]
        mesafe = math.sqrt((kafa_x - yem.x)**2 + (kafa_y - yem.y)**2)

        if mesafe < 20:
            self.skor += 1
            self.buyu = True
            return True
        return False

    def carpti_mi(self, diger_yilan):
        """Diğer yılana çarpıp çarpmadığını kontrol eder"""
        if not self.hayatta:
            return False
        
        kafa_x, kafa_y = self.govde[0]
        
        # Diğer yılanın tüm gövdesine çarpma kontrolü
        for parca in diger_yilan.govde:
            mesafe = math.sqrt((kafa_x - parca[0])**2 + (kafa_y - parca[1])**2)
            if mesafe < 12:  # Çarpışma mesafesi
                self.hayatta = False
                return True
        
        return False

    def kendine_carpti_mi(self):
        """Kendi gövdesine çarpıp çarpmadığını kontrol eder"""
        if not self.hayatta or len(self.govde) < 4:
            return False
        
        kafa_x, kafa_y = self.govde[0]
        
        # İlk 3 parçayı atla (kafa ve hemen arkası)
        for parca in self.govde[3:]:
            mesafe = math.sqrt((kafa_x - parca[0])**2 + (kafa_y - parca[1])**2)
            if mesafe < 10:
                self.hayatta = False
                return True
        
        return False

    def reset(self, baslangic_x, baslangic_y):
        """Yılanı başlangıç durumuna sıfırlar"""
        self.govde = [(baslangic_x, baslangic_y)]
        self.yon = "DURUYOR"
        self.hayatta = True
        self.skor = 0
        self.buyu = False

    def ciz(self, img, cv2):
        if not self.hayatta:
            return

        for parca in self.govde:
            cv2.rectangle(img, (parca[0]-5, parca[1]-5), (parca[0]+5, parca[1]+5), self.renk, -1)