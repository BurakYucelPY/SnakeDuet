import random

class Yilan:
    def __init__(self, baslangic_x, baslangic_y, renk):
        self.govde = [(baslangic_x, baslangic_y)]
        self.yon = "DURUYOR"
        self.renk = renk
        self.hayatta = True
        self.skor = 0

    def hareket_et(self, yeni_yon, ekran_genislik, ekran_yukseklik):
        if not self.hayatta or yeni_yon == "DURUYOR":
            return

        zıt_yonler = {"SAG": "SOL", "SOL": "SAG", "YUKARI": "ASAGI", "ASAGI": "YUKARI"}
        if zıt_yonler.get(self.yon) != yeni_yon:
            self.yon = yeni_yon

        bas_x, bas_y = self.govde[0]

        hiz = 10
        
        if self.yon == "SAG":
            bas_x += hiz
        elif self.yon == "SOL":
            bas_x -= hiz
        elif self.yon == "YUKARI":
            bas_y -= hiz
        elif self.yon == "ASAGI":
            bas_y += hiz

        if bas_x < 0 or bas_x > ekran_genislik or bas_y < 0 or bas_y > ekran_yukseklik:
            self.hayatta = False
            return

        yeni_bas = (bas_x, bas_y)
        self.govde.insert(0, yeni_bas)

        self.govde.pop()

    def ciz(self, img, cv2):
        if not self.hayatta:
            return

        for parca in self.govde:
            cv2.rectangle(img, 
                          (parca[0] - 5, parca[1] - 5), 
                          (parca[0] + 5, parca[1] + 5), 
                          self.renk, 
                          -1)